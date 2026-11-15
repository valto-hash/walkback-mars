# Validation record

Local validation performed 15 November 2026: 21/21 JavaScript tests passed; 9/9 synthetic raster/projection tests passed; 698 embedded Mars 2020 Perseverance waypoints passed SHA-256 integrity validation (Sols 13–2022); Python compilation and HTML/inline JavaScript syntax checks passed. Chromium browser smoke is configured in GitHub Actions but could not be completed locally because the local browser environment blocked localhost. Do not describe it as locally passed.

Run locally:

```bash
npm test
npm run validate:data
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s scripts -p 'test_*.py' -v
python -m py_compile scripts/prepare_ctx_dem.py scripts/prepare_themis_grid.py scripts/prepare_hirise_patch.py scripts/render_route_figures.py
python scripts/test_browser_smoke.py
```

GitHub Actions runs the browser smoke against the hosted-style local page, including advanced budgets, RF estimates, THEMIS/HiRISE JSON loading and mobile controls. It requires the Three.js CDN.

## Scientific limits

- Tests use synthetic rasters and software contracts; no real CTX, THEMIS or HiRISE product raster has been imported.
- No ~87 MB CTX DEM, THEMIS mosaic or HiRISE DTM is bundled.
- Global terrain is about 215 m/cell; HiRISE is an independent local preview, not global pathfinding.
- The Minetti walking model is Earth-based; its 0.38-g adjustment is heuristic. Resource hours, terrain multipliers, task/rest time and RF parameters are hypothetical.
- RF is a single-hop free-space estimate plus geometric line of sight, not a validated network design.
- The accelerated warning clock is not a solar forecast, local radiation dose or health model.
- Browser smoke is not scientific, accessibility or mobile hardware certification. Manual testing remains necessary.
- GitHub Pages is only live after the repository owner enables Pages and a deployment succeeds.
