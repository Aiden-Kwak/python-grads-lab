import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

path = '../datasets/precip.mon.ltm.nc'
ncfile=xr.open_dataset(path)
print(ncfile)

precip=ncfile.data_vars['precip']
print(precip.shape)

amazon_lon=300
amazon_lat=-3
# 아마존 위치랑 가장 가까운 (method='nearest') 좌표의 강수량 데이터 가져오기
precip_amazon=precip.sel(lon=amazon_lon, lat=amazon_lat, method='nearest')
print(precip_amazon.values)

#visualization
# nrows, ncols로 플롯개수 정하는거임. 1행1열이니까 하나만
# figure객체를 컨테이너로 안에 axe객체를 넣어서 그래프 그림(아마?)
"""
nrow=1 
ncol=1
fig, ax=plt.subplots(nrows=nrow, ncols=ncol, figsize=(12,5))
month=[x for x in range(1,13)]
ax.plot(month, precip_amazon, marker='o')
plt.xticks(np.arange(min(month), max(month)+1, 1.0))
plt.show()
"""

nrow=1
ncol=2
fig, ax=plt.subplots(nrows=nrow, ncols=ncol, figsize=(12,5))
month=[x for x in range(1,13)]
ax[0].plot(month, precip_amazon, marker='o')
ax[1].bar(month, precip_amazon, width=0.5)

for axes in ax:
    #np.arange(start, stop, step)// step은 간격
    axes.set_xticks(np.arange(1, len(month)+1, 2)) # 여러개 만들때 xticks대신 set_xticks
    # step 2주면 1,3,5,7,.. 이렇게 2씩 간격처리됨.
plt.show()
