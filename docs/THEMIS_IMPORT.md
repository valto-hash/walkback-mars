# Importing a THEMIS visual grid

WALKBACK accepts `walkback.themis-visual-grid.v1` as a grayscale overlay. The importer labels it **qualitative-only**.

## Source and limits

Use the USGS Astrogeology THEMIS controlled mosaics documentation: https://stac.astrogeology.usgs.gov/docs/data/mars/themis_controlled_mosaics/. Controlled 8-bit mosaics are visual basemaps; their pixel values are not temperature, calibrated radiance or local radiation dose. For quantitative thermal work use individual calibrated products and their PDS labels.

## Projection

Read the exact PDS/USGS map label. Explicitly reproject the selected input to the same Mars equirectangular projected-metre coordinates used by `scripts/prepare_ctx_dem.py`: planetocentric latitude, positive-east longitude, radius 3,396,160 m. Do not merely assign a CRS and do not use Earth EPSG:4326. The script rejects missing CRS and insufficient Jezero coverage, but a metre-based CRS alone cannot prove the chosen planetary convention is correct.

## Process

```bash
python -m pip install -r scripts/requirements.txt
python scripts/prepare_themis_grid.py jezero_themis_warped.tif data/processed/jezero_themis_visual_grid.json --native-resolution-m 100
```

Load the resulting JSON from **Advanced planning → Load processed THEMIS grid**. It is a visual overlay only and does not feed route-time, resource or radiation calculations.

The JSON preserves source, mission, instrument, pixel size, CRS/transform and percentile stretch metadata, with `quantitative_use_allowed: false`. The repository does not bundle a THEMIS raster; none was downloaded or loaded for this release.
