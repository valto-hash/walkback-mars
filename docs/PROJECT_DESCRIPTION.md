# WALKBACK: Can You Get Back in Time?

## Project summary

Human exploration of Mars requires more than choosing the shortest path. A field traverse must balance terrain, life-support limits, shelter access, communications and scientific value. WALKBACK is an interactive browser prototype for exploring these decisions around Jezero Crater.

The prototype embeds 698 NASA/JPL Mars 2020 Perseverance waypoint records spanning Sol 13 to Sol 2022. The records provide rover positions, elevation and odometer values. WALKBACK displays the rover traverse and a proposed route connecting selected sites of scientific interest. It computes two configurable reachability envelopes on a derived terrain grid: a blue walk-back envelope constrained by user-entered consumable time, flat-ground speed and safety margin; and a green shelter-reach envelope constrained by a selected warning interval. The browser also computes a radio line-of-sight layer using an assumed 10 m shelter mast and a 2 m suit antenna. Users can explore the 3D scene in first-person mode, inspect seven proposed science stops, and switch among Portuguese, English, Spanish and German.

Between the selected site anchors, the proposed straight-line route is about 12.2 km. The Perseverance odometer records about 32.3 km across the same traverse segments, including science-driven rover detours. The selected legs add approximately 784 m of positive elevation gain. These are route-comparison metrics, not proof that the proposed line is human-walkable.

## Current limitations

The terrain outside the rover traverse corridor is procedural rather than a real digital elevation model. The slope calculation uses a grid of approximately 200 m, not the 1–5 m human-scale resolution proposed in the project brief. The Tobler-based walking-time model has not been adjusted for Mars gravity (0.38 g). The current prototype does not integrate soil-strength/trafficability, solar-energy, measured local radiation-dose or live solar-weather layers. The green envelope uses a configurable warning interval; it is not a live solar-storm forecast or a radiation-dose simulation. WALKBACK is an exploratory planning prototype, not a certified safety system.

## NASA data used

The primary embedded NASA source is the NASA/JPL Mars 2020 Perseverance waypoint dataset: https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json. The NASA Mars 2020 raw-image archive is linked from stop descriptions but is not downloaded or embedded in the app. Mars Trek, USGS Astrogeology maps, the Curiosity Proposed Path resource and NASA Worldview are reference links or future integration sources, not currently integrated data layers.

## Team

Guilherme Albernaz Martins Costa is the adult team member. Two additional team members are under 18; their names are intentionally omitted from this public project description in accordance with the NASA Space Apps 2026 Participant Terms. The full event registration must follow the event's official participant requirements.

## AI tools disclosure

ChatGPT (OpenAI) assisted with organizing and writing the presentation and accompanying submission-support text. The route figures and plotted visuals were derived from waypoint data embedded in the supplied application. The team must add any other AI tools used by team members and describe their actual roles in the official submission form.

## Project link

https://github.com/valto-hash/walkback-mars
