#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: map_test.py
#@Software: PyCharm

import os
import jieba
import collections

folder_name = "../texts/THUCN_small"
file_names = os.listdir(folder_name)



def frequency(word_list):
    WordDict = {}
    for c in word_list:
        if c in WordDict.keys():
            WordDict[c] += 1
        else:
            WordDict[c] = 1
    WordFreq = collections.OrderedDict(sorted(WordDict.items(), key=lambda dc:dc[1],
                                              reverse=True))
    return WordFreq


def map(folder_name,file_name,stopword):
    with open(os.path.join(folder_name, file_name), "r", encoding="utf-8") as f:
        text = f.read()
    txt_list = jieba.lcut(text)
    text_list = list()
    for word in txt_list:
        if word not in stopword:
            text_list.append(word)
    print(frequency(text_list))
    #return frequency(text_list)


folder_name = "../texts/THUCN_small"
file_names = os.listdir(folder_name)
print(file_names)
# 创建停用词
with open("../texts/stopwords_list.txt", "r", encoding="utf-8") as f:
    stopword = f.read().splitlines()
stopword.append("\n")

for file_name in file_names:
    d = map(folder_name,file_name,stopword)
    # for key,value in d.items():
    #     print(key,value)