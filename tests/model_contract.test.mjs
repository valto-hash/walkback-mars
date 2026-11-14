import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(path.join(root, 'index.html'), 'utf8');
const scriptBlocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
assert.ok(scriptBlocks.length >= 1, 'the application must contain its inline application script');
for (const [i, source] of scriptBlocks.entries()) {
  try { new vm.Script(source, { filename: `index.html:inline-script-${i + 1}` }); }
  catch (error) { error.message = `Inline script ${i + 1} failed JavaScript parsing: ${error.message}`; throw error; }
}

const helperMatch = html.match(/const WALKBACK_MODEL=\(\(\)=>\{[\s\S]*?\}\)\(\);/);
assert.ok(helperMatch, 'the shared WALKBACK_MODEL helper block must exist');
const sandbox = {};
vm.runInNewContext(`${helperMatch[0]}\nthis.model = WALKBACK_MODEL;`, sandbox);
const model = sandbox.model;

test('usable support-time budget preserves the explicit reserve', () => {
  assert.equal(model.resourceBudgetHours(4, 25), 3.2);
  assert.equal(45 / 60, 0.75);
});

test('Minetti polynomial matches reference points and is symmetric only where measured', () => {
  assert.equal(model.minettiCost(0), 2.5);
  assert.ok(Math.abs(model.minettiCost(0.1) - 4.899135) < 1e-9);
  assert.ok(Math.abs(model.minettiCost(-0.1) - 1.127125) < 1e-9);
  assert.ok(model.minettiCost(0.45) > model.minettiCost(0));
  assert.equal(model.minettiCost(2), model.minettiCost(0.45), 'grade is clamped to the published model range');
});

test('the Mars gravity adjustment is explicit and preserves configured level speed', () => {
  assert.equal(model.MARS_GRAVITY_RATIO, 0.38);
  assert.equal(model.marsAdjustedCost(0), 2.5);
  assert.ok(model.marsAdjustedCost(0.1) > 2.5);
  assert.ok(model.marsAdjustedCost(0.1) < model.minettiCost(0.1));
  assert.ok(Math.abs(model.walkingSpeed(3, 0) - 3) < 1e-12);
  assert.ok(model.walkingSpeed(3, 0.1) < 3, 'uphill grade reduces modeled speed');
  assert.ok(model.walkingSpeed(3, -0.1) > 3, 'downhill grade lowers modeled cost');
  assert.ok(model.walkingSpeed(3, 0.1, 1) < model.walkingSpeed(3, 0.1, 0.38), 'the full-Earth sensitivity case has a larger slope penalty');
  assert.throws(() => model.marsAdjustedCost(0.1, 0), { name: 'RangeError' });
});

test('reachability classes are independent and mutually exclusive', () => {
  assert.equal(model.classifyTime(0.5, 3.2, 0.75), 'both');
  assert.equal(model.classifyTime(0.75, 3.2, 0.75), 'both');
  assert.equal(model.classifyTime(1.0, 3.2, 0.75), 'resource-only');
  assert.equal(model.classifyTime(3.21, 3.2, 0.75), 'neither');
  assert.equal(model.classifyTime(Infinity, 3.2, 0.75), 'unreachable');
  assert.equal(model.classifyTime(1.0, 0.75, 1.5), 'warning-only');
  assert.equal(model.classifyTime(1.6, 0.75, 1.5), 'neither');
});

test('slope screening boundaries match the on-screen legend', () => {
  assert.equal(model.slopeBand(10), 'low');
  assert.equal(model.slopeBand(10.1), 'moderate');
  assert.equal(model.slopeBand(20), 'moderate');
  assert.equal(model.slopeBand(20.1), 'high');
  assert.equal(model.slopeBand(30), 'high');
  assert.equal(model.slopeBand(30.1), 'blocked');
});

test('Dijkstra helper rejects blocked cells and diagonal corner cutting', () => {
  assert.equal(model.allowsGridMove(20, 10, 15, 15, true, 30), true);
  assert.equal(model.allowsGridMove(20, 31, 15, 15, true, 30), false);
  assert.equal(model.allowsGridMove(20, 10, 31, 15, true, 30), false);
  assert.equal(model.allowsGridMove(20, 10, 15, 15, false, 30), true);
});

test('first-person status colors cover all four classes and unreachable cells', () => {
  assert.equal(model.hudColor('both'), '#1f6b3add');
  assert.equal(model.hudColor('resource-only'), '#12507add');
  assert.equal(model.hudColor('warning-only'), '#a85b18dd');
  assert.equal(model.hudColor('neither'), '#8a1f12dd');
  assert.equal(model.hudColor('unreachable'), '#8a1f12dd');
});

test('invalid values fail loudly', () => {
  assert.throws(() => model.resourceBudgetHours(-1, 25), { name: 'RangeError' });
  assert.throws(() => model.resourceBudgetHours(4, -1), { name: 'RangeError' });
  assert.throws(() => model.walkingSpeed(0, 0), { name: 'RangeError' });
  assert.throws(() => model.minettiCost(Number.NaN), { name: 'RangeError' });
  assert.throws(() => model.validateDemGrid({schema:'walkback.dem-grid.v1',width:261,height:261,base_reference_m:null,values_m:[]}), { name: 'RangeError' });
});

test('CTX DEM validator rejects null base values and sparse data instead of treating null as zero', () => {
  const good={schema:'walkback.dem-grid.v1',width:261,height:261,grid_spacing_km:56/260,base_reference_m:-2500,values_m:Array(261*261).fill(-2500)};
  const parsed=model.validateDemGrid(good);
  assert.equal(parsed.validCells,261*261);
  assert.equal(parsed.baseReferenceM,-2500);
  const withNull={...good,values_m:[null,...good.values_m.slice(1)]};
  assert.equal(model.validateDemGrid(withNull).fallbackCells,1);
  const tooSparse={...good,values_m:Array(261*261).fill(null)};
  assert.throws(()=>model.validateDemGrid(tooSparse),{name:'RangeError'});
});

test('app labels the solar warning as hypothetical and makes the optional CTX DEM workflow explicit', () => {
  assert.match(html, /Hypothetical alert window/);
  assert.match(html, /not a solar forecast or radiation-dose model/);
  assert.match(html, /walkback\.dem-grid\.v1/);
  assert.match(html, /Load processed CTX DEM/);
  assert.match(html, /app grid ≈/);
  assert.match(html, /Minetti-inspired/);
  assert.doesNotMatch(html, /Tobler-inspired speed approximation/);
  assert.match(html, /id=\"alertScenario\"/);
  assert.match(html, /alertRemainingSeconds=Math.max\(0,alertRemainingSeconds-60\)/);
  assert.match(html, /1 simulated minute per real second/);
  assert.match(html, /not a solar forecast or radiation-dose model/);
});


test('hypothetical alert clock is user-triggered and advances one simulated minute per real second', () => {
  assert.match(html, /function toggleAlertClock\(\)/);
  assert.match(html, /alertTimer=setInterval/);
  assert.match(html, /alertRemainingSeconds=Math\.max\(0,alertRemainingSeconds-60\)/);
  assert.match(html, /Tsh=alertRemainingSeconds\/3600/);
  assert.match(html, /1 simulated minute per real second/);
  assert.match(html, /not a solar forecast or radiation-dose model/);
});

test('alert countdown actually advances, pauses and resets the warning-window envelope', () => {
  const start = html.indexOf('const sbl=()=>');
  const end = html.indexOf('function reach(', start);
  assert.ok(start >= 0 && end > start, 'alert clock functions must be present');
  const source = html.slice(start, end);
  const elements = new Map();
  const $ = (selector) => {
    if (!elements.has(selector)) elements.set(selector, { textContent: '' });
    return elements.get(selector);
  };
  const sandbox = {
    lang:'en', U:{en:{alertPause:'Pause',alertStart:'Start',alertReset:'Reset',alertReady:'Ready',alertRunning:'Running',alertFinished:'Finished',alertNote:'Demo only'}},
    PR:{warn:45}, alertRemainingSeconds:2700, alertTimer:null, Tsh:0.75, si:-1, walk:false,
    $,
    setInterval:(fn,ms)=>{sandbox.tick=fn;sandbox.intervalMs=ms;return 7;},
    clearInterval:(id)=>{sandbox.cleared=id;},
    terrain:()=>{sandbox.terrainCalls=(sandbox.terrainCalls||0)+1;},
    simRender:()=>{}, hudUpdate:()=>{}
  };
  vm.runInNewContext(`${source}\nglobalThis.snapshot=()=>({remaining:alertRemainingSeconds,warningHours:Tsh,running:!!alertTimer});\ntoggleAlertClock();`, sandbox);
  assert.equal(sandbox.intervalMs,1000);
  assert.equal(sandbox.snapshot().running,true);
  sandbox.tick();
  assert.equal(sandbox.snapshot().remaining,2640);
  assert.equal(sandbox.snapshot().warningHours,44/60);
  vm.runInNewContext('toggleAlertClock();',sandbox);
  assert.equal(sandbox.snapshot().running,false);
  assert.equal(sandbox.cleared,7);
  vm.runInNewContext('resetAlertClock();',sandbox);
  assert.equal(sandbox.snapshot().remaining,2700);
  assert.equal(sandbox.snapshot().warningHours,0.75);
});

test('language initialization updates the optional DEM controls without a temporal-dead-zone error', () => {
  const start = html.indexOf('function setLang(l){');
  const end = html.indexOf('\n}\n/* Trechos:', start);
  assert.ok(start >= 0 && end > start, 'setLang must be present as a standalone function');
  const source = html.slice(start, end + 2);
  const elements = new Map();
  const $ = (selector) => {
    if (!elements.has(selector)) elements.set(selector, { textContent: '', innerHTML: '', value: '', disabled: false });
    return elements.get(selector);
  };
  const I = { en: { h1:'WALKBACK',lb:'Load waypoints',ll:'Loops',lv:'Vertical',ph:'Places',p:[{n:'Base',w:'What',y:'Why'}],w:'What',y:'Why' } };
  const U = { en: new Proxy({fr:{},cr:'Credits',sp:['slow','medium','fast']}, { get:(target,key)=>key in target?target[key]:String(key) }) };
  const sandbox = {
    lang:'en', I, U, $,
    document:{documentElement:{lang:''}},
    T:()=>I.en, fly:false, walk:false, si:-1, spd:1, anc:0, stops:[{n:'Base'}],
    sbl:()=>{}, renderAlertScenario:()=>{}, simRender:()=>{}, PL:(i)=>I.en.p[i], SRC:[], D:{en:['']}, real:()=>'', draw:()=>{}
  };
  vm.runInNewContext(`${source}; setLang('en');`, sandbox);
  assert.equal(elements.get('#demlb').textContent, 'dem');
  assert.equal(elements.get('#demreset').textContent, 'demReset');
  assert.equal(elements.get('#lgd').textContent, 'lg');
});