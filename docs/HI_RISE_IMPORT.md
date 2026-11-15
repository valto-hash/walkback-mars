# Local HiRISE DTM detail patches

The global WALKBACK mesh is 261 × 261 across 56 km, about 215 m per cell. It cannot preserve 1–5 m details. HiRISE products are therefore independent local detail patches, not upsampled into false global resolution.

USGS Jezero product catalog: https://astrogeology.usgs.gov/search/map/mars_2020_jezero_crater_landing_site_products.

## Projection and source checks

Select a DTM covering a specific science stop or short corridor. Inspect its PDS/USGS map label and reproject it to the same Mars equirectangular projected-metre convention used by WALKBACK: planetocentric latitude, positive-east longitude, radius 3,396,160 m. The processor samples a user-selected center in the app's local kilometre coordinates. The script does not infer or repair a mismatched planetary datum.

## Generate a local patch

For a 1 km square at 5 m samples centered on app coordinate (x,y) in kilometres:

```bash
python scripts/prepare_hirise_patch.py jezero_hirise_dtm_warped.tif data/processed/jezero_hirise_patch.json --center-x-km 0 --center-y-km 0 --size-m 1000 --pixel-size-m 5
```

The app coordinate (0,0) is the landing-site origin. Use the actual location of the feature being inspected. Maximum patch size is 501 × 501 cells.

Load the JSON under **Advanced planning → Load local HiRISE patch**. It appears in a separate elevation-shaded preview with its sample spacing. It does not modify the global grid or Dijkstra path solution, and is not a walking-hazard certification.

No actual HiRISE DTM was downloaded or loaded for this release.
