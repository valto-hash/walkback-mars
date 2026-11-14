# WALKBACK: Can You Get Back in Time?

## Project summary

Human exploration of Mars requires more than choosing the shortest line on a map. A traverse must balance terrain, life-support resources, shelter access, communications and scientific value. WALKBACK is an interactive browser prototype for exploring these decisions around Jezero Crater.

The current app embeds 698 NASA/JPL Mars 2020 Perseverance waypoint records spanning Sol 13–2022. It visualizes the rover traverse and a proposed route between seven selected science-stop anchors. A 261 × 261 terrain grid (~215 m per cell) supports a slope screen and a Dijkstra return-time surface. The walking-time proxy uses Minetti et al.'s slope-cost polynomial with an explicitly unvalidated first-order 0.38-g sensitivity assumption. Users can configure a flat-ground reference speed, remaining life-support time and reserve margin, then compare the modeled return time against a second, user-entered hypothetical warning window. Four map states distinguish whether both budgets pass, only the resource budget passes, only the warning window passes, or neither passes. A user-triggered demonstration clock advances one simulated warning-window minute per real second; this is an accelerated storytelling control, not a solar forecast or radiation-dose model. The app also provides a geometric radio viewshed with assumed antenna heights, a first-person camera, route/elevation summaries, a five-Sol scenario, and Portuguese, English, Spanish and German interface text.

An optional import workflow is included for a USGS Astrogeology Jezero DEM mosaic derived from the Mars Reconnaissance Orbiter Context Camera (MRO / CTX). The raw ~87 MB GeoTIFF is not bundled and is not loaded by default. The processing script samples the native ~20 m DEM onto the current ~215 m app grid; this does not preserve 20 m solver resolution and still does not meet the 1–5 m obstacle-screening target in the original challenge brief.

## Route comparison

The proposed straight-line segments between selected anchors total approximately 12.2 km. The Perseverance odometer records approximately 32.3 km across the corresponding traverse segments. The sum of positive elevation changes between successive selected anchors is approximately 784 m. The +784 m figure is not cumulative ascent across every intermediate rover waypoint. These are route-comparison metrics, not a validated human-walkable route.

## Model and uncertainty

The Minetti polynomial was measured on Earth. The app scales only the slope-related cost difference from the level-ground baseline by 0.38 as a transparent sensitivity assumption. Cavagna et al.'s simulated 0.4-g study motivates considering a lower-gravity walking scenario, but it does not calibrate this slope-cost model for suited Mars EVA. The default 2.5 km/h flat-ground input is illustrative, not a suit specification. See [`MODEL.md`](MODEL.md).

## Current limitations

The default terrain remains procedural outside the rover corridor unless the optional CTX grid is downloaded, processed and loaded. Even after import, the solver grid remains ~215 m. The coarse >30° slope screen cannot identify metre-scale obstacles. There is no soil trafficability, regolith cohesion, loose-sand hazard, solar-energy, dust-opacity, live solar-weather, local radiation-dose or shelter-attenuation layer. The warning interval is manually entered. Radio visibility is geometric rather than a full RF link budget. The walking model is not validated for suited humans at 0.38 g. WALKBACK is a research prototype, not a certified EVA safety system.

## NASA data

- Embedded: [NASA/JPL Mars 2020 Perseverance waypoints](https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json).
- Optional import: [USGS / MRO CTX Jezero DEM mosaic](https://astrogeology.usgs.gov/search/map/mars_2020_science_investigation_ctx_dem_mosaic), via [`scripts/prepare_ctx_dem.py`](../scripts/prepare_ctx_dem.py).
- Reference-only sources are listed in [`DATA.md`](DATA.md) and [`CREDITS.md`](../CREDITS.md).

## Five-Sol mission concept

Sol 1 base and delta; Sol 2 Margin Unit; Sol 3 Cheyava Falls and Serpentine Rapids; Sol 4 Pico Turquino and Witch Hazel Hill; Sol 5 return to base without sampling. This is a hypothetical project scenario, not an approved or scheduled NASA crew mission. Instruments, EVA durations, sample counts and masses are proposed assumptions. Recovery of the 10 cached Three Forks sample tubes by a future crew is hypothetical, not an approved mission plan.

## Team and participant protection

Guilherme Albernaz Martins Costa is the adult team member. Two additional team members are under 18; their names are intentionally omitted from these public materials in accordance with the NASA Space Apps 2026 Participant Terms. The official registration should be completed through the event system with all guardian requirements followed.

## AI tools disclosure

ChatGPT (OpenAI) assisted with code review and correction, model-contract tests, technical documentation, data-processing workflow and presentation editing. The team must disclose any additional AI tools actually used and accurately describe their contribution in the official form.

## Repository

https://github.com/valto-hash/walkback-mars