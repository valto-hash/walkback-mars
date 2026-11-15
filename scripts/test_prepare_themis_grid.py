from __future__ import annotations
import unittest
import numpy as np
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from prepare_themis_grid import sample_grid,SCHEMA

class ThemisTests(unittest.TestCase):
 def test_qualitative_grid(self):
  mem=MemoryFile();ds=mem.open(driver="GTiff",height=300,width=300,count=1,dtype="float32",crs="EPSG:3857",transform=from_origin(-6e6,6e6,4e4,4e4))
  try:
   ds.write(np.arange(90000,dtype="float32").reshape(300,300),1);out=sample_grid(ds)
   self.assertEqual(out["schema"],SCHEMA);self.assertEqual(len(out["values_8bit"]),261*261);self.assertFalse(out["quantitative_use_allowed"])
  finally:ds.close();mem.close()
 def test_rejects_missing_projection(self):
  mem=MemoryFile();ds=mem.open(driver="GTiff",height=10,width=10,count=1,dtype="float32",transform=from_origin(0,10,1,1))
  try:
   ds.write(np.ones((10,10),dtype="float32"),1)
   with self.assertRaisesRegex(ValueError,"explicit Mars map projection"):sample_grid(ds)
  finally:ds.close();mem.close()
if __name__=="__main__":unittest.main()
