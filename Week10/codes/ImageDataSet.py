#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: ImageDataSet.py
#@Software: PyCharm

import os
from PIL import Image
import numpy as np

# pixel = 350 x 350
class Faces:
	def __init__(self,dirname):
		self._dirname = dirname
		self._imglist = os.listdir(dirname)
		#print(os.path.join(dirname,self._imglist[0]))

	def load_image(self,name):
		path = os.path.join(self._dirname,name)
		print(path)
		return Image.open(path)

	def image2array(self,img):
		im2arr = np.array(img)
		#print(im2arr.shape,im2arr.size)
		return im2arr


class FaceDataset(Faces):
	def __init__(self,dirname,start=0,step=1,max=2):
		super(FaceDataset, self).__init__(dirname)
		self._start = start
		self._step = step
		self._max = max

	def __iter__(self):
		self._a = self._start
		return self

	def __next__(self):
		if self._a <= self._max:
			ind = self._a
			self._a += self._step
			return Image.open(os.path.join(self._dirname,
										   self._imglist[ind]))
		else:
			raise StopIteration('大于max:{}'.format(self._max))


class FaceDataset2(Faces):
	def __init__(self,dirname,start=0,step=1,max=10):
		super(FaceDataset2, self).__init__(dirname)
		self._start = start
		self._step = step
		self._max = max

	def __iter__(self):
		print(self._a)
		return iter(self._imglist)


# fd = FaceDataset("../FaceImages/Images",start=1,step=3,max=6)
# for x in fd:
# 	print(x)
# 	print(fd.image2array(x))

fd2 = FaceDataset2("../FaceImages/Images")
# for x in fd2:
# 	print(x)
# 	filename = os.path.join("../FaceImages/Images",x)
# 	print(fd2.image2array(Image.open(filename)))

with open("test.txt","w") as f:
	for x in fd2:
		filename = os.path.join("../FaceImages/Images", x)
		img = Image.open(filename)
		f.write(img.__str__()+'\n')
		f.write(str(fd2.image2array(img)))

