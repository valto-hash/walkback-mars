# WALKBACK | Data inventory

## Integrated source

| Layer | Source | Mission | Content in app | Type | Confidence |
|---|---|---|---|---|---|
| Rover route / selected stop anchors | NASA/JPL M20_waypoints.json | Mars 2020 Perseverance | 698 waypoint records with Sol, longitude, latitude, elevation and odometer fields; used for rover path, anchor locations, elevation profile and route statistics | Mission-recorded waypoint fields; app route summaries are derived | High for source waypoint provenance; derived route interpretation is a model output |

## Derived layers

| Layer | Method | Important limitation |
|---|---|---|
| Procedural Jezero terrain | Procedural terrain synthesis; corrected along rover corridor using waypoint elevations | Not a full real digital elevation model; outside rover corridor is synthetic. |
| Slope | Elevation derivatives on the 261 × 261 grid | Approx. 200–215 m cells, not the 1–5 m human-scale target. |
| Walk-back travel time | Dijkstra over an eight-neighbour grid using slope-dependent Tobler-inspired speed | Simplified cost function; no gravity adjustment, suit model or terrain-material model. |
| Shelter reach | Reachability under a user-selected warning-time window | Not a solar forecast or local radiation-dose calculation. |
| Radio visibility | Terrain line-of-sight with assumed mast/antenna heights and Mars curvature | Not a radio link budget or communications certification. |

## Reference links not integrated as data layers

- Mars Trek: https://trek.nasa.gov/mars/
- USGS Astrogeology Interactive Maps: https://astrogeology-usgs.hub.arcgis.com/pages/interactive-maps-mars
- Curiosity's Proposed Path up Mount Sharp: https://science.nasa.gov/resource/curiositys-proposed-path-up-mount-sharp/
- NASA Worldview: https://worldview.earthdata.nasa.gov/
- Mars 2020 Raw Images: https://mars.nasa.gov/mars2020/multimedia/raw-images/

Add a manifest record for every new data layer before integrating it into the application. Record at least: `id`, title, source, mission, resolution, link, license/credit, confidence, and whether the layer is measured or derived.
