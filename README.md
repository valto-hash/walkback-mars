# WALKBACK — Can You Get Back in Time?

**NASA Space Apps Challenge 2026 · Jezero Crater, Mars**

WALKBACK is an exploratory, interactive traverse-planning prototype. It asks whether a hypothetical explorer could return to a selected shelter within independently configured life-support limits and a separate, user-defined warning window. It combines the NASA/JPL Perseverance traverse with optional orbital-terrain and imagery import workflows.

> **Important:** WALKBACK is not a certified EVA planner, radiation-protection system, communications design, or astronaut-safety tool. Its resource capacities, walking pace, terrain penalties and radio parameters are editable scenarios, not validated Mars hardware or human-performance data.

## Project files

- [Interactive application](index.html)
- [Seven-slide English presentation](presentation.html)
- [Project description](docs/PROJECT_DESCRIPTION.md)
- [Model, equations and limitations](docs/MODEL.md)
- [Advanced planning assumptions](docs/ADVANCED_MODEL.md)
- [Data inventory and provenance](docs/DATA.md)
- [CTX DEM import](docs/DEM_IMPORT.md)
- [THEMIS visual-grid import](docs/THEMIS_IMPORT.md)
- [HiRISE local DTM patch import](docs/HI_RISE_IMPORT.md)
- [Validation record](docs/VALIDATION.md)
- [Credits](CREDITS.md)

## What is implemented

### Exploration and NASA data

- 698 NASA/JPL Mars 2020 Perseverance waypoint records (Sol 13–2022), embedded and protected by a SHA-256 integrity check.
- 3D Jezero scene, rover traverse, proposed human science stops, rover odometer comparisons and elevation profile.
- Optional import of a processed MRO/CTX Jezero digital elevation grid. The source DEM is approximately 20 m/pixel but the application samples it onto its approximately 215 m/cell global mesh.
- Optional THEMIS controlled-mosaic grayscale overlay. The importer requires an explicitly warped raster and marks the result qualitative-only; it is not a temperature, radiance or dose layer.
- Optional HiRISE high-resolution local DTM patch preview, kept separate from the coarse global route solver.
- NASA raw-image link filtered to the relevant Perseverance Sol for each selected stop.

### Planning scenarios

- Four independent life-support time limits: oxygen, electrical power, thermal control and CO₂ removal. The minimum is treated as the limiting resource.
- Reserve, task/setup overhead, break time, three illustrative pace presets, surface-category multiplier and an additional uncertainty margin.
- Four reachability classes from the independent resource and hypothetical warning-window limits.
- Minetti-inspired slope-cost proxy with a clearly labelled, unvalidated 0.38-g sensitivity assumption.
- Editable single-hop free-space RF link-budget estimate combined with geometric line of sight.
- User-triggered accelerated warning clock (one simulated minute per real second). It is not a solar forecast or dose model.

### Delivery and accessibility

- Portuguese, English, Spanish and German interface.
- Responsive controls, visible keyboard focus, reduced-motion support and live status announcements.
- PWA manifest, install icons and a service worker that caches the app shell and previously fetched assets. First visit still needs network access for the external Three.js CDN.

## Getting started

Serve the folder over HTTP (service workers do not run from `file://`):

```bash
python -m http.server 8000
```

Open `http://localhost:8000/` in a modern browser. Use the **Advanced planning** panel to configure the four resource limits, terrain assumptions and RF parameters. The CTX, THEMIS and HiRISE importers accept their documented processed JSON formats; source rasters are not bundled.

## Optional data workflows

1. **CTX:** download the USGS MRO/CTX Jezero DEM, inspect its product metadata and run `scripts/prepare_ctx_dem.py`. The native raster is about 20 m/pixel; the app mesh is about 215 m/cell.
2. **THEMIS:** inspect the exact PDS/USGS map label, explicitly warp the selected raster into the app-compatible Mars equirectangular projected-metre grid, then run `scripts/prepare_themis_grid.py`. Controlled 8-bit mosaics are visual context only.
3. **HiRISE:** inspect the selected DTM map label, warp to the app-compatible Mars projected-metre convention, then run `scripts/prepare_hirise_patch.py` for a local patch. The preview does not alter global pathfinding.

Do not use terrestrial EPSG:4326 as a shortcut for Mars planetary data. Verify planetocentric/aerocentric latitude, longitude direction, projection, datum/radius and product transform from the exact dataset label before reprojection. See each importer guide for commands and limitations.

## Validation

```bash
npm test
node scripts/validate_embedded_data.mjs
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s scripts -p 'test_*.py' -v
python -m py_compile scripts/prepare_ctx_dem.py scripts/prepare_themis_grid.py scripts/prepare_hirise_patch.py scripts/render_route_figures.py
```

GitHub Actions also runs a Chromium browser smoke test for the advanced controls and importers. A successful CI run is a software check, not scientific validation. Manual checks on target phones and desktops remain necessary. See [docs/VALIDATION.md](docs/VALIDATION.md).

## GitHub Pages

The deploy workflow runs after relevant changes on `main` and can also be started manually. The repository owner must first enable **Settings → Pages → Build and deployment → GitHub Actions**. After the first successful deploy, the expected addresses are:

- `https://valto-hash.github.io/walkback-mars/`
- `https://valto-hash.github.io/walkback-mars/presentation.html`

A passing validation workflow alone does not mean Pages is live.

## Scientific boundaries still open

- No CTX GeoTIFF, THEMIS mosaic or HiRISE DTM is bundled or automatically loaded; import paths and processing scripts are supplied, and the team must acquire and verify real products.
- The global mesh is approximately 215 m/cell. It is not suitable for foot-scale hazard screening; HiRISE remains a local visual patch.
- Surface multipliers are hypothetical uniform scenario factors, not measured trafficability values. No soil mechanics, sinkage, rock abundance, dust adhesion, slope stability or obstacle-negotiation model is included.
- The Minetti polynomial is based on terrestrial walking. Its 0.38-g adjustment is a heuristic, not a suited-Mars-EVA calibration.
- The RF panel is a single-hop free-space approximation plus a geometric line-of-sight screen. There is no full relay-network, pointing, multipath, diffraction or hardware validation.
- There is no live solar-weather feed, particle spectrum, local radiation dose, shield/shelter attenuation, or radiation-health model. Odyssey MARIE archive data is not a local Jezero dose map.
- No independent EVA, geotechnical, radiation-protection or mission-design review has been completed.

Read [docs/MODEL.md](docs/MODEL.md) and [docs/ADVANCED_MODEL.md](docs/ADVANCED_MODEL.md) before interpreting outputs.

## Team and participant privacy

- **Guilherme Albernaz Martins Costa** — adult team member.
- **Two additional team members under 18** — names omitted from these public materials in accordance with the NASA Space Apps 2026 Participant Terms. Follow the guardian, registration and submission-media requirements in the official event terms.

## AI tools disclosure

ChatGPT (OpenAI) assisted with code review/correction, test writing, documentation, data-processing workflow preparation and presentation editing. The team must disclose any other AI tools actually used and describe their real contribution in the official form.

## License decision

No license has yet been selected for the team's original source code. Public visibility is not itself an open-source license. The team must make the license choice collectively; see [docs/LICENSE_DECISION_REQUIRED.md](docs/LICENSE_DECISION_REQUIRED.md). Do not infer that third-party licenses apply to WALKBACK.