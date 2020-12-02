# -*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: MyMapReduce.py
# @Software: PyCharm

import os,time
import jieba
import json
import collections
from multiprocessing import Pool,Manager,Process


def frequency(word_list):
    """
    cal the frequency for each word from a word list
    :param word_list: a list contains each word in the text
    :return: an ordered dictionary with word and its frequency
            by desc in a text
    """
    WordDict = {}
    for c in word_list:
        if c in WordDict.keys():
            WordDict[c] += 1
        else:
            WordDict[c] = 1
    WordFreq = collections.OrderedDict(sorted(WordDict.items(), key=lambda dc:dc[1],
                                              reverse=True))
    return WordFreq


def map(q,folder_name,file_name,stopword):
    '''
    word frequency analysis, turn a path into an ordered dictionary
    the first step of MapReduce work: split
    :param folder_name: the folder name of the texts
    :param file_name: the text name (a text)
    :param stopword: import from a txt file
    :return: put the ordered dictionary with word frequency into the queue
    '''
    #print(f"{folder_name}/{file_name}")
    with open(os.path.join(folder_name, file_name), "r", encoding="utf-8") as f:
        text = f.read()
    txt_list = jieba.lcut(text)
    # text_list = list()
    # for word in txt_list:
    #     if word not in stopword:
    #         text_list.append(word)
    word_freq = frequency(txt_list)
    q.put(word_freq)

    #print(f"[{file_name}] mapped! -- by {os.getpid()}")

def reduce(q,length):
    """
	get the freq_dict from the map process
    :param q: a queue for delivering information
    :param length: the number of texts
    :return: a dictionary
    """
    dictionary = {}
    count_ok_text = 0
    while True:
        #print("now:",count_ok_text,"  already done:{:.2f}%".format(count_ok_text/length*100))
        td = q.get()
        for key, value in td.items():
            if key in dictionary.keys():
                dictionary[key] += value
            else:
                dictionary[key] = value
        count_ok_text += 1
        if count_ok_text >= length:
            break

    # dictionary = collections.OrderedDict(sorted(dictionary.items(), key=lambda dc: dc[1],
    #                                             reverse=True))

    # json.dump(dictionary, open("word_frequency.json", 'w'))

    # wd = ""
    # for key,value in dictionary.items():
    #     wd = wd + str(key) + "\t" + str(value) + "\n"
    #
    # with open("word_frequency.txt","w",encoding="utf-8") as f:
    #     f.write(wd)

    # print(dictionary)

def main(process_num):
    # find the file
    folder_name = "../texts/THUCN"
    file_names = os.listdir(folder_name)
    # print(file_names)
    # create the stopword
    with open("../texts/stopwords_list.txt", "r", encoding="utf-8") as f:
        stopword = f.read().splitlines()
    stopword.append("\n")

    # create a queue
    q = Manager().Queue()
    # create a process pool
    mpo = Pool(process_num)
    #
    for file_name in file_names:
        mpo.apply_async(map, args=(q, folder_name, file_name, stopword,))

    r = Process(target=reduce, args=(q, len(file_names),))
    r.start()

    mpo.close()
    mpo.join()
    #r.close()
    r.join()

if __name__ == "__main__":
    start = time.time()
    main(6)
    period = time.time() - start
    print("period",period)
    # start = time.time()
    # main(10)
    # period = time.time() - start
    # print("period",period)

