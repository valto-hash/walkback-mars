# WALKBACK data and figure scripts

## Dependencies

```bash
python -m pip install -r scripts/requirements.txt
```

## Optional USGS MRO / CTX DEM

The source GeoTIFF is about 87 MB and is not stored in Git. Download it from:

https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif

```bash
python scripts/prepare_ctx_dem.py M20_JezeroCrater_CTXDEM_20m.tif data/processed/jezero_ctx_dem_grid.json
```

The source product is approximately 20 m/pixel. WALKBACK samples it to a 261 × 261 grid over 56 km, about 215 m/cell. The processor uses Mars equirectangular, planetocentric latitude, positive-east longitude and radius 3,396,160 m. It does not use terrestrial EPSG:4326.

## Optional Mars Odyssey / THEMIS visual overlay

Choose a controlled mosaic, inspect its exact PDS/USGS map label, and explicitly reproject the raster to the WALKBACK-compatible Mars equirectangular projected-metre grid. Never merely assign a CRS. Then:

```bash
python scripts/prepare_themis_grid.py THEMIS_warped_to_WALKBACK.tif data/processed/jezero_themis_visual_grid.json --native-resolution-m 100
```

The output is a qualitative 8-bit grayscale visual layer only. It is not temperature, calibrated radiance or radiation dose.

## Optional MRO / HiRISE local DTM patch

Inspect the selected product's map label and explicitly reproject to the same Mars projected-metre convention. Select a local application coordinate in kilometres:

```bash
python scripts/prepare_hirise_patch.py HiRISE_DTM_warped_to_WALKBACK.tif data/processed/jezero_hirise_patch.json --center-x-km 0 --center-y-km 0 --size-m 1000 --pixel-size-m 5
```

This creates a local preview, independent from the 215 m global path solver. The script limits the output to 501 × 501 cells.

## Rebuild figures

```bash
python scripts/render_route_figures.py
```

The route and elevation SVGs are generated from embedded NASA/JPL waypoints. They are not topographic basemaps or human-safe route certifications.
