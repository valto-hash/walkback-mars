#!/usr/bin/env node
import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';
const root=new URL('../',import.meta.url),html=fs.readFileSync(new URL('index.html',root),'utf8'),manifest=JSON.parse(fs.readFileSync(new URL('data/manifest.json',root),'utf8'));
const match=html.match(/const WP=(\[[\s\S]*?\]);\nconst EMB=/);if(!match)throw new Error('Could not locate embedded waypoint array.');
const waypoints=vm.runInNewContext(`(${match[1]})`);if(!Array.isArray(waypoints)||waypoints.length!==698)throw new Error(`Expected 698 waypoints, found ${waypoints?.length}.`);
const hash=crypto.createHash('sha256').update(JSON.stringify(waypoints)).digest('hex'),entry=manifest.integrity?.embedded_waypoints;
if(entry?.sha256!==hash)throw new Error(`Waypoint SHA-256 mismatch: expected ${entry?.sha256}, got ${hash}.`);
if(entry.count!==waypoints.length)throw new Error('Manifest waypoint count mismatch.');
const sols=waypoints.map(x=>Number(x[0]));if(sols.some((v,i)=>!Number.isFinite(v)||(i>0&&v<sols[i-1])))throw new Error('Waypoint Sol values must be finite and ordered.');
console.log(`Verified ${waypoints.length} waypoints, Sol ${sols[0]}–${sols.at(-1)}, SHA-256 ${hash}`);
