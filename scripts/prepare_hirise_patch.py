#!/usr/bin/env python3
"""Extract a local HiRISE DTM detail patch, separate from global pathfinding."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from typing import Any
import numpy as np
import rasterio
from prepare_ctx_dem import L0_LON_DEG,L0_LAT_DEG,APP_LOCAL_RADIUS_KM,mars_equirectangular_xy

SCHEMA="walkback.hirise-patch.v1"

def local_to_mars_xy(x_km:float,y_km:float):
    lat=L0_LAT_DEG+y_km/APP_LOCAL_RADIUS_KM
    lon=L0_LON_DEG+x_km/(APP_LOCAL_RADIUS_KM*math.cos(math.radians(lat)))
    return mars_equirectangular_xy(lon,lat)

def _valid(v:Any):
    try:return v is not None and not np.ma.is_masked(v) and math.isfinite(float(v))
    except (TypeError,ValueError):return False

def sample_patch(dataset,center_x_km:float,center_y_km:float,size_m:float=1000,pixel_size_m:float=5,minimum_valid_fraction:float=.98):
    if dataset.count<1:raise ValueError("Input DTM has no raster band.")
    if dataset.crs is None:raise ValueError("Input must have an explicit Mars projected CRS.")
    if not all(math.isfinite(float(v)) for v in (center_x_km,center_y_km,size_m,pixel_size_m)) or size_m<=0 or pixel_size_m<=0:raise ValueError("Center, size and spacing must be finite; size and spacing positive.")
    if size_m/pixel_size_m>500:raise ValueError("Patch exceeds 501 × 501 cells; use a smaller patch or coarser spacing.")
    n=int(round(size_m/pixel_size_m))+1;actual=(n-1)*pixel_size_m
    coords=[]
    for j in range(n):
      y=center_y_km+actual/2000-j*pixel_size_m/1000
      for i in range(n):
        x=center_x_km-actual/2000+i*pixel_size_m/1000
        coords.append(local_to_mars_xy(x,y))
    vals=[]
    for item in dataset.sample(coords,indexes=1,masked=True):
      v=item[0];vals.append(float(v) if _valid(v) else None)
    valid=[v for v in vals if v is not None];fraction=len(valid)/len(vals)
    if fraction<minimum_valid_fraction:raise ValueError(f"Patch has only {fraction:.2%} valid cells; verify source projection and coverage.")
    elev=np.asarray(valid,dtype=np.float64)
    return {"schema":SCHEMA,"source":"Operator-supplied HiRISE DTM","source_mission":"Mars Reconnaissance Orbiter","source_instrument":"HiRISE",
      "native_pixel_size_m":float(pixel_size_m),"width":n,"height":n,"actual_size_m":float(actual),
      "center_app_local_x_km":float(center_x_km),"center_app_local_y_km":float(center_y_km),"valid_cell_fraction":fraction,
      "raster_crs":dataset.crs.to_string(),"raster_transform":str(dataset.transform),"minimum_elevation_m":float(elev.min()),
      "maximum_elevation_m":float(elev.max()),"values_m":vals,
      "use":"Independent local high-resolution detail view only. Not part of the global solver grid and not a safety certification."}

def prepare(input_path:Path,output_path:Path,center_x_km:float,center_y_km:float,size_m:float=1000,pixel_size_m:float=5):
    with rasterio.open(input_path) as ds:r=sample_patch(ds,center_x_km,center_y_km,size_m,pixel_size_m)
    output_path.parent.mkdir(parents=True,exist_ok=True);output_path.write_text(json.dumps(r,separators=(",",":")),encoding="utf-8");return r

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("input",type=Path);p.add_argument("output",type=Path,nargs="?",default=Path("data/processed/jezero_hirise_patch.json"))
    p.add_argument("--center-x-km",type=float,required=True);p.add_argument("--center-y-km",type=float,required=True);p.add_argument("--size-m",type=float,default=1000);p.add_argument("--pixel-size-m",type=float,default=5);a=p.parse_args()
    if not a.input.is_file():p.error(f"Input DTM not found: {a.input}")
    r=prepare(a.input,a.output,a.center_x_km,a.center_y_km,a.size_m,a.pixel_size_m)
    print(f"Wrote {a.output}; {r['width']}×{r['height']} cells at {r['native_pixel_size_m']:.2f} m; local preview only")
    return 0
if __name__=="__main__":raise SystemExit(main())
