# WALKBACK | Model, parameters and limitations

## 1. Purpose

The prototype compares two travel-time constraints around a selected shelter anchor on the Jezero scene: (1) a return-time budget derived from remaining consumables and an explicit safety margin; and (2) a configurable warning-time window for reaching shelter. It is an exploratory decision-support concept, not an operational EVA planner.

## 2. Grid and terrain representation

The browser computes over a 261 × 261 grid spanning approximately 56 km in each horizontal direction. Cell spacing is approximately 56/260 km, or about 0.215 km (roughly 200–215 m). The procedural terrain is adjusted along the Perseverance traverse corridor using elevation values in the embedded NASA/JPL waypoint records. Away from that corridor, terrain remains procedural. The slope layer therefore does not meet the 1–5 m human-scale target described in the project brief.

## 3. Walking-time cost

For each neighbouring grid cell, the code estimates local slope from the elevation difference and horizontal edge length. The speed term is a configurable flat-ground speed multiplied by an exponential slope penalty inspired by Tobler's hiking function, with a minimum speed floor of 0.15 km/h. The travel-time increment is horizontal edge length divided by the estimated speed. Dijkstra's algorithm propagates minimum travel time from the selected shelter anchor across the grid.

The speed expression implemented in the current HTML is:

`v = max(0.15, v_flat × exp(-3.5 × (abs(g + 0.05) - 0.05)))`

where `g` is the signed local grade used by the code. This is a simplified Tobler-based adaptation, not a validated Mars walking model. It is **not** adjusted for Mars gravity (0.38 g), suit mass, fatigue, thermal loads, terrain material, astronaut physiology or real EVA procedures.

## 4. Blue consumables-constrained envelope

The default demonstration inputs are 4 h remaining consumables, 3 km/h flat-ground speed and a 25% safety margin. The return-time budget is calculated as:

`T_walkback = consumables / (1 + margin)`

Grid cells with computed travel time at or below this budget form the blue reachability envelope. These values are editable demonstration assumptions, not real suit or mission specifications.

## 5. Green shelter-reach envelope

The default warning interval is 45 minutes. The green envelope includes cells whose modeled travel time to the selected shelter is no greater than the configured warning interval converted to hours. It is a warning-window reachability illustration only. There is no live solar-event feed, point-by-point radiation-dose model, atmospheric shielding model or validated shelter dose-attenuation model in the current app.

## 6. Radio line of sight

The code computes a terrain line-of-sight estimate from a 10 m mast at the shelter to a 2 m antenna at the explorer, including a simplified Mars-curvature term using a 3,389.5 km radius. This is a geometric prototype assumption, not a radio link budget; it does not model frequency, power, antenna pattern, atmospheric losses, relay network performance or hardware specifications.

## 7. Route comparison

The seven selected anchor points are matched to nearby waypoint Sols, with target Sols 13, 648, 940, 1219, 1250, 1299 and 1354. The app reports Perseverance odometer distance between selected stops and direct horizontal distance between adjacent stop anchors. The proposed human path is a straight connection of those anchors; it has not been validated as traversable or safe for humans. Elevation differences come from waypoint records.

Values derived from embedded waypoint records and used in the presentation: approximately 12.2 km straight-line distance between selected stop anchors, approximately 32.3 km on the rover odometer, and approximately +784 m cumulative positive elevation gain. These are route-comparison values and should not be interpreted as a human EVA plan.

## 8. Scientific interpretation

Cheyava Falls is presented as a site with organic carbon and textures discussed as possible biosignature clues. The app does not claim that life has been found; non-biological explanations remain possible. The seven-stop expedition and sample quantities are a proposed scenario and estimated values, not an actual NASA crew mission plan.

## 9. Current missing inputs

- A real, high-resolution Jezero digital elevation model beyond the rover corridor.
- Integrated mineralogy and geology layers (for example, HiRISE, CTX, CRISM, USGS maps and ESA HRSC products) with source, resolution and confidence metadata.
- Soil strength / trafficability and loose-sand / rock-hazard models.
- Solar energy, dust opacity, weather and seasonal illumination layers.
- Radiation measurements or dose forecasts by location, including a validated shelter attenuation model.
- Real suit consumable data, EVA procedures and a walking model calibrated for 0.38 g.
- Field/engineering validation and expert review.
