import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
from matplotlib import font_manager as fm
from matplotlib import rc

# 폰트 설정
font_path = '../font/GmarketSansTTFMedium.ttf'
font = fm.FontProperties(fname=font_path).get_name()
rc('font', family=font)

path_precip = '../datasets/precip.mon.ltm.nc'
path_uwnd = '../datasets/uwnd.mon.ltm.nc'
path_vwnd = '../datasets/vwnd.mon.ltm.nc'

precip_nc = xr.open_dataset(path_precip)
uwnd_nc = xr.open_dataset(path_uwnd)
vwnd_nc = xr.open_dataset(path_vwnd)

precip = precip_nc.data_vars['precip']
uwnd = uwnd_nc.data_vars['uwnd']
vwnd = vwnd_nc.data_vars['vwnd']

uwnd = uwnd.sel(level=850)
vwnd = vwnd.sel(level=850)

precip = precip.sel(lon=slice(225, 295), lat=slice(20, 60))
uwnd = uwnd.sel(lon=slice(225, 295), lat=slice(60, 20))
vwnd = vwnd.sel(lon=slice(225, 295), lat=slice(60, 20))

# Visualization: North American Monsoon
def plot_NAM(ax, month=int):
    select_time = '0001-0' + str(month)
    month_title = str(month) + '월'
    m = Basemap(
        lon_0=0, lat_0=0,
        llcrnrlon=225, llcrnrlat=20, urcrnrlon=295, urcrnrlat=60,
        resolution='i', ax=ax
    )
    coord = np.meshgrid(precip.lon, precip.lat)

    m.drawcoastlines(linewidth=1, color='gray')
    m.drawcountries(linewidth=1, color='gray')
    m.drawstates(linewidth=0.5, color='gray')

    # linspace는 [20.  30.  40.  50.  60.] 5개의 등간격을 만들어줌
    m.drawparallels(np.linspace(20, 60, 5), labels=[1, 0, 0, 0], linewidth=0.5)
    m.drawmeridians(np.linspace(225, 295, 6), labels=[0, 0, 0, 1], linewidth=0.5)

    mycmap = LinearSegmentedColormap.from_list('mycmap', ['white', 'orange', 'red', 'darkred'])
    precip_contour = m.contourf(coord[0], coord[1], precip.sel(time=select_time)[0], cmap=mycmap, 
                                levels=np.linspace(0, 10.5, 8))
    cbar = m.colorbar(precip_contour, ax=ax, location='right')
    cbar.ax.tick_params(labelsize=10)

    coord = np.meshgrid(uwnd.lon, uwnd.lat)
    m.quiver(coord[0], coord[1], uwnd.sel(time=select_time)[0], vwnd.sel(time=select_time)[0], width=0.003, scale=200)
    ax.set_title('NAM ' + month_title)

nrow = 3
ncol = 2
fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(13.5, 13.5))

for row in range(0, 3):
    for col in range(0, 2):
        plot_NAM(ax[row, col], month=row * 2 + col + 4)

plt.show()
