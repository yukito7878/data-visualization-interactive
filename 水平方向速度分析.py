import matplotlib.pyplot as plt
import numpy as np
import math

dataFileDir = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\上向きpb直後の水平方向速度表.txt"

z_speedMat = []
z_altitudeMat = []

fid = open(dataFileDir)
strLine = fid.readline()
while True:
    strLine = fid.readline()
    if len(strLine)<2:
        break
    z_altitudeVal = float(strLine[99:104])
    z_speedVal = float(strLine[127:133])
    z_speedMat.append(z_speedVal)
    z_altitudeMat.append(z_altitudeVal)
fid.close()

plt.figure(figsize=(10, 5))
plt.plot(z_altitudeMat, z_speedMat, marker='o', linestyle='', color='b')
plt.title("Speed vs. Average altitude")
plt.xlabel("Average Altitude (km)")
plt.ylabel("Speed (km/s)")
plt.grid(True)

# グラフを表示
plt.show()

x = np.array(z_altitudeMat)
y = np.array(z_speedMat)
mean_x = np.mean(x)
mean_y = np.mean(y)
variance_x = 0
variance_y = 0
covariance_xy = 0
n = len(z_speedMat)
for i in range(n):
    xvariance_param = ((x[i]-mean_x)**2)/n
    variance_x += xvariance_param 
    
    yvariance_param = ((y[i]-mean_y)**2)/n
    variance_y += yvariance_param 
    
    covariance_param = (x[i]*y[i])/n
    covariance_xy += covariance_param
                
    covariance = covariance_xy - mean_x*mean_y
    a = covariance/variance_x
sd_x = math.sqrt(variance_x)
sd_y = math.sqrt(variance_y)
print('共分散:', covariance)
print('相関係数:', covariance/(sd_x*sd_y))
print('傾き:', a)