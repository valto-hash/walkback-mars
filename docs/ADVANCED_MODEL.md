# Advanced planning assumptions and model limits

## Independent resource budgets

The advanced panel has separate user-editable hour budgets for oxygen, electrical power, thermal control and CO₂ removal. The minimum is the active bottleneck. The reserve is applied, then science/setup time and breaks/preparation time are subtracted:

`usable return hours = max(0, min(resource hours) / (1 + reserve %) - tasks - rest)`

Defaults are demonstration values only (4 h for each resource, 25% reserve, 0.25 h tasks and 0.25 h rest). They are not NASA suit capacities or flight hardware specifications.

## Terrain and uncertainty scenarios

Illustrative surface multipliers: compact 1.00, mixed regolith 1.20, rocky 1.35, loose sand 1.55. An additional uncertainty percentage increases computed travel time. These factors are scenario assumptions, not measured Jezero trafficability coefficients. They do not model foot sinkage, shear strength, dust, rock-size distribution, slope stability, suit mobility or human fatigue. The Minetti slope-cost polynomial is based on Earth measurements; its 0.38-g scaling remains a heuristic, not a validated Mars-EVA model.

A uniform multiplier makes all grid edges slower by the same ratio. It changes estimated travel time, not the geometric shortest path.

## Communications link budget

The app combines geometric line of sight with a single-hop free-space approximation:

`margin = EIRP + receiver gain - system losses - FSPL - receiver sensitivity`

`FSPL (dB) = 32.44 + 20 log10(frequency MHz) + 20 log10(distance km)`

Default values (400 MHz, 1 W, 3 dBi TX, 0 dBi RX, 2 dB losses, -110 dBm sensitivity, 6 dB required margin) are editable illustrative assumptions, not selected flight hardware. The result excludes diffraction, terrain reflection, multipath, polarization, pointing, data rate, coding, frequency allocation and relay topology. It is not a communications guarantee.

## Radiation

The accelerated warning clock is a user-operated narrative scenario. There is no live solar forecast, local surface dose, solar particle spectrum, shelter attenuation, suit shielding or health-effects calculation. Odyssey MARIE archives describe a mission radiation experiment; they do not provide a local Jezero surface-dose map. Do not describe the warning envelope as radiation protection or a measured forecast.

## Data importers

CTX remains optional; app resolution is ~215 m/cell. THEMIS controlled 8-bit mosaics can only be loaded as a visual overlay, not quantitative temperature. Calibrated products and PDS labels are required for thermal analysis. HiRISE is imported as a separate local patch so high-resolution detail is not misrepresented as a global DEM.
