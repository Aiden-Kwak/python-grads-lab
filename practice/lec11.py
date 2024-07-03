# composite map for ENSO

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

path_precip='../datasets/precip.mon.mean.nc'
path_sst='../datasets/sst.mnmean.nc'
path_hgt='../datasets/hgt.mon.mean.nc'

precip_nc=xr.open_dataset(path_precip)
sst_nc=xr.open_dataset(path_sst)
hgt_nc=xr.open_dataset(path_hgt)

#print(precip_nc)
#print(sst_nc)
#print(hgt_nc)

precip=precip_nc.data_vars['precip']
sst=sst_nc.data_vars['sst']
hgt=hgt_nc.data_vars['hgt']


print(precip.shape)
print(sst.shape)
print(hgt.shape)
#(545, 72, 144)
#(2045, 89, 180)
#(491, 17, 73, 144)

hgt_200mb=hgt.sel(level=200)
print(hgt_200mb.shape)

def monthly_anomalies(variable):
    climatology=variable.groupby('time.month').mean(dim='time')
    anomalies=variable.groupby('time.month')-climatology
    return anomalies

precip_ano=monthly_anomalies(precip)
sst_ano=monthly_anomalies(sst)
hgt_200mb_ano=monthly_anomalies(hgt_200mb)

elninos=['1983-01', '1987-01', '1988-01', '1992-01', '1995-01', '1998-01', '2003-01', '2010-01', '2016-01']
laninas = ['1989-01', '1996-01', '1999-01', '2000-01', '2008-01', '2011-01', '2012-01']

elnino_precip=0
elnino_sst=0
elnino_hgt=0

lanina_precip=0
lanina_sst=0
lanina_hgt=0

for elnino in elninos:
    elnino_precip+=precip_ano.sel(time=elnino)[0]/len(elninos)
    elnino_sst+=sst_ano.sel(time=elnino)[0]/len(elninos)
    elnino_hgt+=hgt_200mb_ano.sel(time=elnino)[0]/len(elninos)

for lanina in laninas:
    lanina_precip+=precip_ano.sel(time=lanina)[0]/len(laninas)
    lanina_sst+=sst_ano.sel(time=lanina)[0]/len(laninas)
    lanina_hgt+=hgt_200mb_ano.sel(time=lanina)[0]/len(laninas)

print(elnino_hgt)
print(lanina_hgt)

def plot_precip(ax, variable, title):
    m=Basemap(
        lon_0=180, lat_0=0,
        llcrnrlon=0, llcrnrlat=-70, urcrnrlon=360, urcrnrlat=80,
        resolution='i', ax=ax
    )
    coord=np.meshgrid(variable.lon, variable.lat)
    m.drawcoastlines(linewidth=0.75, color='gray')
    m.drawparallels(np.linspace(-60, 80, 5), labels=[1, 0, 0, 0], linewidth=0)
    m.drawmeridians(np.linspace(0, 360, 5), labels=[0, 0, 0, 1], linewidth=0)

    precip_contourf=m.contourf(coord[0], coord[1], variable, cmap=plt.cm.Spectral, levels=np.linspace(-5, 5, 11), extend='both')
    cbar=m.colorbar(precip_contourf, ax=ax, pad=0.3, location='bottom')
    cbar.ax.tick_params(labelsize=10)
    ax.set_title(title)

def plot_sst(ax, variable, title):
    m=Basemap(
        lon_0=180, lat_0=0,
        llcrnrlon=0, llcrnrlat=-70, urcrnrlon=360, urcrnrlat=80,
        resolution='i', ax=ax
    )
    coord=np.meshgrid(variable.lon, variable.lat)
    m.drawcoastlines(linewidth=0.75, color='gray')
    m.drawlsmask(land_color='lightgray')
    m.drawparallels(np.linspace(-80,80,5), labels=[1,0,0,0], linewidth=0) 
    m.drawmeridians(np.linspace(0,360,5), labels=[0,0,0,1], linewidth=0)

    sst_contourf=m.contourf(coord[0], coord[1], variable, cmap=plt.cm.bwr, levels=20)
    cbar=m.colorbar(sst_contourf, ax=ax, pad=0.3, location='bottom')
    cbar.ax.tick_params(labelsize=10)
    ax.set_title(title)

def plt_hgt(ax, variable, title):
    m=Basemap(
        projection='ortho',
        lon_0=180, lat_0=20,
        resolution='i', ax=ax
    )
    coord=np.meshgrid(variable.lon, variable.lat)
    lons, lats=m(coord[0], coord[1])
    m.drawcoastlines(linewidth=0.75, color='gray')
    hgt_contourf=m.contourf(lons, lats, variable, cmap=plt.cm.coolwarm, levels=30)

    ax.set_title(title)
    cbar=m.colorbar(hgt_contourf, ax=ax, location='bottom')
    cbar.ax.tick_params(labelsize=10)

nrow=2
ncol=3

fig, ax=plt.subplots(nrows=nrow, ncols=ncol, figsize=(18, 10))
plt.subplots_adjust(wspace=0.2, hspace=0.3)

plot_precip(ax[0][0], elnino_precip, 'El Nino Precipitation')
plot_precip(ax[1][0], lanina_precip, 'La Nina Precipitation')
plot_sst(ax[0][1], elnino_sst, 'El Nino SST')
plot_sst(ax[1][1], lanina_sst, 'La Nina SST')
plt_hgt(ax[0][2], elnino_hgt, 'El Nino 200mb HGT')
plt_hgt(ax[1][2], lanina_hgt, 'La Nina 200mb HGT')

plt.show()
