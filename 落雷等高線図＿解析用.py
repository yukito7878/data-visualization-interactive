import matplotlib.pyplot as plt
import numpy as np
import os

f = plt.figure(figsize=(10,8))
re = 0.05
le = 0.05
he = 0.1
w1 = 0.7
w2 = 0.1

te = 0.05
be = 0.05
ve = 0.1
h = 0.4

ax1 = f.add_axes([le, 1-te-h, w1, h])
ax2 = f.add_axes([le+w1+he, 1-te-h, w2, h])
ax3 = f.add_axes([le, be, w1, h])
ax4 = f.add_axes([le+w1+he, be, w2, h])

strRoot = r"C:\Users\yukit\Downloads\python05-data (1)\python05-data"
strMat = os.listdir(strRoot)
strMat.sort()

sumArray = np.zeros((12,24))
countArray = np.zeros((12,24))

for fileMonth in strMat:
    monthVal = fileMonth[4:6]
    monthMatDir = strRoot + '\\' + fileMonth
    monthMat = os.listdir(monthMatDir)
    monthMat.sort()
    for fileName in monthMat:
        fid = open(monthMatDir + '\\' + fileName)
        while True:
            strLine = fid.readline()
            if len(strLine) == 0:
                break
            hourVal = int(strLine[0:2])
            tempVal = float(strLine[7:12])
            
            sumArray[int(monthVal)-1, hourVal] += tempVal
            countArray[int(monthVal)-1, hourVal] += 1
aveArray = np.divide(sumArray, countArray)

aveArray_warm = aveArray[4:10, :]
aveArray_cold1 = aveArray[10:12, :]
aveArray_cold2 = aveArray[0:4, :]
aveArray_cold = np.vstack((aveArray_cold1, aveArray_cold2))

xMat = np.arange(24)
yMat = np.arange(6)
warmMax = np.amax(aveArray_warm)
warmMin = np.amin(aveArray_warm)
coldMax = np.amax(aveArray_cold)
coldMin = np.amin(aveArray_cold)

c1 = ax1.contourf(xMat, yMat, aveArray_warm, levels = np.arange(int(warmMin), int(warmMax)+2, 1), cmap = 'jet')
cb1 = plt.colorbar(c1, cax = ax2)

c2 = ax3.contourf(xMat, yMat, aveArray_cold, levels = np.arange(int(coldMin), int(warmMax)+2, 1), cmap = 'jet')
cb2 = plt.colorbar(c2, cax = ax4) 

ax1.set_yticklabels([5,6,7,8,9,10])
ax3.set_yticklabels([11,12,1,2,3,4])  
 
plt.show()