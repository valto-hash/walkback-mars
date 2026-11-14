#!/usr/bin/env python3
"""Sample the USGS MRO/CTX Jezero DEM onto WALKBACK's 261x261 grid.

The source uses a Mars equirectangular projection with planetocentric latitude,
positive-east longitude and the USGS catalog's spherical radius. Do NOT use
EPSG:4326 or an Earth geodetic transform for these planetary coordinates.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import rasterio

L0_LON_DEG = 77.4509
L0_LAT_DEG = 18.4446
APP_LOCAL_RADIUS_KM = 59.15
MARS_EQUIRECTANGULAR_RADIUS_M = 3_396_160.0
GRID_SIZE = 261
GRID_EXTENT_KM = 56.0
CTX_NATIVE_RESOLUTION_M = 20.0
SOURCE_URL = (
    "https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/"
    "ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif"
)
SOURCE_NAME = "Mars 2020 Science Investigation CTX DEM Mosaic, Jezero Crater (USGS / MRO CTX)"


def _valid_scalar(value: Any) -> bool:
    if value is None or np.ma.is_masked(value):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def mars_equirectangular_xy(longitude_east_deg: float, latitude_planetocentric_deg: float) -> tuple[float, float]:
    """Convert Mars east longitude / planetocentric latitude to metres.

    This is the equatorial equirectangular projection (lat_ts=0, lon_0=0)
    specified in the USGS product catalog. It is not terrestrial EPSG:4326.
    """
    lon = float(longitude_east_deg)
    lat = float(latitude_planetocentric_deg)
    if not (math.isfinite(lon) and math.isfinite(lat) and -90 <= lat <= 90):
        raise ValueError("Mars longitude/planetocentric latitude must be finite and latitude must be in [-90, 90].")
    return (
        MARS_EQUIRECTANGULAR_RADIUS_M * math.radians(lon),
        MARS_EQUIRECTANGULAR_RADIUS_M * math.radians(lat),
    )


def app_grid_mars_coordinates() -> tuple[list[float], list[float]]:
    """Return the app grid's Mars equirectangular X/Y coordinates in row-major order."""
    n = GRID_SIZE
    step_km = GRID_EXTENT_KM / (n - 1)
    x_values: list[float] = []
    y_values: list[float] = []
    for j in range(n):
        y_km = -GRID_EXTENT_KM / 2 + (n - 1 - j) * step_km
        lat = L0_LAT_DEG + y_km / APP_LOCAL_RADIUS_KM
        for i in range(n):
            x_km = -GRID_EXTENT_KM / 2 + i * step_km
            # Invert the app's local equirectangular lon/lat approximation exactly.
            lon = L0_LON_DEG + x_km / (APP_LOCAL_RADIUS_KM * math.cos(math.radians(lat)))
            x_m, y_m = mars_equirectangular_xy(lon, lat)
            x_values.append(x_m)
            y_values.append(y_m)
    return x_values, y_values


def sample_grid(
    dataset: rasterio.io.DatasetReader,
    native_resolution_m: float = CTX_NATIVE_RESOLUTION_M,
    minimum_valid_fraction: float = 0.98,
) -> dict[str, Any]:
    """Sample a Mars-equirectangular raster at the app's 261x261 vertices."""
    if dataset.count < 1:
        raise ValueError("Input DEM has no raster band.")
    if not (0.0 < minimum_valid_fraction <= 1.0):
        raise ValueError("minimum_valid_fraction must be in (0, 1].")
    if not math.isfinite(float(native_resolution_m)) or native_resolution_m <= 0:
        raise ValueError("Native resolution must be a positive finite number.")

    x_m, y_m = app_grid_mars_coordinates()
    sampled = list(dataset.sample(zip(x_m, y_m), indexes=1, masked=True))
    expected = GRID_SIZE * GRID_SIZE
    if len(sampled) != expected:
        raise RuntimeError("Raster sampler returned an unexpected number of cells.")

    values: list[float | None] = []
    for sample in sampled:
        scalar = sample[0]
        values.append(float(scalar) if _valid_scalar(scalar) else None)

    valid_count = sum(v is not None for v in values)
    valid_fraction = valid_count / len(values)
    if valid_fraction < minimum_valid_fraction:
        raise ValueError(
            f"Only {valid_fraction:.2%} of the app grid is covered by valid DEM cells; "
            f"at least {minimum_valid_fraction:.0%} is required. "
            "Check that the input is the USGS Mars equirectangular CTX product, not an Earth-georeferenced raster."
        )

    base_x, base_y = mars_equirectangular_xy(L0_LON_DEG, L0_LAT_DEG)
    base_sample = next(dataset.sample([(base_x, base_y)], indexes=1, masked=True))[0]
    if not _valid_scalar(base_sample):
        raise ValueError("The DEM has no valid elevation at the Perseverance landing/base reference point.")

    try:
        transform_text = str(dataset.transform)
        bounds = [float(v) for v in dataset.bounds]
        raster_crs = str(dataset.crs) if dataset.crs else "not embedded; interpreted using USGS Mars equirectangular metadata"
    except Exception:  # pragma: no cover - defensive metadata fallback
        transform_text, bounds, raster_crs = "unknown", [], "unknown"

    step_km = GRID_EXTENT_KM / (GRID_SIZE - 1)
    return {
        "schema": "walkback.dem-grid.v1",
        "source": SOURCE_NAME,
        "source_url": SOURCE_URL,
        "source_mission": "Mars Reconnaissance Orbiter (MRO)",
        "source_instrument": "Context Camera (CTX)",
        "native_resolution_m": float(native_resolution_m),
        "display_grid_spacing_m": step_km * 1000.0,
        "grid_spacing_km": step_km,
        "width": GRID_SIZE,
        "height": GRID_SIZE,
        "coordinate_reference": {
            "target": "Mars",
            "projection": "Equirectangular",
            "latitude_type": "Planetocentric",
            "longitude_direction": "Positive East",
            "longitude_domain": "-180 to 180 degrees",
            "mars_radius_m": MARS_EQUIRECTANGULAR_RADIUS_M,
            "app_origin_lon_deg": L0_LON_DEG,
            "app_origin_lat_deg": L0_LAT_DEG,
            "raster_crs_metadata": raster_crs,
            "raster_transform": transform_text,
            "raster_bounds_m": bounds,
        },
        "base_reference_m": float(base_sample),
        "valid_cell_fraction": valid_fraction,
        "nodata_cells": len(values) - valid_count,
        "values_m": values,
        "interpretation": (
            "Absolute DEM elevations in metres. Planetary coordinates were sampled in the USGS Mars "
            "equirectangular projection. Values are sampled to the app's ~215 m grid; native ~20 m "
            "pixels are not retained in the current solver mesh."
        ),
    }


def prepare(input_path: Path, output_path: Path, native_resolution_m: float = CTX_NATIVE_RESOLUTION_M) -> dict[str, Any]:
    with rasterio.open(input_path) as dataset:
        result = sample_grid(dataset, native_resolution_m=native_resolution_m)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, separators=(",", ":")), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="USGS MRO/CTX Jezero Mars-equirectangular DEM GeoTIFF (~20 m).")
    parser.add_argument("output", type=Path, nargs="?", default=Path("data/processed/jezero_ctx_dem_grid.json"))
    parser.add_argument("--native-resolution-m", type=float, default=CTX_NATIVE_RESOLUTION_M)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"Input raster not found: {args.input}")
    result = prepare(args.input, args.output, args.native_resolution_m)
    print(f"Wrote: {args.output}")
    print(f"Source: {result['source']}")
    print(f"Projection: Mars equirectangular / planetocentric latitude / positive-east longitude")
    print(f"Native resolution: {result['native_resolution_m']:.1f} m")
    print(f"App grid spacing: {result['display_grid_spacing_m']:.1f} m")
    print(f"Valid grid cells: {result['valid_cell_fraction']:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())