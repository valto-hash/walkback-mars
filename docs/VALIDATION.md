# WALKBACK | Validation report

## Automated checks run in the local working copy

### JavaScript model contract

Command:

```bash
npm test
```

Result: **13 tests passed**. The suite parses the full inline app JavaScript and tests:

1. usable support-time budget and reserve margin;
2. Minetti polynomial at known grades and clamping to its stated range;
3. explicit 0.38-g slope-cost sensitivity, level-speed normalization and uphill/downhill direction;
4. independent resource/warning reachability classes;
5. slope-screen boundaries;
6. slope blocking and no diagonal corner cutting through a blocked cell;
7. HUD colors for all four classes and unreachable cells;
8. invalid values fail loudly;
9. DEM JSON schema, base-reference and NoData validation (null is not converted to zero elevation);
10. visible labeling that the warning is hypothetical and the CTX DEM is optional/imported, not bundled;
11. runtime execution of the language/DEM-control initialization path (catches reference-order errors);
12. presence of a user-triggered, explicitly accelerated hypothetical warning-window clock;
13. runtime behavior of the countdown (advance, pause and reset).

### DEM processing pipeline

Command:

```bash
cd scripts
python -m unittest test_prepare_ctx_dem.py -v
```

Result: **4 synthetic-GeoTIFF/projection tests passed**. These verify the Mars equirectangular coordinate conversion, 261 × 261 sampling on a synthetic planetary-metre raster, landing-site reference lookup and rejection of incomplete Mars-projection coverage. They do not verify the actual 87 MB USGS source file.

## Not completed / not validated

- The actual CTX GeoTIFF could not be downloaded into this build environment; the pipeline and browser importer are ready, but no real CTX JSON grid is bundled or loaded by default.
- No browser/WebGL end-to-end test was completed in this environment.
- No independent validation by EVA specialists, geologists, radiation-protection experts or mission engineers has been performed.
- The Minetti-based 0.38-g adjustment is an explicit sensitivity assumption and has not been calibrated for suited human locomotion.
- The app solver remains ~215 m/cell; the pipeline does not retain native 20 m data in the solver.
- No validation of soil trafficability, solar energy, radiation dose, shelter attenuation, RF link margin or rescue response has been performed.
- Mobile and desktop GPU performance has not been benchmarked.

These tests verify code contracts and the synthetic data pipeline only. They do not certify the physical model or any route for human EVA.