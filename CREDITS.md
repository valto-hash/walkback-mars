# WALKBACK | Credits and data provenance

This file distinguishes datasets embedded by default from optional import sources and reference-only resources.

## Embedded by default

| Resource | Mission / source | Use | Scope / resolution | Credit / status |
|---|---|---|---|---|
| `M20_waypoints.json` | NASA/JPL, Mars 2020 / Perseverance | 698 waypoint records embedded in `index.html`; position, Sol, elevation and odometer support traverse, stop anchors and route comparison | Irregular rover drive-endpoint records, Sol 13–2022; not a fixed raster resolution | Credit NASA/JPL. Verify the dataset-specific notice/terms before further redistribution. Source: https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json |

## Optional import source (not bundled or loaded by default)

| Resource | Mission / instrument | Use | Native resolution | Credit / status |
|---|---|---|---:|---|
| Jezero CTX DEM Mosaic | NASA Mars Reconnaissance Orbiter / Context Camera (MRO / CTX), USGS Astrogeology product | Optional terrain grid imported via `scripts/prepare_ctx_dem.py` and the in-app JSON loader | ~20 m/pixel at source; sampled to ~215 m cells by the current app | Primary product credit: Fred Calef / USGS Astrogeology Science Center; the catalog identifies public-domain use and requests author citation. Cite as: Calef, F. (2021), *Mars 2020 Science Investigation CTX DEM Mosaic*, USGS Astrogeology Science Center. Product page: https://astrogeology.usgs.gov/search/map/mars_2020_science_investigation_ctx_dem_mosaic ; direct GeoTIFF: https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif . The original TIFF is not in this repository. The raster uses Mars equirectangular projection, planetocentric latitude, positive-east longitude, and a 3,396,160 m radius. |

## Reference-only resources (not integrated as active layers)

| Resource | URL | Status |
|---|---|---|
| Mars 2020 Raw Images | https://mars.nasa.gov/mars2020/multimedia/raw-images/ | Linked from stop descriptions by Sol; not embedded. |
| NASA Mars Trek | https://trek.nasa.gov/mars/ | Reference for future orbital products; not embedded. |
| USGS Astrogeology Interactive Maps: Mars | https://astrogeology-usgs.hub.arcgis.com/pages/interactive-maps-mars | Geological reference only; not integrated. |
| Curiosity's Proposed Path up Mount Sharp | https://science.nasa.gov/resource/curiositys-proposed-path-up-mount-sharp/ | Route-method reference only; not an input data layer. |
| NASA Worldview | https://worldview.earthdata.nasa.gov/ | Reference for a possible future Earth mode; not implemented. |
| Mars Odyssey THEMIS controlled mosaics | https://astrogeology.usgs.gov/search/map/mars-odyssey-themis-controlled-mosaics | Reference only; not downloaded or integrated. |

## Reproducible presentation figures

`assets/jezero-route-overview.svg` and `assets/perseverance-elevation-profile.svg` are generated from the 698 waypoint records embedded in `index.html` with `scripts/render_route_figures.py`. They are plots of waypoint geometry/elevation, not image basemaps or digital elevation models.

## Software dependency

| Library | Version / delivery | License / credit |
|---|---|---|
| Three.js and OrbitControls | 0.128.0, loaded from jsDelivr CDN | Three.js is distributed under the MIT License. Retain its notice if redistributing the library. Source: https://github.com/mrdoob/three.js/tree/r128 ; license: https://github.com/mrdoob/three.js/blob/r128/LICENSE |
| Python raster pipeline | Rasterio and NumPy, installed from PyPI by the user | Third-party dependency licenses remain with those projects; see their package metadata. |

## Science references for the walking-cost proxy

- Minetti, A. E. et al. (2002). “Energy cost of walking and running at extreme uphill and downhill slopes.” *Journal of Applied Physiology*, 93(3), 1039–1046. https://doi.org/10.1152/japplphysiol.01177.2001
- Cavagna, G. A. et al. (2000). “The role of gravity in human walking: pendular energy exchange, external work and optimal speed.” *Journal of Physiology*, 528(3), 657–668. https://doi.org/10.1111/j.1469-7793.2000.00657.x

These studies do not validate the app's 0.38-g slope-cost scaling assumption or a suited astronaut walking model.

## Team and under-18 participant protection

The public repository identifies the adult team member only. Names, voices and likenesses of the two under-18 team members are intentionally omitted from public submission materials under the 2026 NASA Space Apps Participant Terms: https://www.spaceappschallenge.org/legal/ .

## AI tools disclosure

ChatGPT (OpenAI) assisted with code review/correction, automated test development, technical documentation, the optional CTX processing workflow and presentation editing. The team must disclose any other AI tools actually used and describe their actual contributions in the official submission form.