#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: plt_subplot.py
#@Software: PyCharm

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open("E:\\大三上2020秋\\1 现代程序设计技术\\Homework\\Week7\\images\\batch1\\img1.jpg")
gray = img.convert('L')
r,g,b = img.split()
img_merged = Image.merge('RGB', (r, g, b))

plt.figure(figsize=(20,5)) #设置窗口大小
plt.suptitle('Multi_Image') # 图片名称
plt.subplot(1,2,1), plt.title('image')
plt.imshow(Image.open("../images/batch4/img4.jpg"))
plt.subplot(1,2,2), plt.title('image_small')
plt.imshow(Image.open("../images/batch4/result/img4.jpg"))
plt.show()



plt.figure(figsize=(10,5)) #设置窗口大小
plt.suptitle('Multi_Image') # 图片名称
plt.subplot(2,3,1), plt.title('image')
plt.imshow(img), plt.axis('off')
plt.subplot(2,3,2), plt.title('gray')
plt.imshow(gray,cmap='gray'), plt.axis('off') #这里显示灰度图要加cmap
plt.subplot(2,3,3), plt.title('img_merged')
plt.imshow(img_merged), plt.axis('off')
plt.subplot(2,3,4), plt.title('r')
plt.imshow(r,cmap='gray'), plt.axis('off')
plt.subplot(2,3,5), plt.title('g')
plt.imshow(g,cmap='gray'), plt.axis('off')
plt.subplot(2,3,6), plt.title('b')
plt.imshow(b,cmap='gray'), plt.axis('off')

plt.show()

