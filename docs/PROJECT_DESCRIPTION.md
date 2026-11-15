# WALKBACK: Can You Get Back in Time?

## Project summary

Human exploration of Mars requires more than selecting the shortest line on a map. A traverse must balance terrain, consumable resources, shelter access, communications and scientific value. WALKBACK is an interactive browser prototype for exploring those trade-offs around Jezero Crater.

The app embeds 698 NASA/JPL Mars 2020 Perseverance waypoint records spanning Sol 13–2022. It visualizes the rover traverse and a proposed route between selected science-stop anchors, a 3D terrain view, an elevation profile, slope screening and a modeled return-time surface. The walking-time proxy uses the Minetti Earth treadmill slope-cost polynomial with an explicitly heuristic 0.38-g sensitivity adjustment. It is not calibrated for suited Mars EVA.

The advanced panel now accepts independent user-editable time budgets for oxygen, electrical power, thermal control and CO₂ removal. The lowest budget is limiting; a reserve is applied, then science/setup time and breaks/rest are subtracted. Additional scenario controls represent pace, surface category and uncertainty. These are assumptions, not real suit capacities or measured Jezero trafficability values.

Two independent time constraints are shown in four states: both pass, resources only, warning window only, neither. A user-triggered demonstration clock accelerates one simulated minute per real second. It is not solar forecasting, radiation dose or crew-health modelling.

The communications panel combines geometric line of sight with an editable single-hop free-space link-margin approximation. It is not a validated network or hardware link budget.

## Multi-mission data workflows

The app's default embedded layer is the Mars 2020 / Perseverance traverse. Optional import pipelines are prepared for:
- MRO / CTX Jezero DEM: native source approximately 20 m/pixel, resampled to the current global app grid of approximately 215 m/cell.
- Mars Odyssey / THEMIS controlled mosaics: qualitative 8-bit visual overlay only, not temperature or radiance.
- MRO / HiRISE DTM: separate high-resolution local patch preview; it does not alter global pathfinding.

The real source rasters are not bundled or automatically loaded. Their exact product labels, projections, source metadata and coverage must be checked before processing. The current solver remains coarse.

## Route comparison

Straight-line connections between selected anchors and Perseverance odometer distances offer a geometric comparison only. They do not describe a validated human-walkable route or prove obstacle clearance.

## Current limitations

The default terrain outside the rover corridor is procedural until an optional CTX grid is imported. The 215 m global mesh cannot identify 1–5 m hazards. Surface factors are uniform assumptions, not a soil-mechanics model. There is no solar energy model, dust/weather forecast, particle spectrum, local radiation dose, shelter attenuation or radiation-health model. The RF model is simplified. There has been no independent EVA, geotechnical, radiation-protection or communications review. WALKBACK is not a certified astronaut-safety system.

## Team and participant protection

Public project materials identify the adult team member only and describe two additional team members as under 18. Their names and recognizable media are omitted from public materials. Follow the current official event terms for guardian registration and submission media.

## AI tools disclosure

ChatGPT (OpenAI) assisted with code review and correction, test writing, documentation, data-processing workflow preparation and presentation editing. The team must disclose any additional AI tools actually used and describe their actual contribution in the official form.

## Repository

https://github.com/valto-hash/walkback-mars