import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math
import os

dataDir = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\pbのデータ"
fileNameMat = os.listdir(dataDir)
fileNameMat.sort()
curIndex = 0

dataFileDir = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\三次元pb速度.txt"
dataFileDir2 = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\水平方向速度データ表.txt"

xMat = []
yMat = []
zMat = []
tMat = []

# 1回だけ図と軸を作成
f = plt.figure(figsize=(18, 6))
ax = f.add_subplot(121, projection='3d')
ax2d = f.add_subplot(122)
cbar2d = None  # 初期化

def drawPro():
    global curIndex, cbar2d, sc
    fid = open(dataDir + '\\' + fileNameMat[curIndex])
    strLine = fid.readline()
    while True:
        strLine = fid.readline()
        if len(strLine) < 2:
            break
        tVal = float(strLine[0:10])
        xVal = float(strLine[11:18])/1000
        yVal = float(strLine[19:26])/1000
        zVal = float(strLine[27:32])/1000
        xMat.append(xVal)
        yMat.append(yVal)
        zMat.append(zVal)
        tMat.append(tVal)
    fid.close()
    x = np.array(xMat)
    y = np.array(yMat)
    z = np.array(zMat)
    t = np.array(tMat)

    # 既存のプロットをクリア
    ax.clear()
    
    sc = ax.scatter(x, y, z, c=t, cmap='viridis', s=5, alpha=0.7)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # 既存のプロットをクリア
    ax2d.clear()

    ax2d.scatter(t, z, c=t, cmap='viridis', s=20, alpha=0.7)
    ax2d.set_xlabel('X')
    ax2d.set_ylabel('Y')

clicked_x = None
indexMin = None
indexMax = None
axList = []

def clickBack(event):
    global clicked_x, indexMin, indexMax, axList
    strKey = event.key
    if strKey == 'd':
        drawNext()
    elif strKey == 'b':
        drawPrev()
    elif strKey == 'i':
        clicked_x = None
        indexMin = None
        indexMax = None
        axList = []
        drawPro()
        f.canvas.draw()
    elif strKey == 'z':
        ax.set_xlim(min(xMat), max(xMat))
        ax.set_ylim(min(yMat), max(yMat))
        ax.set_zlim(min(z), max(z))
        drawExpandedGraph() 
        f.canvas.draw()
    elif strKey == 'h':
        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y), max(y))
        ax.set_zlim(min(zMat), max(zMat))
        drawExpandedGraph()
        f.canvas.draw()
    elif strKey == 'w':
        save_data()
    elif strKey == 'm':
        save_horizontal_data()
        
        

def drawNext():
    global curIndex, xMat, yMat, zMat, tMat, cbar2d
    curIndex += 1
    xMat = []
    yMat = []
    zMat = []
    tMat = []
    drawPro()
    f.canvas.draw()

def drawPrev():
    global curIndex, xMat, yMat, zMat, tMat, cbar2d
    curIndex -= 1
    xMat = []
    yMat = []
    zMat = []
    tMat = []
    drawPro()
    f.canvas.draw()

def drawExpandedGraph():
    global sc, x, y, z, t
    sc = ax.scatter(x, y, z, c=t, cmap='viridis', s=5, alpha=0.7)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax2d.clear()
    ax2d.scatter(t, z, c=t, cmap='viridis', s=20, alpha=0.7)
    ax2d.set_xlabel('X')
    ax2d.set_ylabel('Y')

variance_x = 0
covariance_xy = 0
covariance = None    
horizontal_speed = 0 

def get_a(x, y):
    global variance_x, covariance_xy, covariance
    mean_x = np.mean(t)
    mean_y = np.mean(y)
    n = len(x)
    for i in range(n):
        variance_param = ((x[i]-mean_x)**2)/n
        variance_x += variance_param 
        covariance_param = (x[i]*y[i])/n
        covariance_xy += covariance_param

    covariance = covariance_xy - mean_x*mean_y
    a = covariance/variance_x
    variance_x = 0
    covariance_xy = 0
    covariance = None
    return a
      
def clickChanRange(event):
    global initial_altitude, x, y, z, t, cbar2d, sc, clicked_value, speed, variance_x, a_z, a_x, a_y, covariance_xy, covariance, clicked_x, axList, indexMin, indexMax
    if event.inaxes == ax2d:
        ax2 = event.inaxes
        ax2.axvline(x = event.xdata, color = 'green')
        ax2.figure.canvas.draw()
        axList.append(event.xdata)
        if clicked_x is None:
            clicked_x = event.xdata
            closest_t = min(tMat, key=lambda x: abs(x - clicked_x))
            tlimMin = closest_t
            indexMin = tMat.index(tlimMin)
        else:
            tlimMax = min(tMat, key=lambda x: abs(x - event.xdata))
            indexMax = tMat.index(tlimMax)
    if len(axList) == 2:
        ax.clear()

        t = np.array(tMat[indexMin:indexMax])
        z = np.array(zMat[indexMin:indexMax])
        x = np.array(xMat[indexMin:indexMax])
        y = np.array(yMat[indexMin:indexMax])
        
        drawExpandedGraph()   

        a_z = get_a(t, z)
        a_x = get_a(t, x)
        a_y = get_a(t, y)
        speed = math.sqrt(a_x**2 + a_y**2 + a_z**2)
        initial_altitude = zMat[indexMin]
        
        print('z方向速度(km/s)', a_z*1000)
        print('x方向速度(km/s)', a_x*1000)
        print('y方向速度(km/s)', a_y*1000)
        print('pb速度', speed*1000)
        print('水平方向速度(km/s)', speed*1000)
        print('開始高度(km)', initial_altitude)
        
        f.canvas.draw()
        axList = []
        clicked_x = None

cid = f.canvas.mpl_connect('button_press_event', clickChanRange)

def save_data():
    global curIndex, initial_altitude, speed
    with open(dataFileDir, 'a') as file:
        file.write(f"{fileNameMat[curIndex]} | Speed(km/s): {speed*1000} | Initial altitude(km): {initial_altitude} \n")

def save_horizontal_data():
    global curIndex, initial_altitude, speed
    with open(dataFileDir2, 'a') as file:
        file.write(f"{fileNameMat[curIndex]} | horizontal_speed(km/s): {speed*1000} | Altitude(km): {initial_altitude} \n")
            
    

f.canvas.mpl_connect('key_press_event', clickBack)
if curIndex == 0:
    drawPro()
plt.show()
