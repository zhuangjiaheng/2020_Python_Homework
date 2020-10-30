#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: ImageShop.py
#@Software: PyCharm

import os
from PIL import Image,ImageFilter
import matplotlib.pyplot as plt


class Filter:
    def __init__(self):
        self.img = None

    def load(self,path,has_filter=0):
        # 首次
        #print("load:",has_filter)
        if not has_filter:
            self.img = Image.open(path)
        # 否则从result中读取
        else:
            file_name = os.path.basename(path)
            file_dir = os.path.dirname(path)
            new_path = os.path.join(file_dir, "result")
            new_path = os.path.join(new_path, file_name)
            self.img = Image.open(new_path)
        return self.img

    def save(self,path):
        file_name = os.path.basename(path)
        file_dir = os.path.dirname(path)
        #new_name = os.path.splitext(file_name)[0] + "_c" + os.path.splitext(file_name)[1]
        new_path = os.path.join(file_dir, "result")
        new_path = os.path.join(new_path,file_name)
        print(new_path," saved!")
        self.img.save(new_path)


    def filter(self):
        pass

class Contour(Filter):  #边缘提取
    def filter(self):
        self.img = self.img.filter(ImageFilter.CONTOUR)
        return self

class Blur(Filter):  #模糊效果
    def filter(self):
        self.img = self.img.filter(ImageFilter.BLUR)
        return self

class Sharpen(Filter):
    def filter(self):
        self.img = self.img.filter(ImageFilter.SHARPEN)
        return self

class SquareAdj(Filter):
    def __init__(self,length,width):
        super(SquareAdj, self).__init__()
        self.length = length
        self.width = width
    def filter(self):
        self.img.thumbnail((self.length,self.width))
        return self

class ImageShop:
    has_filter = 0
    def __init__(self, format_, package):
        self.format_ = format_
        self.package = package
        self.path_list = []
        self.img_list = []
        self.result_list = []


    def load_images(self):
        #img = Filter()
        listdir_ = os.listdir(self.package)
        for dir_ in listdir_:
            if dir_[-len(self.format_):] == self.format_:  # 符合条件的文件
                path = os.path.join(self.package, dir_)
                #self.img_list.append(img.load(path))  #可以换地方?
                self.path_list.append(path)   # 构建输入的图片列表
        return self.path_list


    def __batch_ps(self,path_list,key,*args):
        #构建过滤子类的字典
        filter_dict = {"Contour":Contour(),"Blur":Blur(),
                       "Sharpen":Sharpen(),"SquareAdj":SquareAdj(3968,2976)}
        if args:
            #print("args=",args)
            filter_dict["SquareAdj"] = SquareAdj(args[0],args[1])

        f = filter_dict[key]    #根据关键字选择合适的过滤子类
        #print(f.__dict__)
        #print(path_list)

        for path in path_list:

            if self.has_filter:
                f.load(path, self.has_filter)
            else:
                self.img_list.append(f.load(path,self.has_filter))
            Img = f.filter()   # Img为特定处理后的图片对象
            Img.save(path)
            self.result_list.append(Img.img)  #result_list存放处理后的图像
        self.has_filter = 1


    def batch_ps(self,path_list,Contour=False,Blur=False,
                 Sharpen=False,SquareAdj=None):
        if Blur:
            self.__batch_ps(path_list,"Blur")
        if Sharpen:
            self.__batch_ps(path_list,"Sharpen")
        if Contour:
            self.__batch_ps(path_list,"Contour")
        if SquareAdj:
            config = list(SquareAdj)
            self.__batch_ps(path_list,"SquareAdj",*config)   # SquareAdj: tuple

        if Blur == False and Sharpen== False and Contour== False \
            and SquareAdj == None:  # 导入导出不进行任何操作
            Img = Filter()
            for path in path_list:
                if self.has_filter:
                    Img.load(path, self.has_filter)
                else:
                    self.img_list.append(Img.load(path, self.has_filter))
                Img.save(path)
                self.result_list.append(Img.img)  # result_list存放处理后的图像
            self.has_filter = 1

    # def display(self,nrow,ncol,max_img=6,*args,**kwargs):
    #     path_list = self.load_images()
    #     path_list = path_list[:max_img]
    #
    #     method = args  # filter_operator
    #     filter_dict = {"Contour":False,"Blur":False,"Sharpen":False}
    #     print("method",method)
    #     for i in method:
    #         filter_dict[i] = True
    #     print(path_list,filter_dict,kwargs)
    #     self.batch_ps(path_list,**filter_dict,SquareAdj=(kwargs["length"],kwargs["width"]))
    #
    #     plt.figure(figsize=(3*ncol, 2*nrow))  # 设置窗口大小
    #     plt.suptitle(f"Display_{method}_Image")     # 图片名称
    #     for i in range(len(path_list)):
    #         plt.subplot(nrow, ncol, 1);plt.title('image')

    def display(self,nrow,ncol,max_img=6):
        plt.figure(figsize=(3*ncol, 2*nrow))  # 设置窗口大小
        plt.suptitle(f"Display_Image")     # 图片名称
        rlt_list = self.result_list[:max_img]
        for i in range(len(rlt_list)):
            plt.subplot(nrow, ncol, i+1);plt.title(f"image{i+1}")
            plt.imshow(rlt_list[i]);plt.axis('off')
        plt.show()


class TestImageShop(ImageShop):
    # 沿用父类的所有属性


    # 将图片转化为RGB
    def __make_regalur_image(self,img, size=(64, 64)):
        gray_image = img.resize(size).convert('RGB')
        return gray_image

    # 计算直方图
    def __hist_similar(self,lh, rh):
        assert len(lh) == len(rh)
        hist = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)
        return hist

    # 计算相似度
    def __calc_similar(self,li, ri):
        li = self.__make_regalur_image(li)
        ri = self.__make_regalur_image(ri)
        calc_sim = self.__hist_similar(li.histogram(), ri.histogram())
        return calc_sim

    def similar_test(self,start):
        img_num = len(self.img_list)
        li = self.img_list[start]
        ri_list = self.result_list[start::img_num]
        for ri in ri_list:
            print(self.__calc_similar(li, ri))



    def test(self,nrow,ncol,max_img=9,*args):
        filter_dict = {"Contour": False, "Blur": False, "Sharpen": False}
        path_list = self.load_images()
        for tup in args:
            op = tup[0]; param = tup[1]
            filter_dict[op] = True
        #print(filter_dict)
        self.batch_ps(path_list,**filter_dict,SquareAdj=param)
        #self.display(nrow, ncol, max_img)
        self.similar_test(1)  #第0图


T = TestImageShop("jpg","../images/batch4")
T.test(3,3,9,("Contour",None))
#("Contour",None)

