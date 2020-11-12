#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: os_path.py
#@Software: PyCharm

import os
filepath = "../image/1.txt"
if not os.path.isdir(filepath):
    print("no exist")
    os.makedirs(os.path.dirname(filepath))