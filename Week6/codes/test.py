#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: test.py
#@Software: PyCharm
#
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# name_list = ['姓名查询', '电话查询', '邮件查询']
# #per_time by search
# # num_list = [0.0000748,0.00019372,0.00019852]
# # num_list1 = [0.000366716,0.000765456,0.00071416]
# # num_list2 = [0.000629918,0.001380862,0.001414134]
# #all_time by hash_search
# num_list = [0.0002,	0.00024	,0.0003]
# num_list1 =[0.00112	,0.00136,0.00094]
# num_list2 = [0.00212,0.00318,0.0023]
#
#
#
# x = list(range(len(num_list)))
# total_width, n = 0.9, 3
# width = total_width / n
#
# plt.bar(x, num_list, width=width, label='N=1000', fc='skyblue')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x, num_list1, width=width, label='N=5000', tick_label=name_list, fc='orange')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x, num_list2, width=width, label='N=10000', fc='pink')
# plt.title("所有对象哈希查询总时间")
# plt.legend()
# plt.show()

from xpinyin import Pinyin
p = Pinyin()
a = p.get_initials(u"庄嘉恒", u'')
print(a.lower())

import json

# Python 字典类型转换为 JSON 对象
data = {
    'no': 1,
    'name': 'Runoob',
    'url': 'http://www.runoob.com'
}

json_str = json.dumps(data)
print("Python 原始数据：", repr(data))
print("JSON 对象：", json_str)
