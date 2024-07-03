import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

path_precip='../datasets/precip.mon.mean.nc'
path_sst='../datasets/sst.mnmean.nc'
path_hgt='../datasets/hgt.mon.mean.nc'

precip_nc=xr.open_dataset(path_precip)
sst_nc=xr.open_dataset(path_sst)
hgt_nc=xr.open_dataset(path_hgt)

precip=precip_nc.data_vars['precip']
sst=sst_nc.data_vars['sst']
hgt=hgt_nc.data_vars['hgt']

hgt_200mb=hgt.sel(level=200)

def monthly_anomalies(variable):
    climatology=variable.groupby('time.month').mean(dim='time')
    anomalies=variable.groupby('time.month')-climatology
    return anomalies

precip_ano=monthly_anomalies(precip)
sst_ano=monthly_anomalies(sst)
hgt_200mb_ano=monthly_anomalies(hgt_200mb)

elninos=['1983-01', '1987-01', '1988-01', '1992-01', '1995-01', '1998-01', '2003-01', '2005-01', '2007-01',
         '2010-01', '2015-01']
laninas = ['1989-01', '1996-01', '1999-01', '2000-01', '2008-01', '2011-01', '2012-01']

elnino_precip=0
elnino_sst=0
elnino_hgt200=0

for elnino in elninos:
    elnino_precip+=precip_ano.sel(time=elnino)[0]/len(elninos)
    elnino_sst+=sst_ano.sel(time=elnino)[0]/len(elninos)
    elnino_hgt200+=hgt_200mb_ano.sel(time=elnino)[0]/len(elninos)

lanina_precip=0
lanina_sst=0
lanina_hgt200=0

for lanina in laninas:
    lanina_precip+=precip_ano.sel(time=lanina)[0]/len(laninas)
    lanina_sst+=sst_ano.sel(time=lanina)[0]/len(laninas)
    lanina_hgt200+=hgt_200mb_ano.sel(time=lanina)[0]/len(laninas)

def plot_precip(row, col):
    var_name='precip'

    projection_type=ccrs.PlateCarree(central_longitude=180.)
    plot_=plt.subplot(spec[row, col], projection=projection_type)
    plot_.set_extent([-180, 180, -70, 80+1], crs=ccrs.PlateCarree())

    plot_.coastlines(linewidth=0.75, color='gray')
    gl=plot_.gridlines(linewidth=0, draw_labels=True, xlocs=[-90,0,90,180], ylocs=[80,45,10,-25,-60])
    gl.xformatter=LONGITUDE_FORMATTER
    gl.yformatter=LATITUDE_FORMATTER
    gl.xlabels_top=False; gl.ylabels_right=False

    if row==0:
        var=elnino_precip
        state_name="El Niño"
    else:
        var=lanina_precip
        state_name="La Niña"
    
    lon2d, lat2d=np.meshgrid(var.lon, var.lat)
    precip_contourf=plot_.contourf(lon2d, lat2d, var, levels=20,
                                   cmap=plt.cm.Spectral, transform=ccrs.PlateCarree())
    cbar=plt.colorbar(precip_contourf, ax=plot_, location='bottom')
    cbar.ax.tick_params(labelsize=10)
    plot_.set_title(f'{state_name} composite({var_name})')

def plot_sst(row, col):
    var_name='sst'
    projection_type=ccrs.PlateCarree(central_longitude=180.)
    plot_=plt.subplot(spec[row, col], projection=projection_type)
    plot_.set_extent([-180, 180, -70, 80+1], crs=ccrs.PlateCarree())

    plot_.coastlines(linewidth=0.75, color='gray')
    plot_.add_feature(cfeature.LAND, edgecolor='gray', facecolor='lightgray')
    gl=plot_.gridlines(linewidth=0, draw_labels=True, xlocs=[-90,0,90,180], ylocs=[80,45,10,-25,-60])
    gl.xformatter=LONGITUDE_FORMATTER
    gl.yformatter=LATITUDE_FORMATTER
    gl.xlabels_top=False; gl.ylabels_right=False

    if row==0:
        var=elnino_sst
        state_name="El Niño"
    else:
        var=lanina_sst
        state_name="La Niña"
    
    lon2d, lat2d=np.meshgrid(var.lon, var.lat)
    sst_contourf=plot_.contourf(lon2d, lat2d, var, levels=20,
                                cmap=plt.cm.bwr, transform=ccrs.PlateCarree())
    cbar=plt.colorbar(sst_contourf, ax=plot_, location='bottom')
    cbar.ax.tick_params(labelsize=10)
    plot_.set_title(f'{state_name} composite({var_name})')

def plot_hgt(row, col):
    var_name='hgt 200mb'
    projection_type=ccrs.Orthographic(central_longitude=180., central_latitude=20)
    plot_=plt.subplot(spec[row, col], projection=projection_type)

    plot_.coastlines(linewidth=0.75, color='gray')

    if row==0:
        var=elnino_hgt200
        state_name="El Niño"
    else:
        var=lanina_hgt200
        state_name="La Niña"
    
    lon2d, lat2d=np.meshgrid(var.lon, var.lat)
    hgt_contourf=plot_.contourf(lon2d, lat2d, var, levels=30,
                                cmap=plt.cm.coolwarm, transform=ccrs.PlateCarree())
    cbar=plt.colorbar(hgt_contourf, ax=plot_, location='bottom', pad=0.05)
    cbar.ax.tick_params(labelsize=10)
    plot_.set_title(f'{state_name} composite({var_name})')

fig=plt.figure(figsize=(18, 10))
spec = gridspec.GridSpec(2,3)

for row in range(0,2):
    for col in range(0,3):
        if col==0:
            plot_precip(row, col)
        elif col==1:
            plot_sst(row, col)
        else:
            plot_hgt(row, col)

plt.show()