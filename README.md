# WALKBACK — Can You Get Back in Time?

**NASA Space Apps Challenge 2026 · Map of Mars**

WALKBACK is an interactive exploratory traverse-planning prototype for Jezero Crater. It asks whether a hypothetical explorer can return to a selected shelter within a user-configured life-support time budget and a second hypothetical warning window.

## Open the project

- [Interactive application](index.html)
- [Seven-slide English presentation](presentation.html)
- [Project description](docs/PROJECT_DESCRIPTION.md)
- [Model, equations and limitations](docs/MODEL.md)
- [Data inventory](docs/DATA.md)
- [Optional CTX DEM import](docs/DEM_IMPORT.md)
- [Credits and provenance](CREDITS.md)

The app is a static HTML page. It loads Three.js 0.128.0 and OrbitControls from jsDelivr, so a network connection is required to render the 3D scene.

## What is implemented

- 698 NASA/JPL Mars 2020 Perseverance waypoint records (Sol 13–2022) embedded in the application.
- 3D Jezero scene, rover traverse, proposed science-stop anchors and elevation profile.
- Four reachability states comparing the modeled return-time surface against independent resource and hypothetical warning-time budgets.
- User-triggered accelerated warning-window clock (1 simulated minute per real second) for storytelling; it is not a solar forecast or radiation-dose simulation.
- Minetti-inspired slope-cost proxy with an explicit, unvalidated 0.38-g sensitivity assumption.
- Coarse ~215 m slope screen, diagonal corner-cut prevention and geometric radio line of sight.
- Five-Sol hypothetical sampling scenario, first-person camera and four interface languages.
- Optional import of a processed MRO/CTX Jezero DEM grid. The raw ~87 MB GeoTIFF is **not** bundled and must be downloaded and processed separately. The processor uses Mars equirectangular coordinates, not Earth EPSG:4326.

## Important limitations

WALKBACK is a research prototype, **not a certified astronaut-safety or EVA-planning tool**. The default terrain is procedural outside the rover corridor. The optional native ~20 m CTX DEM is sampled onto the existing ~215 m app grid using the USGS Mars equirectangular/planetocentric reference, so local foot-scale hazards remain unresolved. The Minetti-derived gravity sensitivity is a hypothesis, not a calibrated Mars-suit walking model. Soil strength/trafficability, solar power, local radiation dose, live solar-weather forecasts, shelter attenuation and complete RF link budgets are not modeled. Read [docs/MODEL.md](docs/MODEL.md) before interpreting the envelopes.

## NASA data

- Embedded by default: [NASA/JPL Mars 2020 Perseverance waypoints](https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json).
- Optional source: [USGS / MRO CTX Jezero DEM mosaic](https://astrogeology.usgs.gov/search/map/mars_2020_science_investigation_ctx_dem_mosaic), with a reproducible processor in [`scripts/prepare_ctx_dem.py`](scripts/prepare_ctx_dem.py).
- THEMIS, CRISM, HiRISE and other sources are reference-only unless specifically recorded as loaded layers in the app and manifest.

## Rebuild the presentation figures

The route and elevation SVGs are reproducible from the 698 waypoint records embedded in the app: `python scripts/render_route_figures.py`.

## Run locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000` in a modern browser.

## Tests

```bash
npm test
cd scripts
python -m unittest test_prepare_ctx_dem.py -v
```

See [docs/VALIDATION.md](docs/VALIDATION.md) for what these tests do and do not establish.

## Team

- **Guilherme Albernaz Martins Costa** — adult team member.
- **Two additional team members under 18** — names omitted from these public materials in accordance with the NASA Space Apps 2026 Participant Terms.

The full registered team roster belongs in the official event registration system. Follow all guardian and participant requirements there.

## AI tools disclosure

ChatGPT (OpenAI) assisted with code review/correction, tests, documentation, the CTX processing workflow and presentation editing. The team must disclose any other AI tools actually used and describe their real contribution in the official form.

## License

No license has yet been selected for the team's original source code. See [docs/LICENSE_DECISION_REQUIRED.md](docs/LICENSE_DECISION_REQUIRED.md). Do not assume the MIT license of Three.js applies to WALKBACK.