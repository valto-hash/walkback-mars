# WALKBACK | NASA Space Apps Challenge 2026 checklist

## Public deliverables

- [x] Public GitHub repository: https://github.com/valto-hash/walkback-mars
- [x] Interactive prototype in `index.html`.
- [x] Seven-slide English presentation in `presentation.html` (maximum seven slides including title/closing).
- [x] Project description, model notes, data inventory, credits, pitch, DEM import instructions and validation report.
- [x] JavaScript model-contract tests: 13 passed in local validation.
- [x] Synthetic CTX DEM/projection tests: 4 passed in local validation.
- [ ] Enable GitHub Pages manually: Settings → Pages → Build and deployment → GitHub Actions. Automated enabling was denied by the connected GitHub App permission.
- [ ] After Pages deployment, test the app and presentation in an incognito browser and from another device.
- [ ] Enter the public demo link and public project/repository link separately in the official Project tab.
- [ ] Reconfirm the official event deadline, deliverable format and required fields in the event portal before submission.

## Participant / AI disclosures

- [x] ChatGPT (OpenAI) assistance with code review/correction, tests, documentation, data-processing workflow and presentation editing is disclosed.
- [ ] Add any other AI tools actually used by team members and accurately describe their contribution.
- [x] Names of the two under-18 team members are omitted from public submission material in accordance with the 2026 Participant Terms.
- [ ] Ensure public videos/materials contain no recognizable names, voices or likenesses of under-18 participants.
- [ ] Confirm parent/legal guardian registration and event accompaniment requirements for minor participants.

## Scientific accuracy and data scope

- [x] The 698 NASA/JPL Perseverance waypoints are identified as the dataset embedded by default.
- [x] MRO / CTX Jezero DEM is distinguished as an optional import source, not bundled or loaded by default.
- [x] CTX source resolution (~20 m) is distinguished from the current app solver grid (~215 m).
- [x] CTX processor uses Mars equirectangular / planetocentric / positive-east coordinates; it does not incorrectly transform them as Earth EPSG:4326.
- [x] Minetti's Earth-based slope-cost polynomial and the 0.38-g sensitivity assumption are explicitly distinguished; the adaptation is not presented as validated EVA physiology.
- [x] The warning interval is labelled as user-entered/hypothetical, not a solar forecast or radiation-dose calculation.
- [x] All four reachability classes are described, and only green satisfies both limits.
- [x] The resource budget includes the reserve margin: 4.0 h / 1.25 = 3.2 h at defaults.
- [x] The slope threshold is identified as coarse-grid screening, not a certified human limit.
- [x] Route metrics are anchor-to-anchor comparisons, not a validated human route or cumulative ascent over all intermediate points.
- [x] Three Forks tube recovery by a future crew is described as hypothetical, not an approved mission plan.
- [ ] Download the original CTX GeoTIFF, process it and load the JSON grid if the team wants to demonstrate the optional MRO/CTX data layer. Do not claim it is active before loading it.
- [ ] Integrate a second mission layer in the live app before claiming the multi-mission data objective is fully achieved.
- [ ] Improve solver resolution toward the 1–5 m human-scale target and validate soil, energy, radiation and shelter inputs before making human-safety claims.
- [ ] Obtain independent review by relevant EVA, planetary-science, geotechnical and radiation specialists for any future safety interpretation.

## License and credits

- [ ] Agree with all contributors on an OSI-compliant license for original source code and add its full text. No license has been silently chosen.
- [ ] Confirm notices for each dataset and third-party library before redistribution.
- [x] NASA/JPL waypoints are credited; optional CTX source and reference-only resources are recorded separately.

## Remaining manual checks

- [ ] Test app in a current desktop browser and a mobile browser with network access (Three.js is loaded from jsDelivr).
- [ ] Load a real processed CTX JSON grid and inspect terrain continuity/NoData status.
- [ ] Verify public pages open without account login.
- [ ] Complete all submission form fields and confirm final submission status in the official NASA Space Apps portal.