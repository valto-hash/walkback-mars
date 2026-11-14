# WALKBACK | Credits and data provenance

This file distinguishes data embedded in the prototype from resources that are only linked or cited as references. Every new data layer must be recorded in `data/manifest.json` before it is described as integrated.

## Embedded data

| Resource | Mission / source | Use in WALKBACK | Scope / resolution | Confidence and status | Credit / license status |
|---|---|---|---|---|---|
| Mars 2020 Perseverance waypoints (`M20_waypoints.json`) | NASA/JPL, Mars 2020 | 698 records embedded in `index.html`; Sol, location, elevation and odometer fields support the rover traverse, stop anchors and route statistics | Point records at rover drive endpoints; irregular spacing, not a raster resolution; embedded records span Sol 13–2022 | High confidence for source waypoint records; route and safety outputs derived by the app have additional uncertainty | Credit NASA/JPL. Verify the dataset's specific notices/terms before further redistribution. Source: https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json |

## Linked or reference-only resources (not integrated as data layers)

| Resource | URL | Status in current app |
|---|---|---|
| Mars 2020 Raw Images | https://mars.nasa.gov/mars2020/multimedia/raw-images/ | Linked from selected stops by Sol; images are not embedded. |
| NASA Mars Trek | https://trek.nasa.gov/mars/ | Reference for future orbital layers and a real Jezero DEM; not embedded. |
| USGS Astrogeology Interactive Maps: Mars | https://astrogeology-usgs.hub.arcgis.com/pages/interactive-maps-mars | Geological reference only; not integrated. |
| Curiosity's Proposed Path up Mount Sharp | https://science.nasa.gov/resource/curiositys-proposed-path-up-mount-sharp/ | Method reference only; not an input dataset. |
| NASA Worldview | https://worldview.earthdata.nasa.gov/ | Reference for a possible future Earth mode; not implemented. |

## Software dependency

| Library | Version / delivery | License / credit |
|---|---|---|
| Three.js and OrbitControls | 0.128.0, loaded from jsDelivr CDN | Three.js is distributed under the MIT License. Retain its copyright and license notice when redistributing the library. Source: https://github.com/mrdoob/three.js/tree/r128 ; license: https://github.com/mrdoob/three.js/blob/r128/LICENSE |

## Candidate sources for future work

MRO HiRISE, CTX and CRISM; ESA Mars Express HRSC; THEMIS; Curiosity RAD; MCS; MEDA; and MAVEN are discussed as candidates in the project brief. They must not be listed as integrated layers unless they are actually added, with source, resolution, license/credit, confidence and measured/derived status in the manifest.

## Team and under-18 participant protection

This public repository identifies the adult team member only. Names, voices and likenesses of the two under-18 team members are intentionally omitted. The 2026 NASA Space Apps Participant Terms state that recognizable names, voices and likenesses of persons under 18 should not be included in any submission. See https://www.spaceappschallenge.org/legal/ .

## AI tools disclosure

ChatGPT (OpenAI) assisted with preparing and editing the presentation narrative and supporting project documentation. The team must add any other AI tools actually used and describe their actual contributions in the official submission form.
