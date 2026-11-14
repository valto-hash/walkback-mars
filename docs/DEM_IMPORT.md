# Optional MRO / CTX terrain import

The app supports importing a compact JSON grid sampled from the USGS Astrogeology Jezero Context Camera DEM mosaic.

## 1. Download the source GeoTIFF

USGS product page: https://astrogeology.usgs.gov/search/map/mars_2020_science_investigation_ctx_dem_mosaic

Direct download (~87 MB):

`https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif`

Save it locally; do not commit the raw TIFF to Git.

## 2. Process it

```bash
python -m pip install -r scripts/requirements.txt
python scripts/prepare_ctx_dem.py M20_JezeroCrater_CTXDEM_20m.tif data/processed/jezero_ctx_dem_grid.json
```

The processor uses the coordinate reference documented by USGS for this Mars product: **equirectangular projection, planetocentric latitude, positive-east longitude, spherical radius 3,396,160 m**. It converts the app grid directly into those Mars projected metre coordinates. It deliberately does not treat Mars longitude/latitude as Earth EPSG:4326 or run a terrestrial geodetic transform. The processor samples 261 × 261 values, checks coverage and the landing-site base sample, records the coordinate metadata and emits schema `walkback.dem-grid.v1`.

## 3. Load it in the app

Open `index.html`, choose **Load processed CTX DEM (JSON)** and select `data/processed/jezero_ctx_dem_grid.json`. The status message reports the source resolution and the app's current grid spacing. **Reset terrain** restores the waypoint-corrected procedural baseline.

## Resolution and caveats

The USGS source is approximately 20 m/pixel. The existing app mesh and solver grid are 261 × 261 over 56 km, approximately 215 m per cell. The processor samples the source down to that grid; it does not retain native 20 m terrain detail. This improves the elevation source but is not a 1–5 m foot-scale obstacle model and is not proof of route safety. The real source GeoTIFF was not bundled with this repository; importing it remains a manual step.