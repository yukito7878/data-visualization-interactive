import numpy as np
import matplotlib.pyplot as plt
import os
import bz2

plt.rcParams['agg.path.chunksize'] = 20000

dataDir = r'ここにファイルパスを添付'
fileMat = os.listdir(dataDir)
fileMat.sort()

f = plt.figure(figsize=(9, 4))
ax = f.add_axes([0.12, 0.12, 0.81, 0.81])

curIndex = 0
sampRate = 1000000
fileName = fileMat[curIndex]
tMat = np.linspace(0, 1000, sampRate)
fid = bz2.BZ2File(dataDir + '\\' + fileName)
dataMat = np.frombuffer(fid.read(), np.int16)
fid.close()
ax.plot(tMat, dataMat)
ax.set_xlim(tMat[0], tMat[-1])
ax.set_xlabel('Times(ms)')
ax.set_ylabel('Digital Unit')
ax.set_title(f'{fileName}')

def chanRange(curT, tLen):
    global curIndex
    fileName = fileMat[curIndex]
    fid = bz2.BZ2File(dataDir + '\\' + fileName)
    dataMat = np.frombuffer(fid.read(), np.int16)
    curX = int(curT*sampRate/1000)
    xLen = int(tLen*sampRate/1000)
    
    dataLen = len(dataMat)
    if xLen < 0:
        xLen = dataLen*2
    
    xBeg = int(curX - xLen/2)
    xEnd = int(curX + xLen/2)
    if xBeg < 0:
        xBeg = 0
    if xEnd > dataLen:
        xEnd = dataLen
        
    ax.clear()
    newtMat = tMat[xBeg:xEnd]
    newdataMat = dataMat[xBeg:xEnd]
    ax.plot(newtMat, newdataMat)
    ax.set_xlim(tMat[xBeg], tMat[xEnd-1])
    ax.set_xlabel('Time(ms)')
    ax.set_ylabel('Digital Unit')
    ax.set_title(f'{fileName}')
    f.canvas.draw()
    
def click_fun(event):
    global curT
    global val
    curT = event.xdata
    val = event.ydata
    print('Peek Time: ', curT)
    print('Peek Val: ', val)
    
def key_press_fun(event):
    global curIndex
    global tMat
    global dataMat
    strKey = event.key
    if strKey == 'd':
        curIndex += 1
        fileName = fileMat[curIndex]
        fid = bz2.BZ2File(dataDir + '\\' + fileName)
        dataMat = np.frombuffer(fid.read(), np.int16)
        ax.clear()
        ax.plot(tMat, dataMat)
        ax.set_xlim(tMat[0], tMat[-1])
        ax.set_xlabel('Time(ms)')
        ax.set_ylabel('Digital Unit')
        ax.set_title(f'{fileName}')
        f.canvas.draw()
    
    if strKey == 'a':
        curIndex += 1
        fileName = fileMat[curIndex]
        fid = bz2.BZ2File(dataDir + '\\' + fileName)
        dataMat = np.frombuffer(fid.read(), np.int16)
        ax.clear()
        ax.plot(tMat, dataMat)
        ax.set_xlim(tMat[0], tMat[-1])
        ax.set_xlabel('Time(ms)')
        ax.set_ylabel('Digital Unit')
        ax.set_title(f'{fileName}')
        f.canvas.draw()
        
    if strKey == '1':
        chanRange(curT, 100)
    if strKey == '2':
        chanRange(curT, 10)
    if strKey == '3':
        chanRange(curT, 1)
    if strKey == '4':
        chanRange(curT, -1)

axList = []

def clickChanRange(event):
    global axList
    global curIndex
    if event.inaxes is not None:
        ax = event.inaxes
        ax.axvline(x = event.xdata, color = 'green')
        ax.figure.canvas.draw()
        axList.append(event.xdata)
    if len(axList) == 2:
        ax.clear()
        xBeg = int(axList[0]*1000)
        xEnd = int(axList[1]*1000)
        newtMat = tMat[xBeg:xEnd]
        newdataMat = dataMat[xBeg:xEnd]
        ax.plot(newtMat, newdataMat)
        ax.set_xlim(tMat[xBeg], tMat[xEnd])
        ax.set_xlabel('Time(ms)')
        ax.set_ylabel('Digital Unit')
        ax.set_title(f'{fileName}')
        f.canvas.draw()
        axList = []
        
f.canvas.mpl_connect('key_press_event', key_press_fun)
f.canvas.mpl_connect('button_press_event', click_fun)
f.canvas.mpl_connect('button_press_event', clickChanRange)

plt.show()
        
    
    






    