# WALKBACK | NASA Space Apps Challenge 2026 checklist

## Public deliverables

- [x] Public repository and source application: https://github.com/valto-hash/walkback-mars
- [x] Seven-slide English presentation in `presentation.html`.
- [x] Technical description, model assumptions, data provenance, import instructions, credits, pitch notes and validation record.
- [x] 21/21 JavaScript tests and 9/9 synthetic raster/projection tests passed locally.
- [x] 698 embedded waypoint records passed SHA-256 integrity validation.
- [x] GitHub Pages deploy workflow added; the repository owner must enable Pages in Settings and run the workflow for the first deployment.
- [ ] Confirm successful deployment and test the public app from a second device/browser.
- [ ] Complete all official portal fields and confirm the final submission status.

## Data and scientific accuracy

- [x] Default embedded dataset identified as NASA/JPL Perseverance waypoints.
- [x] CTX, THEMIS and HiRISE are distinguished as optional import workflows, not loaded layers.
- [x] CTX native resolution (~20 m/pixel) distinguished from the app's ~215 m/cell solver.
- [x] THEMIS controlled mosaic clearly marked qualitative-only, not temperature/radiance/dose.
- [x] HiRISE remains a local high-resolution preview, not global pathfinding.
- [x] Four independent life-support budgets, reserve, tasks/rest and uncertainty scenarios are exposed.
- [x] Surface multipliers are explicitly hypothetical.
- [x] Minetti's Earth-based model and 0.38-g adjustment are explicitly unvalidated for suited Mars EVA.
- [x] Radio margin is labelled a single-hop free-space approximation, not a validated network.
- [x] Warning clock is hypothetical, not a solar forecast or radiation-dose model.
- [x] Four reachability classes are explained; only green passes both limits.

- [ ] Download, reproject, inspect and load actual CTX, THEMIS and HiRISE products before claiming their layers are active.
- [ ] Integrate validated multi-mission imagery/mineralogy/geology layers in the live map.
- [ ] Improve spatial terrain resolution on selected corridors and validate terrain classifications.
- [ ] Add actual soil mechanics, energy, live solar weather, local radiation dose and shelter attenuation models only with verified sources and expert review.
- [ ] Obtain independent review from relevant EVA, geotechnical, radiation and communications specialists.

## License, credits and participant requirements

- [ ] The team must collectively select an OSI-compliant license for original code and add the full license text. No choice has been made on the team's behalf.
- [ ] Verify dataset-specific notices and third-party library terms.
- [x] Public materials avoid identifiable names/media of under-18 team members.
- [ ] Confirm guardian registration and all event-specific rules for minor participants.
- [ ] Disclose all AI tools actually used and their actual contribution in the official form.

## Final checks

- [ ] Enable Pages and confirm both app and presentation URLs load without login.
- [ ] Test mobile and desktop operation with network access; Three.js initially loads from jsDelivr.
- [ ] Check an actual imported raster for CRS, coverage, NoData and terrain continuity.
- [ ] Confirm deadline, format and submission fields in the official event portal.