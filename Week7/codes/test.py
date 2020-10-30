#-*- coding=utf-8 -*-
#@Time:
#@Author: zjh
#@File: test.py
#@Software: PyCharm

from PIL import Image
# 将图片转化为RGB
def make_regalur_image(img, size=(64, 64)):
    gray_image = img.resize(size).convert('RGB')
    return gray_image

# 计算直方图
def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    hist = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)
    return hist

# 计算相似度
def calc_similar(li, ri):
    calc_sim = hist_similar(li.histogram(), ri.histogram())
    return calc_sim


img1 = Image.open("../images/batch3/img1.jpg")
img_1 = Image.open("../images/batch3/result/img1.jpg")
img1.show()
img_1.show()


img1 = make_regalur_image(img1)
img_1 = make_regalur_image(img_1)

print(calc_similar(img1, img_1))
print(calc_similar(img1, img1))