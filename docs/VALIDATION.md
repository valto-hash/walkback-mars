# Validation record

Last local validation: 15 November 2026. The current source passes 21 JavaScript tests, 9 Python raster/projection tests, the 698-waypoint SHA-256 integrity check, Python compilation and HTML/inline-JavaScript syntax parsing. The Chromium browser smoke test is configured in GitHub Actions but was not completed locally because the local browser navigation environment blocked localhost; do not treat that check as locally passed. It did pass in GitHub Actions on commit `1464c44722831f0748d7d1104e699ac94fbdc05c` (run: https://github.com/valto-hash/walkback-mars/actions/runs/43667954192); all three CI jobs (JavaScript, Python raster and Chromium smoke) completed successfully.

## Automated checks

Run locally:

```bash
npm test
node scripts/validate_embedded_data.mjs
python -m unittest discover -s scripts -p 'test_*.py' -v
python -m py_compile scripts/prepare_ctx_dem.py scripts/prepare_themis_grid.py scripts/prepare_hirise_patch.py scripts/render_route_figures.py
python scripts/test_browser_smoke.py
```

GitHub Actions runs JavaScript model tests, embedded-waypoint integrity, Python raster import tests and a Chromium browser smoke test. The browser smoke test checks the advanced resource panel, RF estimate, THEMIS/HiRISE JSON loaders, and narrow-screen controls. The external Three.js libraries are loaded from jsDelivr; the browser smoke job therefore needs network access to that CDN.

## Scientific and operational limits

- Tests validate code contracts and synthetic raster handling; they do not validate a real CTX, THEMIS or HiRISE product raster.
- The repository does not bundle the ~87 MB CTX DEM, a THEMIS mosaic or a HiRISE DTM. Importers are prepared, but those products must be separately selected, downloaded, projected/verified and loaded by the team.
- The global terrain grid remains about 215 m per cell. HiRISE is presented only as an independent local patch preview.
- The Minetti-derived walking model is Earth-based; the 0.38-g grade sensitivity adjustment is heuristic. Surface multipliers, resource-hour values, task/rest time and RF parameters are editable hypothetical assumptions, not measured EVA parameters.
- Radio is a simplified single-hop free-space link budget plus a geometric line-of-sight screen; it is not an RF network design.
- The accelerated solar-warning clock is not a forecast, local radiation dose or crew health model.
- The browser smoke test is not a full scientific or accessibility certification. Manual checks on actual target phones and desktops remain necessary.
- GitHub Pages is only live after the repository owner enables Pages and the deployment workflow completes successfully.
