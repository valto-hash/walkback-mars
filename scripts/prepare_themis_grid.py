#!/usr/bin/env python3
"""Convert an already-warped THEMIS raster to a qualitative WALKBACK grid.

Inspect the exact PDS/USGS map label and warp explicitly to the app's Mars
planetocentric, positive-east equirectangular metres. This script does not guess
or repair source map projections. Output is a visual 8-bit stretch only.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from typing import Any
import numpy as np
import rasterio
from prepare_ctx_dem import app_grid_mars_coordinates

GRID_SIZE=261
SCHEMA="walkback.themis-visual-grid.v1"
SOURCE_URL="https://stac.astrogeology.usgs.gov/docs/data/mars/themis_controlled_mosaics/"

def _valid(v: Any) -> bool:
    try: return v is not None and not np.ma.is_masked(v) and math.isfinite(float(v))
    except (TypeError, ValueError): return False

def sample_grid(dataset, native_resolution_m: float=100.0, minimum_valid_fraction: float=.98):
    if dataset.count<1: raise ValueError("Input raster has no bands.")
    if dataset.crs is None: raise ValueError("Input must have an explicit Mars map projection.")
    if not 0<minimum_valid_fraction<=1: raise ValueError("minimum_valid_fraction must be in (0,1].")
    if not math.isfinite(native_resolution_m) or native_resolution_m<=0: raise ValueError("Native resolution must be positive.")
    units=str(dataset.crs.linear_units or "")
    if "metre" not in units.lower() and "meter" not in units.lower():
        raise ValueError(f"Expected a projected Mars CRS in metres; got {units!r}.")
    xs,ys=app_grid_mars_coordinates()
    vals=[]
    for item in dataset.sample(zip(xs,ys),indexes=1,masked=True):
        v=item[0]; vals.append(float(v) if _valid(v) else None)
    good=np.asarray([v for v in vals if v is not None],dtype=np.float64)
    fraction=len(good)/(GRID_SIZE*GRID_SIZE)
    if fraction<minimum_valid_fraction: raise ValueError(f"Only {fraction:.2%} valid cells; verify Mars projection and Jezero coverage.")
    lo,hi=np.percentile(good,[2,98])
    gray=[127 if v is not None else None for v in vals] if hi<=lo else [
        int(round(np.clip((v-lo)/(hi-lo),0,1)*255)) if v is not None else None for v in vals]
    return {
      "schema":SCHEMA,"source":"Operator-supplied Mars Odyssey THEMIS controlled mosaic","source_url":SOURCE_URL,
      "source_mission":"Mars Odyssey","source_instrument":"THEMIS","native_resolution_m":float(native_resolution_m),
      "width":GRID_SIZE,"height":GRID_SIZE,"grid_spacing_m":56000/260,
      "coordinate_reference":"Mars equirectangular projected metres; source label and reprojection must be verified by operator",
      "raster_crs":dataset.crs.to_string(),"raster_transform":str(dataset.transform),"valid_cell_fraction":fraction,
      "normalization":{"method":"2nd to 98th percentile linear visual stretch","low_source_value":float(lo),"high_source_value":float(hi)},
      "values_8bit":gray,"interpretation":"qualitative_only_not_temperature","quantitative_use_allowed":False,
      "warning":"Display-only grayscale, not temperature, calibrated radiance or radiation dose."
    }

def prepare(input_path:Path,output_path:Path,native_resolution_m:float=100):
    with rasterio.open(input_path) as ds: result=sample_grid(ds,native_resolution_m)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.write_text(json.dumps(result,separators=(",",":")),encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("input",type=Path);p.add_argument("output",type=Path,nargs="?",default=Path("data/processed/jezero_themis_visual_grid.json"))
    p.add_argument("--native-resolution-m",type=float,default=100)
    a=p.parse_args()
    if not a.input.is_file():p.error(f"Input raster not found: {a.input}")
    r=prepare(a.input,a.output,a.native_resolution_m)
    print(f"Wrote {a.output}; coverage={r['valid_cell_fraction']:.2%}; qualitative visual layer only")
    return 0
if __name__=="__main__":raise SystemExit(main())
