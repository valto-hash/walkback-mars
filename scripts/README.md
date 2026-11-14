# WALKBACK data and figure scripts

## Prepare the optional USGS MRO / CTX DEM

The original GeoTIFF is about 87 MB and is not stored in Git. Download it from:

https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif

Install dependencies:

```bash
python -m pip install -r scripts/requirements.txt
```

Run the processor:

```bash
python scripts/prepare_ctx_dem.py M20_JezeroCrater_CTXDEM_20m.tif data/processed/jezero_ctx_dem_grid.json
```

**Planetary CRS warning:** the product is Mars equirectangular, planetocentric latitude and positive-east longitude, with a 3,396,160 m radius. The processor computes Mars projected metre coordinates directly. It does not use terrestrial `EPSG:4326` transformations.

The original CTX raster has about 20 m pixels. It is sampled onto the app's 261 × 261 grid over 56 km, about 215 m per cell. The solver therefore does not preserve native 20 m detail and cannot screen 1–5 m foot-scale hazards.

## Rebuild presentation figures

The route and elevation SVGs are generated from the 698 waypoint records embedded in `index.html`:

```bash
python scripts/render_route_figures.py
```

The figures show the rover waypoint traverse, selected anchor-to-anchor straight connections and elevation against odometer distance. They are not topographic basemaps or human-safe route certifications.