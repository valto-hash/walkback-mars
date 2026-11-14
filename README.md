# WALKBACK — Can You Get Back in Time?

**NASA Space Apps Challenge 2026 · Map of Mars**

WALKBACK is an interactive browser prototype for exploring human surface traverses around Jezero Crater. Its central question is simple: can an explorer return to a safe point before life-support resources or a configurable warning window run out?

## Try the project

- **Interactive application:** open [index.html](index.html) or visit the GitHub Pages site after deployment: `https://valto-hash.github.io/walkback-mars/`.
- **Seven-slide presentation (English):** [presentation.html](presentation.html).
- **Project description:** [docs/PROJECT_DESCRIPTION.md](docs/PROJECT_DESCRIPTION.md).
- **Model and assumptions:** [docs/MODEL.md](docs/MODEL.md).
- **Data inventory:** [docs/DATA.md](docs/DATA.md).
- **Credits and provenance:** [CREDITS.md](CREDITS.md).

## What is implemented

- 698 NASA/JPL Mars 2020 Perseverance waypoint records (Sol 13–2022) embedded in the application.
- A 3D Jezero scene with the rover traverse and a proposed route between selected science stops.
- Two configurable reachability envelopes: a blue consumables-based walk-back estimate and a green shelter-reach estimate based on a user-selected warning interval.
- A derived terrain grid for slope and path-time exploration.
- Radio line-of-sight calculation using assumed antenna heights.
- First-person exploration, seven stop descriptions, route/elevation summaries, and Portuguese, English, Spanish and German interface text.

## Scientific scope and limitations

This is an exploratory planning prototype, **not a certified astronaut-safety tool**. The terrain outside the rover traverse corridor is procedural; slope is calculated on an approximately 200 m grid; the Tobler-based walking model is not adjusted for Mars gravity (0.38 g); and the current app does not integrate validated suit limits, soil strength/trafficability, solar-energy, measured local radiation-dose or live solar-weather datasets. The green envelope is not a storm forecast or radiation-dose simulation. The straight-line human route is proposed geometry, not a validated human-walkable path.

Read [the model notes](docs/MODEL.md), [data provenance](docs/DATA.md), and [credits](CREDITS.md) before interpreting results.

## NASA data

The primary embedded NASA source is the NASA/JPL Mars 2020 Perseverance waypoint dataset:
https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json

Other resources in the documentation are marked as reference-only or future integration sources. They are not represented as live data layers in the current prototype.

## Team

- **Guilherme Albernaz Martins Costa** — adult team member.
- **Two additional team members under 18** — names intentionally omitted from this public repository and public submission materials in accordance with the NASA Space Apps 2026 participant terms.

The complete registration details belong in the official event system, subject to the event's rules. Do not add identifiable names, voices or likenesses of under-18 participants to public submission materials.

## AI tools disclosure

ChatGPT (OpenAI) assisted with organizing and editing project documentation, the presentation narrative and submission-support text. The team must disclose any other AI tools actually used and accurately describe each tool's contribution in the official submission.

## Run locally

The application is a single static HTML file. It loads Three.js 0.128.0 and OrbitControls from jsDelivr, so an internet connection is required for those libraries.

```bash
python -m http.server 8000
```

Then open `http://localhost:8000` in a modern browser.

## License

No license has been selected for the team's original source code yet. See [docs/LICENSE_DECISION_REQUIRED.md](docs/LICENSE_DECISION_REQUIRED.md). Do not assume that Three.js's MIT license applies to WALKBACK.
