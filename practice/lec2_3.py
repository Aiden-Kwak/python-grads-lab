import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

path = '../datasets/precip.mon.ltm.nc'
ncfile=xr.open_dataset(path)
print(ncfile)

precip=ncfile.data_vars['precip']
#wusa = western USA
precip_wusa=precip.sel(lon=240, method='nearest')
precip_wusa=precip_wusa.sel(lat=slice(30, 60)) # 위도 30-60사이로 다시 자름
print("c1: ",precip_wusa.shape)
print("c2: ",precip_wusa)
print("c3: ",precip_wusa.lat)
print("c4: ",precip_wusa.time)

#transpose y-t axis
precip_wusa=precip_wusa.transpose('lat', 'time') # matrix transpose

# Visualization
nrow=1
ncol=1
fig, ax=plt.subplots(nrows=nrow, ncols=ncol, figsize=(8,5))
month=[x for x in range(1,13)]
wusa_contour=ax.contourf(month, precip_wusa.lat, precip_wusa, cmap=plt.cm.BrBG)
ax.set_xticks(np.arange(1, len(month)+1, 1))

fig.colorbar(wusa_contour)
plt.show()