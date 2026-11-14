# WALKBACK | Data inventory and provenance

## Embedded by default

| Layer | Source / mission | Data used | Type / confidence | Status |
|---|---|---|---|---|
| Perseverance traverse | NASA/JPL `M20_waypoints.json`, Mars 2020 | 698 records, Sol, longitude, latitude, elevation and odometer; anchors, route and summaries | Mission waypoint records; derived outputs depend on app model assumptions | Embedded in `index.html` |

## Optional terrain source with processing workflow

| Layer | Source / mission | Native resolution | App representation | Status |
|---|---|---:|---|---|
| Jezero CTX DEM mosaic | USGS Astrogeology product derived from Mars Reconnaissance Orbiter Context Camera (MRO / CTX) | Approximately 20 m/pixel | Resampled to 261 × 261 over 56 km × 56 km, approximately 215 m/cell | Importer and reproducible processor included; raw GeoTIFF is not in repository and grid is not loaded by default |

Source product: https://astrogeology.usgs.gov/search/map/mars_2020_science_investigation_ctx_dem_mosaic

USGS metadata: Mars target; equirectangular projection; planetocentric latitude; positive-east longitude; spherical radius 3,396,160 m. Primary product credit: Fred Calef / USGS Astrogeology Science Center (2021). USGS marks the product public domain and requests author citation.
Direct file (~87 MB): https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif

See [`DEM_IMPORT.md`](DEM_IMPORT.md) and [`scripts/README.md`](../scripts/README.md). The processor converts the app grid directly into Mars equirectangular metres. It does not use Earth EPSG:4326. The native 20 m resolution is not retained in the current solver; the output grid is approximately 215 m and remains too coarse for 1–5 m foot-scale hazards.

## Derived layers

| Layer | Method | Main limitation |
|---|---|---|
| Procedural Jezero terrain | Procedural synthesis with local correction from waypoint elevations | Synthetic outside rover corridor unless optional CTX DEM is loaded |
| Slope | Finite differences on 261 × 261 grid | ~215 m/cell; not human-scale |
| Return-time surface | Dijkstra on an 8-neighbour grid using Minetti-inspired slope-cost sensitivity | 0.38-g scaling is an unvalidated heuristic; no suit or trafficability model |
| Reachability classes | Comparison against independent resource and warning-time budgets | Warning time is user-entered, not a live forecast |
| Radio visibility | Terrain line-of-sight with assumed 10 m mast, 2 m antenna and simplified Mars curvature | Not a radio link budget |

## Reference-only resources (not integrated)

- Mars Trek: https://trek.nasa.gov/mars/
- USGS Astrogeology Interactive Maps: https://astrogeology-usgs.hub.arcgis.com/pages/interactive-maps-mars
- Curiosity's Proposed Path up Mount Sharp: https://science.nasa.gov/resource/curiositys-proposed-path-up-mount-sharp/
- NASA Worldview: https://worldview.earthdata.nasa.gov/
- Mars Odyssey THEMIS controlled mosaics: https://astrogeology.usgs.gov/search/map/mars-odyssey-themis-controlled-mosaics
- Mars 2020 Raw Images: https://mars.nasa.gov/mars2020/multimedia/raw-images/

Do not label reference-only products as integrated data layers in the app or submission. Add a manifest entry before integrating a new dataset, including source, mission, instrument, resolution, credit/license, confidence and measured/derived status.