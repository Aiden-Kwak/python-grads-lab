import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec
from matplotlib.patches import Polygon
from matplotlib import font_manager as fm
from matplotlib import rc

# 폰트 설정
font_path = '../font/GmarketSansTTFMedium.ttf' # otf가 안되는듯?
font = fm.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 데이터셋 파일 열기
path = '../datasets/precip.mon.ltm.nc'
ncfile = xr.open_dataset(path)
print(ncfile)

# 특정 경도 및 위도 범위의 데이터 선택
precip = ncfile.data_vars['precip']
precip_usa = precip.sel(lon=slice(225, 295), lat=slice(20, 60))
print('=' * 50)
rms = precip_usa.std(dim='time')

# 특정 지역 강수량 평균
region1 = precip.sel(lon=slice(232, 238), lat=slice(45, 51)).mean(dim=['lon', 'lat'])
region2 = precip.sel(lon=slice(262, 267), lat=slice(38, 44)).mean(dim=['lon', 'lat'])
print(region1)
print(region2)

# 시각화 함수
def draw_box(ax, m, lon1, lon2, lat1, lat2, idx):
    x1, y1 = m(lon1, lat1)
    x2, y2 = m(lon1, lat2)
    x3, y3 = m(lon2, lat2)
    x4, y4 = m(lon2, lat1)

    poly = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], facecolor='none', edgecolor='k', linewidth=2)
    ax.add_patch(poly)
    ax.annotate(text=idx, xy=m((lon1 + lon2) / 2, (lat1 + lat2) / 2), fontsize=15, fontweight='bold', ha='center', va='center')

# 그림 생성
fig = plt.figure(figsize=(12, 12))
spec = gridspec.GridSpec(ncols=2, nrows=2)
plt.subplots_adjust(wspace=0.2, hspace=0.3)

top_ax = fig.add_subplot(spec[0, :])
bottom_left_ax = fig.add_subplot(spec[1, 0])
bottom_right_ax = fig.add_subplot(spec[1, 1])

m = Basemap(
    lon_0=0, lat_0=0,
    llcrnrlon=230, llcrnrlat=25, urcrnrlon=290, urcrnrlat=55,
    resolution='i', ax=top_ax
)
coord = np.meshgrid(rms.lon, rms.lat)

# 미국 지도 그리기
m.drawcoastlines(linewidth=1, color='gray')
m.drawcountries(linewidth=1, color='gray')
m.drawstates(linewidth=1, color='gray')

# 위도 경도선 그리기
m.drawparallels(np.linspace(30, 50, 3), labels=[1, 0, 0, 0], fontsize=15)
m.drawmeridians(np.linspace(230, 290, 3), labels=[0, 0, 0, 1], fontsize=15)

plot1 = m.contourf(coord[0], coord[1], rms, cmap=plt.cm.BrBG)
draw_box(top_ax, m, 232, 238, 45, 51, '1')
draw_box(top_ax, m, 262, 267, 38, 44, '2')

cbar = m.colorbar(plot1, ax=top_ax, location='right', pad='5%', size='3%')
cbar.ax.tick_params(labelsize=10)
top_ax.set_title('(a) RMS of Precipitation', loc='left', fontsize=20)

month = [str(x) + '월' for x in range(1, 13)]

bottom_left_ax.bar(month, region1, width=0.7)
bottom_left_ax.set_title('(b) Region1', loc='left', fontsize=20)
bottom_left_ax.set_xlabel('Month', fontsize=15)
bottom_left_ax.set_ylabel('Precipitation [mm/day]', fontsize=15)

bottom_right_ax.bar(month, region2, width=0.7)
bottom_right_ax.set_title('(c) Region2', loc='left', fontsize=20)
bottom_right_ax.set_xlabel('Month', fontsize=15)
bottom_right_ax.set_ylabel('Precipitation [mm/day]', fontsize=15)

plt.show()
