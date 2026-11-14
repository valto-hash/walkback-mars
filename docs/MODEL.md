# WALKBACK | Model, equations, assumptions and limitations

## 1. Purpose

WALKBACK is an exploratory browser prototype. It compares a modeled return-time surface from a selected shelter anchor with two independent time budgets:

1. **Usable life-support return-time budget**, calculated from a user-entered remaining-support time and reserve margin.
2. **Hypothetical warning window**, entered by the user in minutes.

The map uses four mutually exclusive classes. Only the green class passes both configured budgets. This is not a mission go/no-go system and is not certified for EVA planning.

## 2. Terrain grid and source data

The scene and solver grid contain 261 × 261 vertices over 56 km × 56 km:

\[
\Delta x=\Delta y=\frac{56}{260}=0.21538\;\mathrm{km}\approx215\;\mathrm{m}.
\]

The default terrain is procedural, locally corrected along the Perseverance traverse using NASA/JPL waypoint elevations. It is not a continuous orbital digital elevation model.

An optional import is now available for the **USGS / Mars Reconnaissance Orbiter (MRO) Context Camera (CTX) Jezero DEM mosaic**, whose source product is approximately 20 m/pixel and covers the crater. The raw GeoTIFF is not stored in this repository. `scripts/prepare_ctx_dem.py` samples it onto the app's existing 261 × 261 grid, then the user loads the resulting JSON with the app's “Load processed CTX DEM” control. This is a sample/resampling step: the app solver still operates at approximately 215 m per cell, not at the DEM's native 20 m resolution. It therefore still cannot assess 1–5 m foot-scale hazards.

Source product: [USGS Astropedia, Mars 2020 Science Investigation CTX DEM Mosaic](https://astrogeology.usgs.gov/search/map/mars_2020_science_investigation_ctx_dem_mosaic). USGS metadata specify Mars equirectangular projection, planetocentric latitude, positive-east longitude and a 3,396,160 m radius; it marks the product public domain and requests author citation. Direct GeoTIFF: [M20_JezeroCrater_CTXDEM_20m.tif](https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif). The catalog identifies MRO and CTX and gives an external file size of about 87 MB. The import workflow records native resolution separately from the app grid.

## 3. Slope screening

Slope is estimated by finite differences on the current terrain grid:

\[
\theta=\arctan\left(\sqrt{(\partial z/\partial x)^2+(\partial z/\partial y)^2}\right).
\]

The on-screen screening bands follow the initial project brief:

- up to 10°: low;
- above 10° through 20°: moderate;
- above 20° through 30°: high;
- above 30°: blocked in the coarse solver.

The solver rejects diagonal moves that would cut a corner through a blocked adjacent cell. The >30° screen is only a preliminary filter at roughly 215 m spacing. It does not rule out steep local obstacles, cliffs, boulders, loose sand or hazardous rock surfaces inside a cell.

## 4. Walking-time cost proxy

The earlier Tobler-only approximation has been replaced with a **Minetti-inspired slope-cost proxy**. Minetti et al. measured walking and running energy cost on a treadmill over signed gradients from −0.45 to +0.45 and fit a fifth-order polynomial to the walking-cost data. The polynomial used by the app is:

\[
C_E(i)=280.5i^5-58.7i^4-76.8i^3+51.9i^2+19.6i+2.5,
\]

where \(i\) is signed grade (rise/run) and the input is clamped to the studied interval \([-0.45,0.45]\). The function is based on Earth measurements; it is not a Mars suit model. See [Minetti et al. (2002), Journal of Applied Physiology](https://doi.org/10.1152/japplphysiol.01177.2001).

The application uses an explicitly **heuristic, first-order gravity-sensitivity scenario**:

\[
C_M(i)=C_E(0)+0.38\,[C_E(i)-C_E(0)]
\]

and converts the relative cost into an equivalent-time speed proxy:

\[
v_{eq}(i)=\max\left(0.15,\;v_{flat}\frac{C_E(0)}{C_M(i)}\right)\quad\mathrm{km/h}.
\]

The value 0.38 is the Mars-to-Earth surface-gravity ratio used by the project. Only the *slope-related difference from level-ground cost* is scaled by this factor; the configured level-ground reference is kept unchanged. This is an engineering sensitivity assumption, not a relationship established by Minetti or a validated conversion from metabolic cost to walking speed under Martian gravity.

Cavagna et al. studied human walking under simulated 0.4 g and reported a lower external-work minimum at a slower speed than at 1 g (about 2.5 km/h versus 4.5 km/h for the reported external-work measure). This supports treating low gravity as relevant, but it does **not** calibrate the Minetti slope polynomial for Mars, nor does it represent suited EVA locomotion. The app's default flat-ground reference of 2.5 km/h is therefore only an illustrative starting value. See [Cavagna et al. (2000), Journal of Physiology](https://doi.org/10.1111/j.1469-7793.2000.00657.x).

For a grid edge of length \(L\) km, the modeled time increment is \(\Delta t=L/v_{eq}(i)\) hours. Dijkstra's algorithm propagates the modeled return time from the selected shelter over an eight-neighbour grid. The grade is computed in the direction of travel **back toward the shelter**. The user-adjustable flat-ground speed, consumable time and reserve remain illustrative inputs.

This proxy does not model suit mass/mobility, body mass, individual physiology, fatigue, oxygen and cooling-system consumption, metabolic power limits, terrain traction, obstacle negotiation, actual astronaut gait, or EVA protocols. It must not be described as a validated Mars walking model.

## 5. Life-support return budget

The remaining support-time input and reserve margin produce the usable modeled return-time budget:

\[
T_{resources}=\frac{T_{remaining}}{1+m/100}.
\]

Default demonstration values are 4.0 h remaining support time and a 25% reserve, yielding 3.2 h usable modeled return time. The app now displays the entered support time and the derived usable budget separately. These values are not real suit specifications.

## 6. Hypothetical warning window

The user enters a warning interval in minutes:

\[
T_{window}=\frac{\mathrm{warning\ minutes}}{60}.
\]

The default is 45 minutes (0.75 h). It is a scenario input only. The app provides a user-triggered demonstration clock that advances **one simulated minute per real second** and recomputes the warning-window classification as the clock runs. This acceleration is a storytelling device; it is not a model of solar-event dynamics or mission time. The app has no live solar-event feed, solar-storm forecast, particle spectrum, local dose-rate model, shielding model, shelter attenuation model or radiation-dose budget.

## 7. Four reachability classes

For modeled return time \(t\) at a grid cell:

| State | Condition | Map color | Meaning |
|---|---|---|---|
| Both pass | \(t\le T_{resources}\) and \(t\le T_{window}\) | Green | Both configured budgets pass |
| Resources only | \(t\le T_{resources}\) and \(t>T_{window}\) | Blue | Resource budget passes; warning window fails |
| Warning only | \(t>T_{resources}\) and \(t\le T_{window}\) | Orange | Warning window passes; resource budget fails |
| Neither | \(t>T_{resources}\) and \(t>T_{window}\) | Red | Both budgets fail |

Cells with no computed route are marked unreachable. Only green satisfies both time constraints. The displayed envelope radius is the largest straight-line distance from the anchor to any cell in that class; it is not a route length and does not imply every point at that radius is reachable.

## 8. Radio line of sight

The geometric viewshed assumes a 10 m mast at the shelter and a 2 m explorer antenna. It includes a simplified Mars-curvature term using a 3,389.5 km radius. It is not a radio link budget and does not model frequency, transmit power, antenna pattern/gain, terrain-reflection, atmospheric losses, interference, relay orbits, link margin or actual hardware.

## 9. Route comparison metrics

The app associates seven selected science-stop anchors with nearby Perseverance waypoint Sols (13, 648, 940, 1219, 1250, 1299 and 1354). It compares straight-line connections between those anchors with the rover odometer between the corresponding waypoints.

Approximate values from the embedded NASA/JPL records:

- **12.2 km**: sum of straight-line segments between selected anchors;
- **32.3 km**: Perseverance odometer distance between the corresponding anchors;
- **+784 m**: sum of positive elevation changes between successive selected anchors.

The +784 m value is the sum of positive elevation differences between the selected anchors only; it is not cumulative ascent over every intermediate rover waypoint. The straight-line route is not a terrain-following, obstacle-avoiding human route and has not been validated for human walking.

## 10. Five-Sol scenario

The proposal has five Sols: Sol 1 base and delta; Sol 2 Margin Unit; Sol 3 Cheyava Falls and Serpentine Rapids; Sol 4 Pico Turquino and Witch Hazel Hill; Sol 5 return to base without sampling. The app's simulation contains eight entries including the return stage. Instruments, durations, sample counts and masses are proposed scenario assumptions, not deployed hardware or an approved NASA crew mission. Recovery of the 10 cached Three Forks sample tubes by a future crew is hypothetical, not an approved mission plan.

## 11. Known gaps that remain

- The raw CTX GeoTIFF has not been bundled or loaded automatically; the optional pipeline/importer is ready, but the user must download and process the source file.
- The solver grid remains ~215 m, too coarse for the 1–5 m human-scale terrain target.
- The terrain is procedural unless the optional CTX grid is loaded; even then, it is resampled to the coarse app grid.
- Additional mineralogy/geology/thermal layers (for example CRISM, HiRISE, THEMIS and USGS geologic maps) are not currently integrated as active map layers.
- Soil strength, grain size, cohesion, sand traps, loose regolith, rock abundance and sharp-rock hazards are not modeled.
- Solar illumination, seasonal shadows, dust opacity and solar energy/storage are not modeled.
- There is no solar-storm forecast, dose-rate model, location-specific radiation dose or shelter attenuation model.
- The gravity-sensitive walking-cost proxy is not validated against suited human movement at 0.38 g.
- There is no full RF link budget or relay-network analysis.
- No independent review by EVA, geotechnical, radiation-protection or mission-design specialists has been completed.

WALKBACK remains a research prototype. It must not be used to authorize or plan a real EVA.