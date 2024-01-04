import matplotlib.pyplot as plt
import numpy as np
import os
import math

dataDir = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\pbのデータ"
fileNameMat = os.listdir(dataDir)
fileNameMat.sort()
curIndex = 0

dataFileDir = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\三次元pb速度.txt"
dataFileDir2 = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\水平方向速度データ表.txt"
te = 0.03
be = 0.05
h1 = 0.2
h2 = 0.2
h3 = 0.4
vb = 0.07

le = 0.11
re = 0.05
hb = 0.06
w1 = 0.52
w2 = 1-le-re-w1-hb

f = plt.figure(figsize=(7.5,6.5))

ax1 = f.add_axes([le, 1-te-h1, w1+w2+hb, h1])
ax2 = f.add_axes([le, 1-te-h1-vb-h2, w1, h2])
ax3 = f.add_axes([le+w1+hb, 1-te-h1-vb-h2, w2, h2])
ax4 = f.add_axes([le, be, w1, h3])
ax5 = f.add_axes([le+w1+hb, be, w2, h3])

xMat = []
yMat = []
zMat = []
tMat = []

ax1.set_title(f'{fileNameMat[curIndex]}')
ax1.set_xlabel('Time(ms)')
ax2.set_ylabel('Height (km)')
ax4.set_xlabel('West-East (km)')
ax4.set_ylabel('South-North (km)')
ax5.set_xlabel('Height (km)')

def drawPro():
    global curIndex
    fid = open(dataDir + '\\' + fileNameMat[curIndex])
    strLine = fid.readline()
    while True:
        strLine = fid.readline()
        if len(strLine)<2:
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

    ax1.scatter(tMat, zMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')
    ax2.scatter(tMat, xMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')
    ax3.hist(zMat, bins=20, range=[int(min(zMat)), int(max(zMat)) + 1], histtype='step', orientation='horizontal')
    ax4.scatter(xMat, yMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')
    ax5.scatter(zMat, yMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')
    ylimMin = min(yMat) - 1
    ylimMax = max(yMat) + 1
    zlimMin = min(zMat) - 1
    zlimMax = max(zMat) + 1
    ax5.set_xlim([zlimMin, zlimMax])
    ax5.set_ylim([ylimMin, ylimMax])
    ax1.set_title(f'{fileNameMat[curIndex]}')

    
drawPro()

clicked_x = None
indexMin = None
indexMax = None
axList = []

def clickBack(event):
    global clicked_x, axList, tlimMin, tlimMax, xlimMin, xlimMax, ylimMin, ylimMax, zlimMin, zlimMax, indexMin, indexMax
    strKey = event.key
    if strKey == '0':
        tlimMin = tMat[0]
        tlimMax = tMat[-1]
        indexMin = 0
        indexMax = -1
        xlimMin = min(xMat) - 1
        xlimMax = max(xMat) + 1
        ylimMin = min(yMat) - 1
        ylimMax = max(yMat) + 1
        zlimMin = min(zMat) - 1
        zlimMax = max(zMat) + 1
        clicked_x = None
        axList = []
        
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()
        
        ax1.scatter(tMat, zMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')
        ax2.scatter(tMat, xMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')
        ax3.hist(zMat, bins=20, range=[int(min(zMat)), int(max(zMat)) + 1], histtype='step', orientation='horizontal')
        ax4.scatter(xMat, yMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')
        ax5.scatter(zMat, yMat, marker='o', s=10, c=tMat, edgecolor='none', alpha=0.5, cmap='jet')

        ax5.set_xlim([zlimMin, zlimMax])
        ax1.set_title(f'{fileNameMat[curIndex]}')
        f.canvas.draw()
    
    elif strKey == 'd':
        drawNext()
    elif strKey == 'b':
        drawPrev()
    elif strKey == 'w':
        save_data()
    elif strKey == 'm':
        save_horizontal_data()
    elif strKey == 'r':
        filter_data()
        
variance_x = 0
covariance_xy = 0
covariance = None    
horizontal_speed = 0   
def clickChanRange(event):
    global pb_speed, horizontal_speed, variance_x, a_z, a_x, a_y, covariance_xy, covariance, clicked_x, axList, tlimMin, tlimMax, xlimMin, xlimMax, ylimMin, ylimMax, zlimMin, zlimMax, indexMin, indexMax
    if event.inaxes is not None:
        ax = event.inaxes
        ax.axvline(x = event.xdata, color = 'green')
        ax.figure.canvas.draw()
        axList.append(event.xdata)
        if clicked_x is None:
            clicked_x = event.xdata
            closest_t = min(tMat, key=lambda x: abs(x - clicked_x))
            tlimMin = closest_t
            indexMin = tMat.index(tlimMin)
            xlimMin = xMat[indexMin] - 1
            ylimMin = yMat[indexMin] - 1
            zlimMin = zMat[indexMin] - 1
            
            print(tlimMin, indexMin)
            
        else:
            tlimMax = min(tMat, key=lambda x: abs(x - event.xdata))
            indexMax = tMat.index(tlimMax)
            xlimMax = xMat[indexMax] + 1
            ylimMax = yMat[indexMax] + 1
            zlimMax = zMat[indexMax] + 1
            print(tlimMax, indexMax)
        
    if len(axList) == 2:
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()

        ax1.scatter(tMat[indexMin:indexMax], zMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')
        ax2.scatter(tMat[indexMin:indexMax], xMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')
        ax3.hist(zMat[indexMin:indexMax], bins=20, range=[int(min(zMat[indexMin:indexMax])), int(max(zMat[indexMin:indexMax])) + 1], histtype='step', orientation='horizontal')
        ax4.scatter(xMat[indexMin:indexMax], yMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')
        ax5.scatter(zMat[indexMin:indexMax], yMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')

        ax1.set_title(f'{fileNameMat[curIndex]}')

        tdata = np.array(tMat[indexMin:indexMax]) # 内積計算のためにnp.arrayで作る。
        zdata = np.array(zMat[indexMin:indexMax])
        xdata = np.array(xMat[indexMin:indexMax])
        ydata = np.array(yMat[indexMin:indexMax])

        a_z = get_a(tdata, zdata)
        a_x = get_a(tdata, xdata)
        a_y = get_a(tdata, ydata)
        
        pb_speed = math.sqrt(a_x**2 + a_y**2 + a_z**2)
        horizontal_speed = math.sqrt(a_x**2 + a_y**2 + a_z**2)
        print('z方向速度(km/s)', a_z*1000)
        print('pb速度', pb_speed*1000)
        print('x方向速度(km/s)', a_x*1000)
        print('y方向速度(km/s)', a_y*1000)
        print('水平方向速度(km/s)', horizontal_speed*1000)
        print('開始高度(km)', zMat[indexMin])
        
        f.canvas.draw()
        print(axList)
        axList = []
        clicked_x = None

def drawPrams():
    global tMat, xMat, yMat, zMat, indexMin, indexMax
    tdata = np.array(tMat[indexMin:indexMax]) # 内積計算のためにnp.arrayで作る。
    zdata = np.array(zMat[indexMin:indexMax])
    xdata = np.array(xMat[indexMin:indexMax])
    ydata = np.array(yMat[indexMin:indexMax])
    
    a_z = get_a(tdata, zdata)
    a_x = get_a(tdata, xdata)
    a_y = get_a(tdata, ydata)
    pb_speed = math.sqrt(a_x**2 + a_y**2 + a_z**2)
    horizontal_speed = math.sqrt(a_x**2 + a_y**2 + a_z**2)
    print('z方向速度(km/s)', a_z*1000)
    print('pb速度', pb_speed*1000)
    print('x方向速度(km/s)', a_x*1000)
    print('y方向速度(km/s)', a_y*1000)
    print('水平方向速度(km/s)', horizontal_speed*1000)
    print('開始高度(km)', zMat[indexMin])
 
variance_x = 0
covariance_xy = 0
covariance = None      
def get_a(x, y):
    global variance_x, covariance_xy, covariance
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    print(mean_x, mean_y)
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
        
def drawNext():
    global curIndex, xMat, yMat, zMat, tMat
    curIndex += 1
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    xMat = []
    yMat = []
    zMat = []
    tMat = []
    drawPro()
    f.canvas.draw()

def drawPrev():
    global curIndex, xMat, yMat, zMat, tMat
    curIndex -= 1
    xMat = []
    yMat = []
    zMat = []
    tMat = []
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    drawPro()
    f.canvas.draw()
 
def save_data():
    global curIndex, a, tlimMin, tlimMax, indexMin
    with open(dataFileDir, 'a') as file:
        file.write(f"{fileNameMat[curIndex]} | Speed(km/s): {pb_speed*1000} | Initial altitude(km): {zMat[indexMin]} | \n")
            
def save_horizontal_data():
    global curIndex, a_x, a_y, tlimMin, tlimMax, indexMin, horizontal_speed
    horizontal_speed = math.sqrt(a_x**2 + a_y**2 + a_z**2)
    with open(dataFileDir2, 'a') as file:
        file.write(f"{fileNameMat[curIndex]} x(km/s): {a_x*1000} | y: {a_y*1000} | altitude(km): {zMat[indexMin]} | Time range (ms): {tlimMax-tlimMin} | horizontal_speed: {horizontal_speed*1000}(km/s)\n")
            
def filter_data():
    global curIndex, xMat, yMat, zMat, tMat, xdata, ydata, zdata, indexMin, indexMax
    zdatas = zMat[indexMin:indexMax]
    xdatas = xMat[indexMin:indexMax]
    ydatas = yMat[indexMin:indexMax]
    for data, data2, data3 in zip(zdatas, xdatas, ydatas):
        threshold = 2.7
        z_scores = np.abs((data - np.mean(zdatas)) / np.std(zdatas))
        z_scores_x = np.abs((data2 - np.mean(xdatas)) / np.std(xdatas))
        z_scores_y = np.abs((data3 - np.mean(ydatas)) / np.std(ydatas))
        if z_scores > threshold or z_scores_x > threshold or z_scores_y > threshold:
            filter_index = zMat.index(data)
            xMat.pop(filter_index)
            yMat.pop(filter_index)
            zMat.pop(filter_index)
            tMat.pop(filter_index)
            print(filter_index)
            indexMax = indexMax-1
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax1.scatter(tMat[indexMin:indexMax], zMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')
    ax2.scatter(tMat[indexMin:indexMax], xMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')
    ax3.hist(zMat[indexMin:indexMax], bins=20, range=[int(min(zMat[indexMin:indexMax])), int(max(zMat[indexMin:indexMax])) + 1], histtype='step', orientation='horizontal')
    ax4.scatter(xMat[indexMin:indexMax], yMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')
    ax5.scatter(zMat[indexMin:indexMax], yMat[indexMin:indexMax], marker='o', s=10, c=tMat[indexMin:indexMax], edgecolor='none', alpha=0.5, cmap='jet')
    
    ax1.set_title(f'{fileNameMat[curIndex]}')
    f.canvas.draw()
        
f.canvas.mpl_connect('button_press_event', clickChanRange)
f.canvas.mpl_connect('key_press_event', clickBack)
plt.show() 
