import matplotlib.pyplot as plt
import os
import numpy as np

f1 = plt.figure(figsize=(10, 6))
ax = f1.add_axes([0.12, 0.12, 0.81, 0.81])
f2 = plt.figure(figsize=(10, 6))
ax2 = f2.add_axes([0.12, 0.12, 0.81, 0.81])
strRoot = r"C:\Users\yukit\Downloads\python05-data (1)\python05-data"
monthMat_unsorted = os.listdir(strRoot)
monthMat = sorted(monthMat_unsorted, key = lambda x: int(str(x)[4:6]))

hourValList = [0]*24
tempValList = [0]*24
aveTemp = []
maxTemp = []
minTemp = []
for monthName in monthMat:
    monthVal = monthName[4:6]
    monthDir = strRoot + '\\' + monthName
    daysMat = os.listdir(monthDir)
    daysMat.sort()
    
    countTemp = 0
    sumTemp = 0
    monthTemp = []
    for daysFile in daysMat:
        fid = open(monthDir + '\\' + daysFile)
        while True:
            strLine = fid.readline()
            if len(strLine) == 0:
                break
            hourVal = int(strLine[0:2])
            tempVal = float(strLine[7:12])
            
            hourValList[hourVal] += 1
            tempValList[hourVal] += tempVal
            
            sumTemp += tempVal
            countTemp += 1
            monthTemp.append(tempVal)
            
    aveTempeach = sumTemp/countTemp
    aveTemp.append(aveTempeach)
    maxTemp.append(max(monthTemp))
    minTemp.append(min(monthTemp))


    
aveTempVal = np.divide(tempValList, hourValList)
hourMat = np.arange(24)
monthLabel = np.arange(1, 13)
print(aveTempVal)
print(maxTemp)
print(minTemp)
print(aveTemp)

ax.plot(hourMat, aveTempVal, '-o', color = 'r')
ax2.plot(monthLabel, maxTemp, '-o', color = 'r')
ax2.plot(monthLabel, aveTemp, '-o', color = 'black')
ax2.plot(monthLabel, minTemp, '-o', color = 'b')


ax.set_title('Average Temp each hour')
ax.set_xlabel('Hour')
ax.set_ylabel('Temprature')
ax2.set_title('Average, max, min Temprature in each months')
ax2.set_xlabel('month')
ax2.set_ylabel('Temprature')

plt.show()
            