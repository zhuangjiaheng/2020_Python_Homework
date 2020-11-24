#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: visualization.py
#@Software: PyCharm

import os
import abc
from nltk.corpus import stopwords
from tqdm import tqdm

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image,JpegImagePlugin
from wordcloud import WordCloud
import imageio

from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

import librosa.display
import cv2





class Plotter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def plot(self,data,*args,**kwargs):
        pass


class Point:
    def __init__(self,x,y,*args):
        self.x = x
        self.y = y
        if args != ():    # 空元组
            self.z = args[0]

class PointPlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        #print(data)
        if hasattr(data, 'z'):
            self.x = data.x
            self.y = data.y
            self.z = data.z
            ax = plt.subplot(111, projection='3d')
            ax.scatter(self.x, self.y, self.z, *args,**kwargs)

            ax.set_zlabel('Z')
            ax.set_ylabel('Y')
            ax.set_xlabel('X')
            plt.title("PointPlot")
        else:
            self.x = data.x
            self.y = data.y
            plt.scatter(self.x,self.y,*args,**kwargs)
        plt.show()


class ArrayPlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        dim = len(data)
        n_components = 3
        if dim >= n_components:
            pca = PCA(n_components=n_components)
            data_pca = pca.fit_transform(data.transpose())
            #print(type(data_pca))
            #print("data_pca=",data_pca)
            self.x = [row[0] for row in data_pca]
            self.y = [row[1] for row in data_pca]
            self.z = [row[2] for row in data_pca]
            ax = plt.subplot(111, projection='3d')
            ax.set_zlabel('Z')
            ax.set_ylabel('Y')
            ax.set_xlabel('X')
            ax.scatter(self.x, self.y, self.z, *args,**kwargs)
        else:
            self.x = data[0]
            self.y = data[1]
            plt.scatter(self.x,self.y,*args,**kwargs)
        plt.title("ArrayPlot")
        plt.show()

class TextPlotter(Plotter):

    def _get_tfidf_keyword(self,texts,max_word):
        stop_words = stopwords.words('english')
        tfidf = TfidfVectorizer(max_features=max_word,stop_words=stop_words)  # 默认值
        weight = tfidf.fit_transform(texts).toarray()
        word = tfidf.get_feature_names()
        #print(weight,len(weight),word,len(word))
        word_fre = {}
        for i in range(len(weight)):     # 几段文本
            for j in range(len(word)):
                if word[j] not in word_fre:
                    word_fre[word[j]] = weight[i][j]
                else:
                    word_fre[word[j]] = max(word_fre[word[j]], weight[i][j])
        #print(word_fre)
        return word_fre

    def plot(self,texts,*args,**kwargs):
        max_word = kwargs['max_word']
        word_fre = self._get_tfidf_keyword(texts,max_word)
        word_cloud = WordCloud(
                mask=np.array(Image.open("../data/mask.png")),
                font_path="msyh.ttc",
                background_color="white",
                max_font_size=70,
                max_words= max_word,
                width=500,height=500)
        word_cloud.fit_words(word_fre)
        word_cloud.generate_from_frequencies(word_fre)
        plt.imshow(word_cloud)
        plt.xticks([])  # 去掉横坐标
        plt.yticks([])  # 去掉纵坐标
        plt.show()


class ImagePlotter(Plotter):
    def plot(self,data,nrow,ncol,max_img=6,*args,**kwargs):
        plt.figure(*args,**kwargs)
        plt.suptitle(f"ImagePlotter{nrow}x{ncol}")
        for i in range(len(data[:max_img])):
            plt.subplot(nrow,ncol,i+1)
            plt.imshow(data[i])
            plt.axis('off')
        plt.show()

class GifPlotter(Plotter):
    def plot(self,data,*args,**kwargs):

        gif_images = []
        #print(data)
        bar = tqdm(data)
        for path in bar:
            #bar.set_description("Now get pic " + path)
            gif_images.append(imageio.imread(path))
        imageio.mimsave("test_mini.gif", gif_images, **kwargs)


class SoundPlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        y, sr = librosa.load(path=data, *args,**kwargs)
        #print(y,sr)
        librosa.display.waveplot(y, sr=sr)
        plt.show()

class VideoPlotter(Plotter):
    def plot(self,data,*args,**kwargs):

        i = 0
        while (data.isOpened()):
            ret, frame = data.read()
            if ret == False:
                break

            img_file = "../data/mp4_img"
            if not os.path.exists(img_file):
                os.mkdir(img_file)
            cv2.imwrite(img_file + "/" + str(i) + '.jpg', frame)
            i += 1
        data.release()
        cv2.destroyAllWindows()


        gp = GifPlotter()
        gif_ipth_list = os.listdir(img_file)
        for i in range(len(gif_ipth_list)):
            gif_ipth_list[i] = os.path.join(img_file, gif_ipth_list[i])
        gp.plot(gif_ipth_list,fps=200)

class Adapter:
	def __init__(self,adp_obj,adp_methods):
		self.obj=adp_obj
		self.__dict__.update(adp_methods)

	def __str__(self):
		return str(self.obj)


class ProxyPlot():
    def __init__(self,data):
        self.data = data

    def get_adapter_type(self):
        try:
            if isinstance(self.data,Point):
                self.type = 'point'
            elif isinstance(self.data,np.ndarray):
                self.type = 'array'
            elif isinstance(self.data,str):
                if os.path.splitext(self.data)[-1] in \
                    ['.mp3','.wma','.rm','.wav','.mid']:
                    self.type = 'sound'
            elif isinstance(self.data,cv2.VideoCapture):
                self.type = 'video'
            elif isinstance(self.data,list):
                if isinstance(self.data[0],JpegImagePlugin.JpegImageFile):
                    self.type = 'image'
                elif isinstance(self.data[0],str):
                    if os.path.splitext(self.data[0])[-1] in \
                        ['.jpg','.png','.jpeg','.bmp']:
                        self.type = 'gif'
                    # elif os.path.splitext(self.data[0])[-1] in \
                    #     ['.mp3','.wma','.rm','.wav','.mid']
                    #     self.type = 'sound'
                    else:
                        self.type = 'text'
            return self.type
        except:
            print("we can't print the data, plz check whether the data structure is valid")
            print("valid data structure : Point / Array / Text / Img / Sound / file of Img or Sound")
            exit()


if __name__ == "__main__":
    iris = load_iris()

    with open("../data/timberline.txt") as f:
        texts1 = f.read().splitlines()
    with open("../data/ChinesePottery.txt") as f:
        texts2 = f.read().splitlines()

    img_dir = "../data/img_list"
    ipth_list = os.listdir(img_dir)
    i_list = []
    for i in ipth_list:
        i = os.path.join("../data/img_list", i)
        i_list.append(Image.open(i))

    gif_dir = "../data/img_series"
    gif_ipth_list = os.listdir(gif_dir)
    for i in range(len(gif_ipth_list)):
        gif_ipth_list[i] = os.path.join("../data/img_series", gif_ipth_list[i])


    dataset = list([Point(1,1,1),Point(2,2),
                    np.transpose(iris.data),np.array([[1,2,3,4],[5,6,7,8]]),
                    texts1,texts2,
                    i_list,
                    gif_ipth_list,
                    "../data/Franz_Liszt_Dream_Of_Love.mp3",
                    cv2.VideoCapture('../data/snow.mp4')
                   ])



    adapter_dict = {'point':dict(plot=PointPlotter().plot),  # 实例化
                    'array':dict(plot=ArrayPlotter().plot),
                    'text':dict(plot=TextPlotter().plot),
                    'image':dict(plot=ImagePlotter().plot),
                    'gif':dict(plot=GifPlotter().plot),
                    'sound':dict(plot=SoundPlotter().plot),
                    'video':dict(plot=VideoPlotter().plot)}


    #print(dataset)
    data = dataset[-1]
    proxy = ProxyPlot(data)
    mode = proxy.get_adapter_type()
    proxy = Adapter(proxy, adapter_dict[mode])
    #proxy.plot(data,offset=128,duration=5)
    proxy.plot(data)





# pp = PointPlotter()
# p = Point(1,1,1)
# proxy = ProxyPlot(p)
# print(isinstance(proxy.data,Point))
# proxy = Adapter(proxy,dict(plot=pp.plot))
# proxy.plot(p,c='g')

# iris = load_iris()
# data = np.transpose(iris.data)
# #data = [[1,2,3,4],[5,6,7,8]]
# ap = ArrayPlotter()
# proxy2 = ProxyPlot(data)
# print(isinstance(proxy2.data,np.ndarray))
# proxy2 = Adapter(proxy2,dict(plot=ap.plot))
# proxy2.plot(data)


# with open("../data/timberline.txt") as f:
#     texts = f.read().splitlines()
# tp = TextPlotter()
# proxy3 = ProxyPlot(texts)
# print(isinstance(proxy3.data[0],str))
# proxy3 = Adapter(proxy3,dict(plot = tp.plot))
# tp.plot(texts,max_word=200)


# img_dir = "../data"
# ipth_list = os.listdir(img_dir)
# i_list = []
# for i in ipth_list:
#     i = os.path.join("../data", i)
#     i_list.append(Image.open(i))
# print(i_list)

# ip = ImagePlotter()
# proxy4 = ProxyPlot(i_list)
# print(isinstance(proxy4.data[0],JpegImagePlugin.JpegImageFile))
# proxy4 = Adapter(proxy4,dict(plot=ip.plot))
# proxy4.plot(i_list,nrow=2,ncol=2,max_img=4)


# gp = GifPlotter()
# gif_dir = "../data/img_series"
# gif_ipth_list = os.listdir(gif_dir)
# for i in range(len(gif_ipth_list)):
#     gif_ipth_list[i] = os.path.join("../data/img_series", gif_ipth_list[i])
# proxy5 = ProxyPlot(gif_ipth_list)
# proxy5 = Adapter(proxy5,dict(plot=gp.plot))
# proxy.plot(gif_ipth_list,fps=100)


# sound_pth = "../data/Franz_Liszt_Dream_Of_Love.mp3"
# print(os.path.splitext(sound_pth)[-1],os.path.splitext(sound_pth)[-1] == '.mp3')
# sp = SoundPlotter()
# proxy6 = ProxyPlot(sound_pth)
# proxy6 = Adapter(proxy6,dict(plot=sp.plot))
# proxy6.plot(sound_pth,duration=341)


#os.path.splitext(file)[-1]






