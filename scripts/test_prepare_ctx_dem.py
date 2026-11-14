import math
import unittest

import numpy as np
from rasterio.io import MemoryFile
from rasterio.transform import from_origin

from prepare_ctx_dem import (
    APP_LOCAL_RADIUS_KM,
    MARS_EQUIRECTANGULAR_RADIUS_M,
    app_grid_mars_coordinates,
    mars_equirectangular_xy,
    sample_grid,
)


class PrepareCtxDemTests(unittest.TestCase):
    def _synthetic_mars_raster(self, *, origin_lon=76.75, origin_lat=19.2, pixel_m=50.0, size=1600):
        x0, y_top = mars_equirectangular_xy(origin_lon, origin_lat)
        transform = from_origin(x0, y_top, pixel_m, pixel_m)
        data = np.full((size, size), -2500.0, dtype=np.float32)
        mem = MemoryFile()
        ds = mem.open(
            driver="GTiff", height=size, width=size, count=1,
            dtype="float32", transform=transform, nodata=-9999.0,
        )
        ds.write(data, 1)
        return mem, ds

    def test_mars_equirectangular_projection_uses_planet_radius(self):
        x, y = mars_equirectangular_xy(90, 0)
        self.assertAlmostEqual(x, math.pi * MARS_EQUIRECTANGULAR_RADIUS_M / 2, places=6)
        self.assertEqual(y, 0)

    def test_app_grid_coordinates_match_the_local_projection(self):
        x, y = app_grid_mars_coordinates()
        self.assertEqual(len(x), 261 * 261)
        self.assertEqual(len(y), 261 * 261)
        center = 130 * 261 + 130
        expected = mars_equirectangular_xy(77.4509, 18.4446)
        self.assertAlmostEqual(x[center], expected[0], places=6)
        self.assertAlmostEqual(y[center], expected[1], places=6)
        self.assertAlmostEqual((x[130 * 261 + 260] - x[130 * 261]) / 56, (MARS_EQUIRECTANGULAR_RADIUS_M * math.pi / 180) / (APP_LOCAL_RADIUS_KM * math.cos(math.radians(18.4446))), delta=2)

    def test_sampling_creates_app_schema_from_mars_meter_coordinates(self):
        mem, ds = self._synthetic_mars_raster()
        try:
            result = sample_grid(ds, native_resolution_m=50.0)
        finally:
            ds.close()
            mem.close()
        self.assertEqual(result["schema"], "walkback.dem-grid.v1")
        self.assertEqual(result["width"], 261)
        self.assertEqual(result["height"], 261)
        self.assertEqual(len(result["values_m"]), 261 * 261)
        self.assertAlmostEqual(result["base_reference_m"], -2500.0)
        self.assertAlmostEqual(result["display_grid_spacing_m"], 215.384615, places=4)
        self.assertEqual(result["valid_cell_fraction"], 1.0)
        self.assertEqual(result["coordinate_reference"]["projection"], "Equirectangular")
        self.assertEqual(result["coordinate_reference"]["latitude_type"], "Planetocentric")

    def test_incomplete_mars_projection_coverage_is_rejected(self):
        mem, ds = self._synthetic_mars_raster(origin_lon=77.35, origin_lat=18.65, pixel_m=15.0, size=1000)
        try:
            with self.assertRaises(ValueError):
                sample_grid(ds)
        finally:
            ds.close()
            mem.close()


if __name__ == "__main__":
    unittest.main()