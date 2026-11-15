const test=require('node:test');const assert=require('node:assert/strict');const M=require('../assets/walkback-advanced-model.js');
test('minimum independent resource is the active bottleneck',()=>assert.deepEqual(M.minResource({oxygen:4,electrical:3.5,cooling:4,co2:3.8}),['electrical',3.5]));
test('usable budget applies reserve then task and rest overhead',()=>{const b=M.usableBudget({oxygen:4,electrical:3.5,cooling:4,co2:3.8},25,.25,.25);assert.equal(b.limiting,'electrical');assert.equal(b.budgetHours,2.3)});
test('zero resources and overhead cannot produce a negative budget',()=>assert.equal(M.usableBudget({oxygen:0,electrical:2},0,2,2).budgetHours,0));
test('terrain and uncertainty multiply travel time transparently',()=>{assert.ok(Math.abs(M.travelTimeMultiplier('sand',20)-1.86)<1e-12);assert.equal(M.travelTimeMultiplier('smooth',0),1)});
test('terrain scenario rejects unknown assumptions',()=>assert.throws(()=>M.terrainMultiplier('mud'),/Unknown assumed surface/));
test('free-space path loss follows the frequency-distance equation',()=>assert.ok(Math.abs(M.freeSpacePathLossDb(400,1)-84.48)<.02));
test('link margin includes power, gains, losses and receiver sensitivity',()=>assert.ok(Math.abs(M.linkMarginDb({frequencyMHz:400,distanceKm:1,powerW:1,txGainDbi:3,rxGainDbi:0,lossesDb:2,sensitivityDbm:-110})-56.52)<.03));
test('radio helpers reject nonphysical negative inputs',()=>assert.throws(()=>M.linkMarginDb({frequencyMHz:400,distanceKm:1,powerW:0,sensitivityDbm:-110}),/Invalid RF/));
