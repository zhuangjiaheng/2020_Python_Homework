#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: RelationNetwork.py
#@Software: PyCharm

# 项目中可能存在的bug：原文长度没有39,预测出来的内容在大于原文长度小于39的位置有
# 这里暂时放得是完整的602个单词
# 有向图的顺序可能有点问题,但貌似是最初的文件就有问题
#{"em1Text": "Iceland", "em2Text": "Reykjavik", "label": "/location/country/capital"}

import json
import torch
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import time
from tqdm import tqdm
from memory_profiler import profile



class RelationNetwork:
    def __init__(self,path_tag,path_text,path_rel):
        self.__path = path_tag
        self.__text = path_text
        self.__rel = path_rel
        #self.__savepth = ""

    # def save_path(self,save_path):
    #     self.__savepth = save_path

    def __append_dict(self,dict,key,value):
        if value not in dict.values():
            dict[key] = value

    def __search_rel_name(self,num):
        for r in self.__rel:
            if int(r.split()[1]) == num:
                break
        if num // 10 == 0:
            return r.split()[0][:-2]
        elif num // 10 == 1:
            return r.split()[0][:-3]

    def __node_process(self,d_tuple,text):
        '''
        将单词进行合并
        :param d_tuple: 原始的二维关系标签组
        :param text: 原文列表
        :return: (字符串标签,关系代号)二维数组,标签列表
        '''
        idex = np.lexsort([d_tuple[:,1]])  # 按照关系代号排序
        d_tuple = d_tuple[idex, :]
        #print("hello",d_tuple)


        label_dict = {}
        temp_str = []  # 存放已经出现在label_dict中的实体名
        node_num = 0   # 生成标准图的字典键
        i=0
        array = []
        while i < len(d_tuple):
            #print("i=",i,"node_num=",node_num)
            if i == len(d_tuple)-1: # 最后一位
                if d_tuple[i][1] != d_tuple[i-1][1]:
                    #self.__append_dict(label_dict,f"Node{node_num}",text[d_tuple[i][0]])
                    if text[d_tuple[i][0]] not in temp_str:  # 最后一个不需要再放入temp_str中
                        node_num += 1
                        label_dict[f"Node{node_num}"] = text[d_tuple[i][0]]
                    array.append(list([text[d_tuple[i][0]], d_tuple[i][1]])) #不用字典是因为node_num不好控制
            else:
                if d_tuple[i][1] == d_tuple[i+1][1]:
                    #if text[d_tuple[i][0]] + ' ' + text[d_tuple[i+1][0]] not in label_dict.values():
                    if text[d_tuple[i][0]] not in temp_str:
                        node_num += 1
                        label_dict[f"Node{node_num}"] = text[d_tuple[i][0]] + ' ' + text[d_tuple[i+1][0]]
                        temp_str.extend([text[d_tuple[i][0]],text[d_tuple[i+1][0]]])

                    array.append(list([text[d_tuple[i][0]] + ' ' + text[d_tuple[i+1][0]], d_tuple[i][1]]))
                    i += 1   # 等所有操作都完成后才能改变索引位置
                else:
                    if text[d_tuple[i][0]] not in temp_str:
                        node_num += 1
                        label_dict[f"Node{node_num}"] = text[d_tuple[i][0]]
                        temp_str.append(text[d_tuple[i][0]])
                    array.append(list([text[d_tuple[i][0]], d_tuple[i][1]]))
            i += 1

        return array,label_dict

    def __relation_process(self,d_tuple):
        '''
        抽取关系,转化为绘图所需的结构
        :param d_tuple: (字符串标签,关系代号)二维数组[按照标签序号排好序]
        :param rel 完整的关系,不同关系列表,一个关系一个字符串
        :return: (字符串1,字符串2,关系代号)
        '''
        #print(d_tuple)
        edges = []
        for i in range(0,len(d_tuple),2):
            row_1 = d_tuple[i][0]        # 第一个实体
            row_2 = d_tuple[i+1][0]      # 第二个实体
            row_3 = d_tuple[i][1]        # 关系代号
            row_4 = self.__search_rel_name(row_3)  # 关系内容
            #print(row_1,row_2,row_4)
            edges.append(list([row_1,row_2,row_3,row_4]))
        return edges

    def __getkey(self,d,value):
        return [k for k, v in d.items() if v == value][0]
        # 此处可以保证一个单词只对应一个node


    #@profile
    def lazy_vis(self):
        with open(self.__path, 'r') as f:
            data = json.load(f)
        with open(self.__text, 'r') as f:
            self.__text = json.load(f)
        with open(self.__rel, 'r') as f:
            self.__rel = f.read().splitlines()
            # for r in rel:
            #     print(r.split()[0][:-2])

        def vis(*args,label_show = True,save_pth = "../images/1.png"):
            #G = nx.DiGraph()
            # plot the networkx
            G = nx.MultiDiGraph()
            bar = tqdm(list(args))

            for sen in bar:
                bar.set_description("Now get sen " + str(sen))
                d_tuple = torch.tensor(data[sen]).nonzero()
                d_tuple = d_tuple.numpy()
                text = self.__text[sen].split()   # 成功访问到self？
                print(d_tuple,text)
                array,label_dict = self.__node_process(d_tuple,text)
                print(array,label_dict)
                edges = self.__relation_process(array)
                #print(edges,"hello")

                for e in edges:
                    G.add_edge(e[0],e[1],ind=e[2],name=e[3])

                time.sleep(1)

            #pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes
            #pos = nx.spring_layout(G, scale=3)           #标准布局
            pos = nx.circular_layout(G)
            nx.draw(G,pos,node_color = '#31ECA8')
            for p in pos:  # raise text positions
                pos[p][1] += 0.07
            nx.draw_networkx_labels(G, pos,font_size=10)

            edge_labels = {}   # 用来整合edge_dict信息

            if label_show == True:
                edge_dict = nx.get_edge_attributes(G, 'name')
            else:
                edge_dict = nx.get_edge_attributes(G, 'ind')

            for k,v in edge_dict.items():
                if k[-1] == 0:
                    edge_labels[k[:2]] = str(v)
                else:
                    edge_labels[k[:2]] = edge_labels[k[:2]] + '\n' + str(v)
            #print(edge_dict,edge_labels)


            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.savefig(save_pth)
            plt.show()



        return vis

# C = RelationNetwork('../data/test_relation_part.json',
#                     '../data/test_text.json',
#                     '../data/relation_label_tag.txt')
# f = C.lazy_vis()
# f(0)
# #f(0,1,2,4,5,6,29,label_show=False,save_pth="../images/1.png")
# # 含有I的是有问题的 如3,