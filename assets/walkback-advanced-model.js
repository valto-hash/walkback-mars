/* Pure, testable helpers used by the WALKBACK advanced scenario panel. */
(function(root){
'use strict';
function minResource(values){
 const entries=Object.entries(values||{});if(!entries.length)throw new RangeError('At least one resource is required.');
 for(const [name,value] of entries)if(!Number.isFinite(Number(value))||Number(value)<0)throw new RangeError(`Invalid resource capacity: ${name}`);
 return entries.reduce((a,b)=>Number(a[1])<=Number(b[1])?a:b);
}
function usableBudget(values,reservePct,taskHours=0,restHours=0){
 const [limiting,value]=minResource(values),r=Number(reservePct),t=Number(taskHours),b=Number(restHours);
 if(![r,t,b].every(Number.isFinite)||r<0||t<0||b<0)throw new RangeError('Reserve, task and rest values must be finite and non-negative.');
 return {limiting,capacityHours:Number(value),budgetHours:Math.max(0,Number(value)/(1+r/100)-t-b)};
}
function terrainMultiplier(surface){const values={smooth:1,mixed:1.2,rocky:1.35,sand:1.55};if(!(surface in values))throw new RangeError('Unknown assumed surface.');return values[surface]}
function travelTimeMultiplier(surface,uncertaintyPct){const u=Number(uncertaintyPct);if(!Number.isFinite(u)||u<0||u>100)throw new RangeError('Uncertainty must be between 0 and 100 percent.');return terrainMultiplier(surface)*(1+u/100)}
function freeSpacePathLossDb(frequencyMHz,distanceKm){const f=Number(frequencyMHz),d=Number(distanceKm);if(!Number.isFinite(f)||f<=0||!Number.isFinite(d)||d<=0)throw new RangeError('Frequency and distance must be positive.');return 32.44+20*Math.log10(f)+20*Math.log10(d)}
function linkMarginDb({frequencyMHz,distanceKm,powerW,txGainDbi=0,rxGainDbi=0,lossesDb=0,sensitivityDbm}){const p=Number(powerW),s=Number(sensitivityDbm),g1=Number(txGainDbi),g2=Number(rxGainDbi),loss=Number(lossesDb);if(!Number.isFinite(p)||p<=0||![s,g1,g2,loss].every(Number.isFinite)||loss<0)throw new RangeError('Invalid RF parameter.');return 10*Math.log10(p*1000)+g1+g2-loss-freeSpacePathLossDb(frequencyMHz,distanceKm)-s}
const api=Object.freeze({minResource,usableBudget,terrainMultiplier,travelTimeMultiplier,freeSpacePathLossDb,linkMarginDb});
if(typeof module!=='undefined'&&module.exports)module.exports=api;root.WALKBACK_ADV_MODEL=api;
})(typeof globalThis!=='undefined'?globalThis:this);
