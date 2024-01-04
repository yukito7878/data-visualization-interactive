import matplotlib.pyplot as plt
import numpy as np
import os
import math

# データディレクトリ
dataDir = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\pbのデータ"
fileNameMat = os.listdir(dataDir)
fileNameMat.sort()
curIndex = 0

# 出力ファイル
dataFileDir = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\三次元pb速度.txt"
dataFileDir2 = r"C:\Users\yukit\Documents\雷解析用データ\lightning_datas\リーダ存在する\立ち上がりわかりやすい\上向きpb直後の水平方向速度表.txt"

# グラフのパラメータ
te, be, h1, h2, h3, vb = 0.03, 0.05, 0.2, 0.2, 0.4, 0.07
le, re, hb, w1 = 0.11, 0.05, 0.06, 0.52
w2 = 1 - le - re - w1 - hb

# プロット用の関数
def draw_plot():
    global xMat, yMat, zMat, tMat, matrix, expanded_count
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    xMat, yMat, zMat, tMat = [], [], [], []
    matrix = None
    expanded_count = 0
    draw_pro()
    f.canvas.draw()

def draw_pro():
    global curIndex, matrix
    fid = open(os.path.join(dataDir, fileNameMat[curIndex]))
    _ = fid.readline()  # ヘッダ行を読み飛ばす
    for strLine in fid:
        tVal = float(strLine[0:10])
        xVal = float(strLine[11:18]) / 1000
        yVal = float(strLine[19:26]) / 1000
        zVal = float(strLine[27:32]) / 1000
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
    ylim_min = min(yMat) - 1
    ylim_max = max(yMat) + 1
    zlim_min = min(zMat) - 1
    zlim_max = max(zMat) + 1
    ax5.set_xlim([zlim_min, zlim_max])
    ax5.set_ylim([ylim_min, ylim_max])
    ax1.set_title(f'{fileNameMat[curIndex]}')

# グラフ描画領域の設定
f = plt.figure(figsize=(7.5, 6.5))
ax1 = f.add_axes([le, 1 - te - h1, w1 + w2 + hb, h1])
ax2 = f.add_axes([le, 1 - te - h1 - vb - h2, w1, h2])
ax3 = f.add_axes([le + w1 + hb, 1 - te - h1 - vb - h2, w2, h2])
ax4 = f.add_axes([le, be, w1, h3])
ax5 = f.add_axes([le + w1 + hb, be, w2, h3])

# 軸ラベルとタイトルの設定
ax1.set_title(f'{fileNameMat[curIndex]}')
ax1.set_xlabel('Time (ms)')
ax2.set_ylabel('Height (km)')
ax4.set_xlabel('West-East (km)')
ax4.set_ylabel('South-North (km)')
ax5.set_xlabel('Height (km)')

# クリックイベント関連の変数
clicked_x = None
index_min = None
index_max = None

def click_back(event):
    global expanded_count, clicked_x, ax_list, ax_list_y, tlim_min, tlim_max, xlim_min, xlim_max, ylim_min, ylim_max, zlim_min, zlim_max, local_index_min, local_index_max
    str_key = event.key
    if str_key == '0':
        clicked_x = [None, None, None, None, None]
        local_index_min = [None, None, None, None, None]
        local_index_max = [None, None, None, None, None]
        ax_list = [[], [], [], [], []]
        ax_list_y = [[], [], [], [], []]
        expanded_count = 0

        draw_plot()
    elif str_key == 'd':
        draw_next()
    elif str_key == 'b':
        draw_prev()
    elif str_key == 'w':
        save_data()
    elif str_key == 'm':
        save_horizontal_data()
    elif str_key == 'r':
        filter_data()

# クリックイベントの処理
# グラフ描画とクリックイベントの関連付け
clicked_x = [None, None, None, None, None]
local_index_min = [None, None, None, None, None]
local_index_min_y = None
local_index_max_y = None
local_index_max = [None, None, None, None, None]
ax_list = [[], [], [], [], []]
ax_list_y = [[], [], [], [], []]
new_xMat, new_yMat, new_zMat, new_tMat = None, None, None, None
x_speed, y_speed, z_speed, speed = None, None, None, None
selected_elements = None
expanded_count = 0

def click_chan_range(event):
    global xMat2, yMat2, zMat2, tMat2, expanded_count, altitude, x_speed, y_speed, z_speed, speed, new_xMat, new_yMat, new_zMat, new_tMat, selected_elements, clicked_x, ax_list, tlim_min, tlim_max, xlim_min, xlim_max, ylim_min, ylim_max, zlim_min, zlim_max, local_index_min, local_index_max, index_max, local_index_min_y, local_index_max_y
    index = None
    if event.inaxes is not None:
        ax = event.inaxes
        if ax == ax1:
            index = 0
        elif ax == ax2:
            index = 1
        elif ax == ax3:
            index = 2
        elif ax == ax4:
            index = 3
        elif ax == ax5:
            index = 4

        ax.axvline(x=event.xdata, color='green')# クリックしたx軸に垂直線を描画
        ax.figure.canvas.draw()  # グラフを再描画
        ax_list[index].append(event.xdata)
        if clicked_x[index] is None:
            clicked_x[index] = event.xdata
            if index == 3:
                ax.axhline(y=event.ydata, color='red')
                ax.figure.canvas.draw()
                ax_list_y[index].append(event.ydata)
                
            else:
                closest_t = min(tMat, key=lambda x: abs(x - clicked_x[index]))
                local_index_min[index] = tMat.index(closest_t)
                xlim_min = xMat[local_index_min[index]] - 1
                ylim_min = yMat[local_index_min[index]] - 1
                zlim_min = zMat[local_index_min[index]] - 1
                
        else:
            clicked_x[index] = event.xdata
            if index == 3:
                ax.axhline(y=event.ydata, color='red')
                ax.figure.canvas.draw()
                ax_list_y[index].append(event.ydata)
            else:
                closest_t = min(tMat, key=lambda x: abs(x - event.xdata))
                local_index_max[index] = tMat.index(closest_t)
                xlim_max = xMat[local_index_max[index]] + 1
                ylim_max = yMat[local_index_max[index]] + 1
                zlim_max = zMat[local_index_max[index]] + 1

    if len(ax_list[index]) == 2:
        ax.clear()
        if index == 3:  # ax4に対する処理（xMatを使う場合）
            if expanded_count == 0:
                matrix = np.column_stack((xMat, yMat, zMat, tMat))
            else:
                matrix = np.column_stack((xMat2, yMat2, zMat2, tMat2))
            selected_elements = matrix[(matrix[:, 0] > ax_list[index][0]) & (matrix[:, 0] < ax_list[index][1]) & (matrix[:, 1] > ax_list_y[index][0]) & (matrix[:, 1] < ax_list_y[index][1])]
            new_xMat = selected_elements[:, 0].tolist()
            new_yMat = selected_elements[:, 1].tolist()
            new_zMat = selected_elements[:, 2].tolist()
            new_tMat = selected_elements[:, 3].tolist()
            ax.scatter(new_xMat, new_yMat, marker='o', s=10, c=new_xMat, edgecolor='none', alpha=0.5, cmap='jet')
            t_data = np.array(new_tMat)
            z_data = np.array(new_zMat)
            x_data = np.array(new_xMat)
            y_data = np.array(new_yMat)
            x_speed = round(get_a(t_data, x_data)*1000, 6)
            y_speed = round(get_a(t_data, y_data)*1000, 6)
            z_speed = round(get_a(t_data, z_data)*1000, 6)
            speed = round(math.sqrt(x_speed**2 + y_speed**2 + z_speed**2), 3)
            altitude = round(np.mean(new_zMat), 4)
            print('x speed(km/s)', x_speed)
            print('y speed(km/s)', y_speed)
            print('z speed(km/s)', z_speed)
            print('horizontal speed(km/s)', speed)
            print('altitude(km)', altitude)
        else:
            tMat2 = tMat[local_index_min[index]:local_index_max[index]]
            zMat2 = zMat[local_index_min[index]:local_index_max[index]]
            xMat2 = xMat[local_index_min[index]:local_index_max[index]]
            yMat2 = yMat[local_index_min[index]:local_index_max[index]]
            ax.scatter(tMat2, zMat2, marker='o', s=10, c=tMat[local_index_min[index]:local_index_max[index]], edgecolor='none', alpha=0.5, cmap='jet')
            ax2.scatter(tMat2, xMat2, marker='o', s=10, c=tMat[local_index_min[index]:local_index_max[index]], edgecolor='none', alpha=0.5, cmap='jet')
            ax3.hist(zMat, bins=20, range=[int(min(zMat)), int(max(zMat)) + 1], histtype='step', orientation='horizontal')
            ax4.clear()
            ax4.scatter(xMat2, yMat2, marker='o', s=10, c=tMat[local_index_min[index]:local_index_max[index]], edgecolor='none', alpha=0.5, cmap='jet')
            ax5.scatter(zMat2, yMat2, marker='o', s=10, c=tMat[local_index_min[index]:local_index_max[index]], edgecolor='none', alpha=0.5, cmap='jet')
            ax.set_xlim([ax_list[index][0], ax_list[index][1]])
            ax2.set_xlim([ax_list[index][0], ax_list[index][1]])
            expanded_count += 1
            

        ax.set_title(f'{fileNameMat[curIndex]}')
    
        f.canvas.draw()
        ax_list[index] = []
        ax_list_y[index] = []
        clicked_x[index] = None
        selected_elements = None


f.canvas.mpl_connect('button_press_event', click_chan_range)

def get_a(x, y):
    variance_x = 0
    covariance_xy = 0
    covariance = None
    mean_x = np.mean(x)
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

def indicate_speed(x, y, z):
    global zMat
    speed = math.sqrt(x**2 + y**2 + z**2)
    print('x方向速度(km/s)', x*1000)
    print('y方向速度(km/s)', y*1000)
    print('z方向速度(km/s)', z*1000)
    print('pb速度', speed*1000)
    print('高度(km)', np.mean(zMat))
# 次のファイルを描画
def draw_next():
    global curIndex, xMat, yMat, zMat, tMat
    curIndex += 1
    draw_plot()

# 前のファイルを描画
def draw_prev():
    global curIndex, xMat, yMat, zMat, tMat
    curIndex -= 1
    draw_plot()

# データを保存
def save_data():
    global curIndex, a, tlim_min, tlim_max, index_min, speed
    with open(dataFileDir, 'a') as file:
        file.write(f"{fileNameMat[curIndex]} | Speed(km/s): {speed*1000} | Initial altitude(km): {zMat[index_min]} | \n")

def save_horizontal_data():
    global curIndex, speed, horizontal_speed, x_speed, y_speed, z_speed, new_zMat, altitude
    with open(dataFileDir2, 'a') as file:
        file.write(f"{fileNameMat[curIndex]} | x(km/s): {x_speed} | y(km): {y_speed} | z(km): {z_speed} | altitude(km): {altitude} |  horizontal_speed: {speed}(km/s)\n")

def filter_data():
    global curIndex, xMat, yMat, zMat, tMat, xdata, ydata, zdata, index_min, index_max
    zdatas = zMat[index_min:index_max]
    xdatas = xMat[index_min:index_max]
    ydatas = yMat[index_min:index_max]
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
            index_max = index_max-1
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax1.scatter(tMat[index_min:index_max], zMat[index_min:index_max], marker='o', s=10, c=tMat[index_min:index_max], edgecolor='none', alpha=0.5, cmap='jet')
    ax2.scatter(tMat[index_min:index_max], xMat[index_min:index_max], marker='o', s=10, c=tMat[index_min:index_max], edgecolor='none', alpha=0.5, cmap='jet')
    ax3.hist(zMat[index_min:index_max], bins=20, range=[int(min(zMat[index_min:index_max])), int(max(zMat[index_min:index_max])) + 1], histtype='step', orientation='horizontal')
    ax4.scatter(xMat[index_min:index_max], yMat[index_min:index_max], marker='o', s=10, c=tMat[index_min:index_max], edgecolor='none', alpha=0.5, cmap='jet')
    ax5.scatter(zMat[index_min:index_max], yMat[index_min:index_max], marker='o', s=10, c=tMat[index_min:index_max], edgecolor='none', alpha=0.5, cmap='jet')
    
    ax1.set_title(f'{fileNameMat[curIndex]}')
    f.canvas.draw()
   
f.canvas.mpl_connect('key_press_event', click_back)
draw_plot()
plt.show()