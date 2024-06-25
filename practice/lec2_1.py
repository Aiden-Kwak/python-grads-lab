import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

path = '../datasets/precip.mon.mean.1x1.nc'
ncfile=xr.open_dataset(path)
print(ncfile)


precip=ncfile.data_vars['precip']
print(precip.shape) # (471, 72, 144) : [time, lat, lon]

#check null value
np.sum(np.isnan(precip)) # 결측값 확인 nan 개수

#1, spatial domain
precip_global=precip.sel(lon=ncfile.lon, lat=ncfile.lat) #sel 메서드는 xarray꺼임. 해당좌표 데이터가져옴
year_ave = np.nanmean(precip_global, axis=0)
print(np.mean([1,np.NaN,3])) # nan 포함시 nan 반환
print(np.nanmean([1,np.NaN,3])) # nan 포함됐어도 nan 제외하고 계산

# Visualization
m1=Basemap(
    lon_0=180, lat_0=0,
    llcrnrlon=0, llcrnrlat=-90, urcrnrlon=360, urcrnrlat=90,
    resolution='h'
)

coord = np.meshgrid(ncfile.lon, ncfile.lat)
m1.drawcoastlines(linewidth=0.75, color='gray')
m1.contour(coord[0], coord[1], year_ave) # 경도, 위도, 등고선으로 그릴 데이터
plt.show()

m2=Basemap(
    lon_0=180, lat_0=0,
    llcrnrlon=0, llcrnrlat=-90, urcrnrlon=360, urcrnrlat=90, 
    #Lower Loeft CoRNer, Upper Right CoRNer
    resolution='h'
)
m2.drawcoastlines(linewidth=0.7, color='gray')
m2.contourf(coord[0], coord[1], year_ave)
plt.show()