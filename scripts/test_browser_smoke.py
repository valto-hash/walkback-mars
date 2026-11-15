#!/usr/bin/env python3
"""Headless-browser smoke test for the hosted-style WALKBACK page."""
from __future__ import annotations
import json, os, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):pass

def main():
    from playwright.sync_api import sync_playwright
    server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    errors=[]
    try:
        with sync_playwright() as p:
            launch={'headless':True,'args':['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--ignore-gpu-blocklist']}
            if os.environ.get('WALKBACK_CHROMIUM_PATH'):launch['executable_path']=os.environ['WALKBACK_CHROMIUM_PATH']
            browser=p.chromium.launch(**launch)
            page=browser.new_page(viewport={'width':1365,'height':900})
            page.on('pageerror',lambda exc:errors.append(str(exc)))
            failed_requests=[]
            page.on('requestfailed',lambda req:failed_requests.append(f'{req.url}: {req.failure}'))
            page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='domcontentloaded',timeout=60000)
            page.wait_for_selector('#advancedPanel',timeout=60000)
            page.wait_for_function("document.querySelector('#h1')?.textContent?.length > 0",timeout=60000)
            try:
                page.wait_for_function("document.querySelector('#advBudget')?.textContent?.trim().length > 0",timeout=20000)
            except Exception:
                print('PAGE ERRORS:',errors)
                print('FAILED REQUESTS:',failed_requests)
                print('ADVANCED PANEL:',page.locator('#advancedPanel').inner_text() if page.locator('#advancedPanel').count() else '(missing)')
                print('BUDGET TEXT:',repr(page.locator('#advBudget').inner_text() if page.locator('#advBudget').count() else '(missing)'))
                raise
            assert page.locator('#advLink').inner_text().strip(),'RF panel did not produce a status.'
            before=page.locator('#advBudget').inner_text()
            page.locator('#advEnergy').fill('2');page.locator('#advEnergy').dispatch_event('change')
            after=page.locator('#advBudget').inner_text()
            assert before!=after,'Changing the electrical limit did not update the bottleneck.'
            page.locator('#r2').fill('2.0');page.locator('#r2').dispatch_event('input')
            assert page.locator('#advPace').input_value()=='custom','Custom pace state was lost.'
            page.locator('#lg').select_option('pt')
            assert page.locator('#advPace').input_value()=='custom','Language change lost custom pace.'
            patch={'schema':'walkback.hirise-patch.v1','width':501,'height':501,'native_pixel_size_m':5,'center_app_local_x_km':0,'center_app_local_y_km':0,'values_m':[123.0]*(501*501)}
            page.locator('#advHiriseFile').set_input_files({'name':'hirise.json','mimeType':'application/json','buffer':json.dumps(patch).encode()})
            try:
                page.wait_for_function("document.querySelector('#advHiriseCanvas')?.style.display === 'block'",timeout=15000)
            except Exception:
                print('HIRISE STATUS:',page.locator('#advHiriseStatus').inner_text())
                print('PAGE ERRORS:',errors)
                raise
            assert page.locator('#advHiriseCanvas').is_visible(),'HiRISE patch preview did not appear.'
            assert '501×501' in page.locator('#advHiriseStatus').inner_text(),'HiRISE metadata missing.'
            themis={'schema':'walkback.themis-visual-grid.v1','width':261,'height':261,'source':'synthetic fixture','values_8bit':[128]*(261*261),'interpretation':'qualitative_only_not_temperature','quantitative_use_allowed':False}
            page.locator('#advThemisFile').set_input_files({'name':'themis.json','mimeType':'application/json','buffer':json.dumps(themis).encode()})
            page.wait_for_function("document.querySelector('#advThemisStatus')?.textContent?.toLowerCase().includes('qualitative only')",timeout=15000)
            assert 'qualitative only' in page.locator('#advThemisStatus').inner_text().lower()
            page.set_viewport_size({'width':390,'height':844})
            assert page.locator('#advSurface').is_visible() and page.locator('#advFreq').is_visible()
            if errors:raise AssertionError('Browser JavaScript errors: '+'; '.join(errors))
            browser.close()
        print('Browser smoke passed: resources, RF, THEMIS, HiRISE and mobile controls.')
    finally:
        server.shutdown();server.server_close()
if __name__=='__main__':main()
