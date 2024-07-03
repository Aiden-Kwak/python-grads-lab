import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

path_prate = '../datasets/prate.sfc.mon.mean.nc'
path_shum = '../datasets/shum.mon.ltm.nc'
path_vwnd = '../datasets/vwnd.mon.ltm.nc'
path_omega = '../datasets/omega.mon.ltm.nc'

#prate_nc = xr.open_dataset(path_prate, decode_times=False)
#shum_nc = xr.open_dataset(path_shum, decode_times=False)
#vwnd_nc = xr.open_dataset(path_vwnd, decode_times=False)
#omega_nc = xr.open_dataset(path_omega, decode_times=False)
prate_nc = xr.open_dataset(path_prate)
shum_nc = xr.open_dataset(path_shum)
vwnd_nc = xr.open_dataset(path_vwnd)
omega_nc = xr.open_dataset(path_omega)
print(prate_nc.time)
print(shum_nc.time)
print(vwnd_nc.time)
print(omega_nc.time)

prate = prate_nc.data_vars['prate']
shum = shum_nc.data_vars['shum']
vwnd = vwnd_nc.data_vars['vwnd']#.sel(level=slice(1000, 100))
omega = omega_nc.data_vars['omega']

#print(prate.shape)
#print(shum.shape)
#print(vwnd.shape)
#print(omega.shape)
#(848, 94, 192)
#(12, 8, 73, 144)
#(12, 12, 73, 144)
#(12, 12, 73, 144)
#print(vwnd_nc.data_vars['vwnd'].shape) (12,17,73,144)

prate=prate.sel(lat=slice(80,-35), lon=slice(240, 260))
shum=shum.sel(lat=slice(80,-35), lon=slice(240, 260), level=slice(1000, 100))
vwnd=vwnd.sel(lat=slice(80,-35), lon=slice(240, 260), level=slice(1000, 100))
omega=omega.sel(lat=slice(80,-35), lon=slice(240, 260), level=slice(1000, 100))

prate_zm = prate.mean(dim='lon')
shum_zm = shum.mean(dim='lon')
#vwnd_zm = vwnd.mean(dim='lon')
vwnd_zm = vwnd.mean(dim='lon')
omega_zm = omega.mean(dim='lon')

# lon 차원에 대해서 평균화
prate_zm *= 86400  # mm/day로 변환
omega_zm *= -1e2  # hPa/day로 변환

# omega_zm을 vwnd_zm 차원에 대해 보간: cdo?ncl?  weight를 맞춰야함. 평면도상에서 했을떄의 문제
#omega_zm_interp = omega_zm.interp(level=vwnd_zm.level)
#print(omega_zm_interp.level)
print('-'*100)
print(omega_zm.level)
print('-'*100)
print(vwnd_zm.level)
print('-'*100)
print(prate_zm.time)
#print(prate_zm.sel(time='0001-01')[0])

def nam_vertical(ax, m=int):
    select_month='0001-0'+str(m)
    ax.bar(prate_zm.lat, prate_zm.sel(time=select_month)[0], width=1.5, color='gold')
    plt.xticks(np.arange(-30, 80, 10))

    ax1=ax.twinx()
    xs_q, ys_q = np.meshgrid(vwnd_zm.lat, vwnd_zm.level)

    U=vwnd_zm.sel(time=select_month)[0]
    V=omega_zm.sel(time=select_month)[0]

    ax1.quiver(xs_q, ys_q, U, V, width=0.001, scale=170)
    ax1.invert_yaxis()
    ax1.set_yscale('log')

    ax2=ax.twinx()
    shum_contour=ax2.contourf(shum_zm.lat, shum_zm.level, shum_zm.sel(time=select_month)[0], cmap='coolwarm', levels=np.linspace(0, 20, 11))
    ax2.set_axis_off()
    plt.colorbar(shum_contour, pad=0.08, label='grams/kg')

    ax.set_title('NAM vertical month={0}'.format(m))
    ax.set_ylabel('mm/day')
    ax1.set_ylabel('hPa/day')


"""
# visualization 함수
def nam_vertical(ax, m):
    select_month = m - 1  # 0부터 시작
    prate_data = prate_zm[select_month]
    vwnd_data = vwnd_zm[select_month]
    omega_data = omega_zm[select_month]
    print(prate_data.shape)
    print(vwnd_data.shape)
    print(omega_data.shape)
    
    ax.bar(prate_zm.lat, prate_data, width=1.5, color='gold', zorder=2)
    ax.set_xticks(np.arange(-30, 80, 10))
    
    ax1 = ax.twinx()
    xs_q, ys_q = np.meshgrid(vwnd_zm.lat, vwnd_zm.level)
    U = vwnd_data
    V = omega_data
    
    ax1.quiver(xs_q, ys_q, U, V, width=0.001, scale=170, zorder=3)  #zorder넣었는데 안보임. 그냥 안그려지는건가
    ax1.invert_yaxis()
    ax1.set_yscale('log')

    ax2 = ax.twinx()
    shum_contour = ax2.contourf(shum_zm.lat, shum_zm.level, shum_zm[select_month], cmap='coolwarm', levels=np.linspace(0, 20, 11), zorder=1)
    ax2.set_axis_off()
    plt.colorbar(shum_contour, ax=ax, pad=0.08, label='grams/kg')

    ax.set_title('NAM vertical month={0}'.format(m))
    ax.set_ylabel('mm/day')
    ax1.set_ylabel('hPa/day')
"""


nrow = 3
ncol = 1
fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(15, 12))
plt.subplots_adjust(wspace=0.2, hspace=0.3)

for i in range(nrow):
    nam_vertical(ax[i], i * 3 + 2)

plt.show()


