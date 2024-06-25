# three cell model
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

path_prate = '../datasets/prate.sfc.mon.mean.nc'
path_uwnd='../datasets/uwnd.mon.ltm.nc'
path_vwnd='../datasets/vwnd.mon.ltm.nc'
path_omega='../datasets/omega.mon.ltm.nc'

prate_nc=xr.open_dataset(path_prate)
uwnd_nc=xr.open_dataset(path_uwnd)
vwnd_nc=xr.open_dataset(path_vwnd)
omega_nc=xr.open_dataset(path_omega)

# uwnd란 동서방향 바람, vwnd란 남북방향바람 속도, omega는 대기 수직속도, prate는 시간당 강수량(강수율):Kg/m^2/s
prate=prate_nc.data_vars['prate']
uwnd=uwnd_nc.data_vars['uwnd']
vwnd=vwnd_nc.data_vars['vwnd']
omega=omega_nc.data_vars['omega']

#print(uwnd)
#print(uwnd.shape) # (12, 17, 73, 144): (time, level, lat, lon)

prate_ltm=prate.groupby('time.month').mean(dim='time')

# 고도기준으로 자른다고 생각하면 될듯? 1000hPa~100hPa까지 자름
# 지표에 가까울 수 록 기압이 높으니까.
uwnd=uwnd.sel(level=slice(1000,100))
vwnd=vwnd.sel(level=slice(1000,100))
omega=omega.sel(level=slice(1000,100))

# zonal mean 동서방향으로 평균화해서 남북방향을 강조
prate_zm=prate_ltm.mean(dim='lon')
uwnd_zm=uwnd.mean(dim='lon')
vwnd_zm=vwnd.mean(dim='lon')
omega_zm=omega.mean(dim='lon')

prate_zm=prate_zm*86400 # mm/day로 변환
omega_zm = -omega_zm *1e2 # hPa/day로 변환 (? 아마)

# x-component 확인
print(vwnd_zm.sel(time='0001-01')[0])
print(vwnd_zm.sel(time='0001-01'))

# visualization
nrow=3
ncol=1

fig, ax=plt.subplots(nrows=nrow, ncols=ncol, figsize=(10,10))
plt.subplots_adjust(wspace=0.2, hspace=0.3)

#1. Jan
# plate bar graph
ax[0].bar(prate_zm.lat, prate_zm.sel(month=1), color='gold')
ax[0].set_ylim(0, 13)

ax0=ax[0].twinx()

xs_q, ys_q = np.meshgrid(vwnd_zm.lat, vwnd_zm.level)
U=vwnd_zm.sel(time='0001-01')[0]
V=uwnd_zm.sel(time='0001-01')[0]
ax0.quiver(xs_q, ys_q, U, V, width=0.001, scale=300, color='k')

ax0.invert_yaxis()
ax0.set_yscale('log')

# Draw uwind in contour line
ax0.contour(uwnd_zm.lat, uwnd_zm.level, uwnd_zm.sel(time='0001-01')[0], levels=10)

ax[0].set_title('Jan (3-cell)')
ax[0].set_ylabel('Precipitation (mm/day)')
ax0.set_ylabel('(mb)') # millibar. 이거 헥토파스칼이랑 똑같은듯

# April
# plate bar graph
ax[1].bar(prate_zm.lat, prate_zm.sel(month=4), color='gold')
ax[1].set_ylim(0, 13)

ax1=ax[1].twinx()

xs_a, ys_a = np.meshgrid(vwnd_zm.lat, vwnd_zm.level)
U=vwnd_zm.sel(time='0001-04')[0]
V=uwnd_zm.sel(time='0001-04')[0]
ax1.quiver(xs_a, ys_a, U, V, width=0.001, scale=300, color='k')

ax1.invert_yaxis()
ax1.set_yscale('log')

# Draw uwind in contour line
ax1.contour(uwnd_zm.lat, uwnd_zm.level, uwnd_zm.sel(time='0001-04')[0], levels=10)

ax[1].set_title('April (3-cell)')
ax[1].set_ylabel('Precipitation (mm/day)')
ax1.set_ylabel('(mb)') # millibar. 이거 헥토파스칼이랑 똑같은듯

# July
# plate bar graph
ax[2].bar(prate_zm.lat, prate_zm.sel(month=7), color='gold')
ax[2].set_ylim(0, 13)

ax2=ax[2].twinx()

xs_j, ys_j = np.meshgrid(vwnd_zm.lat, vwnd_zm.level)
U=vwnd_zm.sel(time='0001-07')[0]
V=uwnd_zm.sel(time='0001-07')[0]
ax2.quiver(xs_j, ys_j, U, V, width=0.001, scale=300, color='k')

ax2.invert_yaxis()
ax2.set_yscale('log')

# Draw uwind in contour line
ax2.contour(uwnd_zm.lat, uwnd_zm.level, uwnd_zm.sel(time='0001-07')[0], levels=10)

ax[2].set_title('July (3-cell)')
ax[2].set_ylabel('Precipitation (mm/day)')
ax2.set_ylabel('(mb)') # millibar. 이거 헥토파스칼이랑 똑같은듯

plt.show()




