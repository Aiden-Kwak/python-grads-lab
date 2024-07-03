# NDVI_Africa
"""
NDVI(Normalized Difference Vegetation Index)
식생이 강하게 반사되는 근적외선과 
식생이 강하게 흡수는 적색광의 차이를 측정하여 
식생을 정량화할 때 사용하는 식생 지수입니다. 
"""
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import warnings
warnings.filterwarnings("ignore")

path='../datasets/ndviavhrr19812001.nc'
ncfile=xr.open_dataset(path)
#print(ncfile)

ndvi=ncfile.data_vars['data']
ndvi_=ndvi.assign_coords({"lon": (((ndvi.lon + 180) % 360) - 180)})
print(ndvi_)

fig, ax = plt.subplots(1,2,figsize=(12,5))
