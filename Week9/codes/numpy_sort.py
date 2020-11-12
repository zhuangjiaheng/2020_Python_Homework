#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: numpy_sort.py
#@Software: PyCharm


# import numpy as np
# data = np.array([[14,  1],
#  [14,  7],
#  [15,  1],
#  [15,  7],
#  [33,  4],
#  [33,  6],
#  [33,  8],
#  [35,  2],
#  [35,  3],
#  [35,  5]] )
# # 按照第一列排序
# idex=np.lexsort([data[:,0]])
# sorted_data = data[idex, :]
# print(sorted_data)
# # 按照第二列排序
# idex=np.lexsort([data[:,1]])
# print(idex)
# sorted_data = data[idex, :]
# print(sorted_data)


def f(a):
    a+=1
a=0
for i in range(5):
    f(a)
    print(a)