const VERSION='walkback-shell-v1.1.3.1';
const BASE=new URL('./',self.location.href);
const SHELL=[
  BASE.href,
  new URL('index.html',BASE).href,
  new URL('presentation.html',BASE).href,
  new URL('manifest.webmanifest',BASE).href,
  new URL('assets/walkback-icon.svg',BASE).href
];
self.addEventListener('install',event=>event.waitUntil(caches.open(VERSION).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('walkback-shell-')&&k!==VERSION).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
  const req=event.request;if(req.method!=='GET')return;
  const url=new URL(req.url);
  if(url.origin===self.location.origin){
    event.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(response=>{if(response.ok){const copy=response.clone();caches.open(VERSION).then(cache=>cache.put(req,copy))}return response}).catch(()=>req.mode==='navigate'?caches.match(new URL('index.html',BASE).href):Response.error())));
  }else if(url.hostname==='cdn.jsdelivr.net'){
    event.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(response=>{if(response.ok||response.type==='opaque'){const copy=response.clone();caches.open(VERSION).then(cache=>cache.put(req,copy))}return response})));
  }
});