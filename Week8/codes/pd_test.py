#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: pd_test.py
#@Software: PyCharm

import numpy as np
import pandas as pd

df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
 "date":pd.date_range('20130102', periods=6),
  "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
 "age":[23,44,54,32,34,32],
 "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
  "price":[1200,np.nan,2133,5433,np.nan,4432]},
  columns =['id','date','city','category','age','price'])

print(df)
print(df.columns.tolist()[2])
print(df.interpolate())


# class TestError(Exception):
#     def __init__(self,s):
#         self.message = "Test Error"+s
#
# class Test:
#     def __init__(self):
#         self.a = 10
#
#     def test(self,s):
#         if self.a > 1:
#             raise TestError(s)
#         else :
#             print("OK")
#
# T=Test()
# try:
#     T.test('1')
# except TestError as te:
#     print(te.message)

# import numpy as np
# from scipy import interpolate
# import pylab as pl
# #创建数据点集并绘制
# pl.figure(figsize=(12,9))
# x = np.linspace(0, 10, 11)
# y = np.sin(x)
# ax=pl.plot()
#
# pl.plot(x,y,'ro')
# #建立插值数据点
# xnew = np.linspace(0, 10, 101)
# for kind in ['nearest', 'zero','linear','quadratic']:
#     #根据kind创建插值对象interp1d
#     f = interpolate.interp1d(x, y, kind = kind)
#     ynew = f(xnew)#计算插值结果
#     pl.plot(xnew, ynew, label = str(kind))
#
# pl.xticks(fontsize=20)
# pl.yticks(fontsize=20)
#
# pl.legend(loc = 'lower right')
# pl.show()

df = pd.DataFrame({"date":[1997,1998,1999,2000,2001,2002,2003],
                   "Hainan,Total_co2":[7.2,10.4,8.1,8.7,9.2,np.NaN,15.6]})
print(df)
print(df.interpolate())