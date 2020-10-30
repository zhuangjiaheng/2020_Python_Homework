#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: pillow_test.py
#@Software: PyCharm


from PIL import Image,ImageFilter

# ===============基本操作===============
# 1.加载图片
image1 = Image.open('images/image1.jpg')

# 2.显示图片
#image1.show()

# 3.保存图片
#image1.save('aaa.jpg')

# ===============滤镜效果================
# # 1. 添加系统滤镜
# # 图片对象.filter(滤镜效果)  -- 返回一个新的图片对象
# # 浮雕效果
# image2 = image1.filter(ImageFilter.EMBOSS)
# image2.show()
# image2.save('images/bbb.jpg')
#
# #铅笔画
# image3 = image1.filter(ImageFilter.CONTOUR)
# image3.show()
#
# #模糊效果
# image4 = image1.filter(ImageFilter.BLUR)
# image4.show()
#
# #瑞华效果
# image5 = image1.filter(ImageFilter.EDGE_ENHANCE)
# image5.show()
#
# #=============自定义滤镜效果==============
# class MYFILTER(ImageFilter.BuiltinFilter):
#     name = "My-filter"
#     filterargs = (3, 3), 2, 0, (
#         -1, -1, -1,
#         -1, 9, -1,
#         -1, -1, -1
#         )
#     # 3x3不要动,其他参数都可以修改
#
# image6 = image1.filter(MYFILTER)
# image6.show()

# ============ 图片剪切 =============
# # 1.加载图片
# image1 = Image.open("images/image1.jpg")
# # 2.图片剪切
# # crop范围 坐标系:左上角作为原点,向右下增加
# # 范围(x1,y1,x2,y2) 左上角点1,右下角点2
# image7 = image1.crop((1349,1153,2973,2190))
# image7.show()

# ============ 图片粘贴 =============
# # 1. 准备图片
# image8 = Image.open("images/image8.jpg")
#
# # 2. 图片粘贴
# # 图片1.paste(图片2,位置)
# image1.paste(image8,(0,0))
# image1.show()  #粘贴直接修改原图
#
# # 3. 图片拼接
# # 创建空白图
# # new(模式,大小,颜色)
# # 模式 - 'RGB'/'RGBA'
# # 颜色 - (红绿蓝),黑色全0,白色全255
# empty = Image.new('RGB',(5952,3968),(255,255,255))
#
#
# image9 = Image.open('images/image9.jpg')
# image10 = Image.open('images/image10.jpg')
#
# empty.paste(image9,(0,0))
# empty.paste(image10,(2976,0))
# empty.show()

# ========== 图片缩放 ===============
# # 1. 加载原图
# # 2. 缩放
# # 图片对象.thumbnail(大小)
# image1.thumbnail((100,100))  #会按图片比例缩放
# image1.show()                #直接修改原图

# ========== 图片镜像 ===============
# # 1. 加载原图
# # 2. 左右镜像
# image_lr = image1.transpose(Image.FLIP_LEFT_RIGHT)
# image_lr.show()
# image_lr.save('images/lr.jpg')
#
# # 3 上下镜像
# image_tb = image1.transpose(Image.FLIP_TOP_BOTTOM)
# image_tb.show()
# image_tb.save('images/tb.jpg')

# ========= 文字水印 ========
# from PIL import ImageFont, ImageDraw
# # 1. 打开图片
# # 2.创建字体对象
# # truetype(字体文件,)
# ImageFont.truetype()

