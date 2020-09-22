#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: WordEmbedding.py
#@Software: PyCharm


import collections
import numpy as np
import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import pdist   #cosine-dis

#show all
np.set_printoptions(threshold=np.inf)

#show Chinese
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

'''
input:a list,each line is an element in the list
output:a dictionary with word frequency
'''
def getText(filepath):
    with open(filepath,'r',encoding='UTF-8') as f:
        txt=f.readlines()
        #strip the '\n' + lower the string
        txt = [line[:-1].lower() for line in txt]
        return txt

'''
input:a string
output:a list after tokenization
'''
def Tokenization(txt,language):
    if language == 'English' or language == 'english':
        StopWord = getText("../stopwords_list_English.txt")
        txt_split = txt.split()
    elif language == 'Chinese' or language == 'chinese':
        StopWord = getText("../stopwords_list.txt")
        txt_split = jieba.lcut(txt)
    else:
        return None          #Language Error

    txt_list = []            #After Stopword
    #delete the stop_word
    for c in txt_split:
        if c not in StopWord:
            txt_list.append(c)

    return txt_list

'''
input:several list after tokenization
output:an ordered dictionary of word list
'''
def Frequency(Word_list):
    WordDict = {}
    for txt_list in Word_list:
        for c in txt_list:
            if c in WordDict.keys():
                WordDict[c] += 1
            else:
                WordDict[c] = 1
    WordFreq = collections.OrderedDict()
    WordFreq = collections.OrderedDict(sorted(WordDict.items(), key=lambda dc:dc[1],
                                              reverse=True))
    return WordFreq

'''
input:an ordered dictionary of word list
output:bar plot
'''
def BarFreq(WordFreq):
    drawords=[];nums=[]
    items = list(WordFreq.items())
    for i in range(6):
        word, count = items[i]
        drawords.append(word);nums.append(count)
    ind = np.arange(1, 7, 1)
    plt.bar(ind, nums, width=0.75, color='orange',
            alpha=0.9,label='Num of Keyword')
    #mark the number
    for a, b in zip(ind, nums):
        plt.text(a - 0.05, b + 0.1, '%d' % b,
                 ha='center', va='bottom', fontsize=10)
    plt.ylabel('nums')
    plt.xlabel('words')
    plt.title('Word Frequency Bar')
    plt.xticks(ind, drawords)
    plt.legend()
    plt.savefig(r"bar.jpg")

'''
input:a 2d word list:(several sentence, sentence word)
output:Cloud plot
'''
# def CloudFreq(WordList):
#     #Create text based on WordList
#     WordList_f = [word for sentence in WordList for word in sentence]
#     text=" ".join(WordList_f)
#     print(text)
#
#     w=wordcloud.WordCloud(font_path="msyh.ttc",
#                           max_words=25,
#                           width=500,height=500,
#                           background_color="white")
#     w.generate(text)
#     w.to_file("wordcloud.jpg")

'''
input:Word_freq dictionary
output:Cloud plot
'''
def CloudFreq2(WordFreq,language):
    if language == 'English' or language == 'english':
        pic_mask = np.array(Image.open("../image/apple.png"))
    elif language == 'Chinese' or language == 'chinese':
        print("chinese")
        pic_mask = np.array(Image.open("../image/crab.png"))
    wc = WordCloud(background_color="white", max_words=50, mask=pic_mask,
                   font_path="msyh.ttc",width=500,height=500)
    # generate word cloud
    wc.generate_from_frequencies(WordFreq)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


'''
input:Full WordFreq
output:WordFreq with count more than 20
'''
def Frequency_cut(WordFreq):
    WordFreq_ ={}
    for key in WordFreq.keys():
        if WordFreq[key] >= 20:
            WordFreq_[key] = WordFreq[key]
    print(WordFreq_,len(WordFreq_))
    return WordFreq_,len(WordFreq_)

'''
input:WordFreq_dict & 2d Word_list
output:2d WordVector
'''
def Word2Vec(WordFreq,Word_list,language):
    Words = list(WordFreq.keys())
    Sentence_length = len(Word_list)
    Words_length = len(Words)
    WordVector = np.zeros((Sentence_length, Words_length))
    for i in range(Sentence_length):
        WordVector[i] = [1 if c in Word_list[i] else 0
                         for c in Words]
    # test for WordVector
    # for i in range(len(WordVector[0])):
    #     if WordVector[0][i]:
    #         print(Words[i])
    data = pd.DataFrame(WordVector)
    writer = pd.ExcelWriter('../WordVector{:}.xlsx'.format(language))  # 写入Excel文件
    data.to_excel(writer, 'page_1')  # ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()
    print("Vector Already Saved!")
    return WordVector

def jieba_tokenize(text):
    return jieba.lcut(text)
def Word2Vec_Advanced(txt_list,language):
    tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, \
                                       lowercase=False)
    tfidf_matrix = tfidf_vectorizer.fit_transform(txt_list)
    #print(tfidf_vectorizer.get_feature_names())

    data = pd.DataFrame(tfidf_matrix.toarray())
    writer = pd.ExcelWriter('../WordVector{:}.xlsx'.format(language))  # 写入Excel文件
    data.to_excel(writer, 'page_1')  # ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()
    print("Vector Already Saved!")
    return tfidf_matrix.toarray()

'''
input:two vector
output:distance
'''
# def cal_one_distance(x,y):
#     if np.linalg.norm(x)*np.linalg.norm(y) == 0:
#         dist = 1
#     else:
#         dist = 1 - np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
#
#     return dist


def cal_one_distance(x,y):
    #dist = pdist(np.vstack([x, y]), 'cosine')
    dist = np.linalg.norm(x - y)
    return dist

'''
input:WordList:each row is a vector of the sentence
output:a 2d matrix,Adjacency Matrix
'''
def cal_distance(WordVector,language):
    num_of_sen = len(WordVector)
    #num_of_word = len(WordVector[0])
    DisM = np.zeros((num_of_sen,num_of_sen))
    for i in range(num_of_sen):
        for j in range(num_of_sen):
            if i!=j:
                DisM[i][j]=cal_one_distance(WordVector[i],WordVector[j])
            else:
                DisM[i][j]=0
        if i%100 == 0 :
            print("{:} row done!".format(i))
    data = pd.DataFrame(DisM)
    writer = pd.ExcelWriter('../Distance_{:}.xlsx'.format(language))  # 写入Excel文件
    data.to_excel(writer, 'page_1')  # ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()
    print("Distance Already Saved!")
    return DisM


'''
input:DisM
output:index of vector, the text of index
'''
def findCenter(DisM,filepath):
    num_of_sentence = len(DisM)
    cosine_sum = []
    # add by row
    for i in range(num_of_sentence):
        cosine_sum.append(np.nanmean(DisM[i]))
    cosine_sum = np.array(cosine_sum)
    #print(cosine_sum)
    # find the min num and its ind
    ind = np.argmin(cosine_sum)
    print(ind,cosine_sum[ind])
    with open(filepath,'r',encoding='UTF-8') as f:
        txt_ =f.readlines()[ind]
    return txt_


def Cluster(DisM,filepath):
    # 假如我要构造一个聚类数为3的聚类器
    estimator = KMeans(n_clusters=2)  # 构造聚类器
    estimator.fit(DisM)  # 聚类
    label_pred = estimator.labels_  # 获取聚类标签
    centroids = estimator.cluster_centers_  # 获取聚类中心
    inertia = estimator.inertia_  # 获取聚类准则的总和
    txt = getText(filepath)
    #print(txt,inertia)
    ClassifyDict = dict(zip(txt,label_pred))
    return ClassifyDict



def run(filepath,language):
    text=getText(filepath)
    Word_list = []
    for txt in text:
        Word_list.append(Tokenization(txt,language))
    #print(Word_list)
    WordFreq=Frequency(Word_list)
    WordDict,num_of_word=Frequency_cut(WordFreq)
    print(WordDict.keys())
    #
    # #BarFreq(WordFreq)
    # #CloudFreq2(WordFreq,language)
    # WordVector = Word2Vec_Advanced(text,language)
    # #print(WordVector)
    # # WordVector = Word2Vec(WordDict,Word_list,language)
    #
    # DisM=cal_distance(WordVector,language)

    '''load the DisM'''
    # if language == "English" or language == "english":
    #     DisM = pd.read_excel("../Distance_English.xlsx", header=0)
    # elif language == "Chinese" or language == "chinese":
    #     DisM = pd.read_excel("../Distance_Chinese.xlsx", header=0)
    # DisM = DisM.values
    # CenterSen=findCenter(DisM,filepath)
    # print(CenterSen)
    # ClassifyDict = Cluster(DisM,filepath)
    # for key in ClassifyDict.keys():
    #     print(key,ClassifyDict[key])






run("../tweets_apple_stock.txt","English")
#run("../online_reviews_texts.txt","Chinese")