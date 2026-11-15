from __future__ import annotations
import unittest
import numpy as np
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from prepare_hirise_patch import sample_patch,local_to_mars_xy,SCHEMA

class HiRiseTests(unittest.TestCase):
 def test_extracts_local_patch(self):
  cx,cy=local_to_mars_xy(0,0);res=50.;mem=MemoryFile()
  ds=mem.open(driver="GTiff",height=200,width=200,count=1,dtype="float32",crs="EPSG:3857",transform=from_origin(cx-5000,cy+5000,res,res))
  try:
   y,x=np.mgrid[0:200,0:200];ds.write((1000+x*.1-y*.1).astype("float32"),1)
   out=sample_patch(ds,0,0,size_m=500,pixel_size_m=5)
   self.assertEqual(out["schema"],SCHEMA);self.assertEqual((out["width"],out["height"]),(101,101));self.assertIn("Independent local",out["use"])
  finally:ds.close();mem.close()
 def test_rejects_large_grid(self):
  cx,cy=local_to_mars_xy(0,0);mem=MemoryFile();ds=mem.open(driver="GTiff",height=200,width=200,count=1,dtype="float32",crs="EPSG:3857",transform=from_origin(cx-5000,cy+5000,50,50))
  try:
   ds.write(np.ones((200,200),dtype="float32"),1)
   with self.assertRaisesRegex(ValueError,"501 × 501"):sample_patch(ds,0,0,size_m=10000,pixel_size_m=5)
  finally:ds.close();mem.close()
if __name__=="__main__":unittest.main()
