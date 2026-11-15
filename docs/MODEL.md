# WALKBACK | Model, equations, assumptions and limitations

## 1. Purpose and status

WALKBACK is an exploratory browser prototype for comparing a hypothetical return-to-shelter time with two independent time limits: a user-configured life-support budget and a hypothetical warning window. It is not a certified EVA planner, radiation-protection system, RF design or astronaut-safety tool.

## 2. Grid and source data

The map/solver has 261 × 261 vertices over 56 km × 56 km:

`Δx = Δy = 56 / 260 = 0.21538 km ≈ 215 m`.

The 698 NASA/JPL Perseverance waypoint records (Sol 13–2022) are embedded by default. The default terrain outside the rover corridor is procedural. An optional MRO/CTX Jezero DEM importer samples the approximately 20 m/pixel USGS raster to the existing 215 m/cell grid; the raw GeoTIFF is not bundled and this is not native 20 m pathfinding. The imported CTX DEM must be inspected for projection, NoData and continuity before use.

THEMIS controlled mosaics can optionally be imported as a percentile-stretched visual grayscale overlay, strictly qualitative. The app rejects them as quantitative temperature data. HiRISE DTM data can be imported as an independent local preview patch, separate from global pathfinding. Neither raster product is currently bundled or active by default.

## 3. Slope screening and pathfinding

Slope is estimated by finite differences on the current terrain grid. The coarse screening bands are up to 10° (low), above 10° to 20° (moderate), above 20° to 30° (high) and above 30° (blocked). Dijkstra's eight-neighbour solver rejects blocked cells and diagonal moves that would cut corners through blocked neighbours. At ~215 m/cell this cannot detect metre-scale obstacles, loose regolith, boulders or local slope breaks.

## 4. Walking-time proxy

The app uses the Minetti-inspired signed-grade polynomial fitted to Earth treadmill walking measurements:

`C_E(i)=280.5i⁵−58.7i⁴−76.8i³+51.9i²+19.6i+2.5`

where grade `i` is clamped to [-0.45, 0.45]. The app applies a first-order Mars gravity sensitivity assumption:

`C_M(i)=C_E(0)+0.38 × [C_E(i)−C_E(0)]`

and estimates equivalent speed from the ratio of level-ground cost to grade cost. The 0.38 factor is a heuristic, not a calibration for suited Mars EVA. The default flat-ground speed is illustrative. Minetti et al. measured Earth walking, not suited astronauts in Martian gravity.

Each grid edge contributes distance divided by estimated return speed, with grade evaluated in the direction back toward shelter. The solver computes a modeled return-time surface. It does not model suit mass or mobility, human physiology, fatigue, metabolic limits, actual oxygen/cooling draw, sinkage, traction, obstacle negotiation or EVA procedures.

Reference: Minetti et al. (2002), Journal of Applied Physiology, https://doi.org/10.1152/japplphysiol.01177.2001.

## 5. Independent resource budget

The advanced panel accepts hours for oxygen, electrical power, thermal control and CO₂ removal. The lowest of these is the limiting resource. The app then applies the reserve factor and subtracts task/setup and rest/break overhead:

`T_usable = max(0, min(O₂, power, thermal, CO₂)/(1 + reserve/100) − tasks − rest)`

Default scenario: 4 h for each resource, 25% reserve, 0.25 h task/setup and 0.25 h rest. This gives 2.7 h usable modeled return time. Every number is an editable scenario value, not a suit capability or NASA hardware specification.

## 6. Terrain and uncertainty scenarios

Illustrative time multipliers are compact/smooth 1.00, mixed 1.20, rocky 1.35 and loose sand 1.55. An additional uncertainty percentage increases travel-time estimates. These uniform factors do not change the geometric shortest path and are not measured trafficability coefficients. They do not implement spatial classification, soil mechanics, dust adhesion, sinkage or slope stability.

## 7. Warning window and four classes

The warning interval is entered by the user. The demonstration clock advances one simulated minute per real second when started. It is a narrative control only; no solar forecast, particle spectrum, local radiation dose, shelter attenuation, shielding or crew-health model exists.

The map distinguishes: green = both resource and warning budgets pass; blue = resources only; orange = warning window only; red = neither. Only green passes both configured time limits. Unreachable cells remain distinct. The envelope radius is not a safe route length and is not a safety clearance.

## 8. Communications approximation

The advanced panel calculates a single-hop free-space link margin combined with the geometric line-of-sight screen:

`FSPL(dB)=32.44 + 20log10(frequency MHz) + 20log10(distance km)`

`margin = transmit power (dBm) + TX gain + RX gain − system losses − FSPL − receiver sensitivity`

The editable values are demonstration assumptions, not selected hardware. The estimate does not include diffraction, multipath, Mars plasma/atmosphere, antenna pattern or pointing, polarization, data rate, coding, regulatory allocation or a network of relays. It is not a communications guarantee.

## 9. Route metrics and mission scenario

The anchor-to-anchor human route is a proposed straight-line comparison to the Perseverance odometer. These geometric comparisons do not prove that a human route is walkable. The five-Sol exploration/return schedule and recovery of cached Three Forks sample tubes are hypothetical future scenarios, not an approved NASA crew mission.

## 10. Interpretation rule

Every display must be understood as one of: embedded mission record, imported source raster, derived estimate, or explicit user scenario. The current prototype supports exploratory comparison only. Real source rasters, independent EVA/geotechnical/radiation/RF review, browser and device validation, and a license decision remain outstanding.