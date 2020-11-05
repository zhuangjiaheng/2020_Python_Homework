#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: Visualization.py
#@Software: PyCharm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import pylab
# from scipy.optimize import curve_fit
#
# def fsigmoid(x, a, b):
#     return 1.0 / (1.0 + np.exp(-a*(x-b)))
#
# xdata = np.arange(1997,2016)
# ydata = np.array([2935.8,2939.8,2978.1,3052.4,3224.3,3515.8,4154.,4714.7,5566.9,6197.8,
# 6822.2,7205.2,7656.,8366.4,9245.4,9501.7,9492.9,9639.8,9644.])
#
# popt, pcov = curve_fit(fsigmoid, xdata, ydata, method='dogbox')
#
# x = np.linspace(1995, 2025, 20)
# y = fsigmoid(x, *popt)
# print(y,popt)
# pylab.plot(xdata, ydata, 'o', label='data')
# pylab.plot(x,y, label='fit')
# #pylab.ylim(0, 1.05)
# pylab.legend(loc='best')
# pylab.show()

'''曲线图'''
# import matplotlib.pyplot as plt
# import pandas as pd
# # Import Data
# df = pd.read_csv('C:/Users/zjh/Desktop/AirPassengers.csv')
# date = df["date"].tolist()
# traffic = df["value"].tolist()
# print(date,traffic)
# # Draw Plot
# plt.figure(figsize=(16,10), dpi= 80)
# plt.plot(date, traffic,color='tab:red')
#
# # Decoration
# plt.ylim(50, 750)
# xtick_location = df.index.tolist()[::12]
# xtick_labels = [x[-4:] for x in df.date.tolist()[::12]]
# print(xtick_labels,xtick_location)
# plt.xticks(ticks=xtick_location, labels=xtick_labels, rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
# plt.yticks(fontsize=12, alpha=.7)
# plt.title("Air Passengers Traffic (1949 - 1969)", fontsize=22)
# plt.grid(axis='both', alpha=.3)
#
# # Remove borders
# plt.gca().spines["top"].set_alpha(0.0)
# plt.gca().spines["bottom"].set_alpha(0.3)
# plt.gca().spines["right"].set_alpha(0.0)
# plt.gca().spines["left"].set_alpha(0.3)
# plt.show()


'''时间面积图'''
# # Import Data
# #df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/nightvisitors.csv')
# df = pd.read_csv("C:\\Users\\zjh\\Desktop\\nightvisitors.csv")
# # Decide Colors
# mycolors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']
#
# # Draw Plot and Annotate
# fig, ax = plt.subplots(1,1,figsize=(16, 9), dpi= 80)
# columns = df.columns[1:]
# labs = columns.values.tolist()
#
# # Prepare data
# x  = df['yearmon'].values.tolist()
# y0 = df[columns[0]].values.tolist()
# y1 = df[columns[1]].values.tolist()
# y2 = df[columns[2]].values.tolist()
# y3 = df[columns[3]].values.tolist()
# y4 = df[columns[4]].values.tolist()
# y5 = df[columns[5]].values.tolist()
# y6 = df[columns[6]].values.tolist()
# y7 = df[columns[7]].values.tolist()
# #y = np.vstack([y0, y2, y4, y6, y7, y5, y1, y3])
# y = np.vstack([y0,y1,y2,y3,y4,y5,y6,y7])
#
# # Plot for each column
# labs = columns.values.tolist()
# ax = plt.gca()
# ax.stackplot(x, y, labels=labs, alpha=0.8)
#
# # Decorations
# ax.set_title('Night Visitors in Australian Regions', fontsize=18)
# ax.set(ylim=[0, 100000])
# ax.legend(fontsize=10, ncol=4)
# plt.xticks(x[::5], fontsize=10, horizontalalignment='center')
# plt.yticks(np.arange(10000, 100000, 20000), fontsize=10)
# plt.xlim(x[0], x[-1])
#
# # Lighten borders
# plt.gca().spines["top"].set_alpha(0)
# plt.gca().spines["bottom"].set_alpha(.3)
# plt.gca().spines["right"].set_alpha(0)
# plt.gca().spines["left"].set_alpha(.3)
#
# plt.show()
#

'''前后比例图'''
import matplotlib.lines as mlines
# Import Data
df = pd.read_csv("C:\\Users\\zjh\\Desktop\\gdppercap.csv")


left_label = [str(c) + ', '+ str(round(y)) for c, y in zip(df.continent, df['1952'])]
right_label = [str(c) + ', '+ str(round(y)) for c, y in zip(df.continent, df['1957'])]
klass = ['red' if (y1-y2) < 0 else 'green' for y1, y2 in zip(df['1952'], df['1957'])]

# draw line
# https://stackoverflow.com/questions/36470343/how-to-draw-a-line-with-matplotlib/36479941
def newline(p1, p2, color='black'):
    ax = plt.gca()
    l = mlines.Line2D([p1[0],p2[0]], [p1[1],p2[1]], color='red' if p1[1]-p2[1] > 0 else 'green', marker='o', markersize=6)
    ax.add_line(l)
    return l

fig, ax = plt.subplots(1,1,figsize=(14,14), dpi= 80)

# Vertical Lines
ax.vlines(x=1, ymin=500, ymax=13000, color='black', alpha=0.7, linewidth=1, linestyles='dotted')
ax.vlines(x=3, ymin=500, ymax=13000, color='black', alpha=0.7, linewidth=1, linestyles='dotted')

# Points
ax.scatter(y=df['1952'], x=np.repeat(1, df.shape[0]), s=10, color='black', alpha=0.7)
ax.scatter(y=df['1957'], x=np.repeat(3, df.shape[0]), s=10, color='black', alpha=0.7)

# Line Segmentsand Annotation
for p1, p2, c in zip(df['1952'], df['1957'], df['continent']):
    print(p1,p2,c)
    newline([1,p1], [3,p2])
    ax.text(1-0.05, p1, c + ', ' + str(round(p1)), horizontalalignment='right', verticalalignment='center', fontdict={'size':14})
    ax.text(3+0.05, p2, c + ', ' + str(round(p2)), horizontalalignment='left', verticalalignment='center', fontdict={'size':14})

# 'Before' and 'After' Annotations
ax.text(1-0.05, 13000, 'BEFORE', horizontalalignment='right', verticalalignment='center', fontdict={'size':18, 'weight':700})
ax.text(3+0.05, 13000, 'AFTER', horizontalalignment='left', verticalalignment='center', fontdict={'size':18, 'weight':700})

# Decoration
ax.set_title("Slopechart: Comparing GDP Per Capita between 1952 vs 1957", fontdict={'size':22})
ax.set(xlim=(0,4), ylim=(0,14000), ylabel='Mean GDP Per Capita')
ax.set_xticks([1,3])
ax.set_xticklabels(["1952", "1957"])
plt.yticks(np.arange(500, 13000, 2000), fontsize=12)

# Lighten borders
plt.gca().spines["top"].set_alpha(.0)
plt.gca().spines["bottom"].set_alpha(.0)
plt.gca().spines["right"].set_alpha(.0)
plt.gca().spines["left"].set_alpha(.0)
plt.show()