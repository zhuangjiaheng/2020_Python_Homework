#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: graph.py.py
#@Software: PyCharm

import networkx as nx
import pickle

def init_graph(node_list, edges):
    '''
    返回一个字典，分别存储节点信息和边信息

    :param node_list: all nodes information
    :param edges: all edges information
    :return:
    '''
    G = nx.Graph()                    #创建孔图
    G.add_nodes_from(node_list)       #创建节点

    for edge in edges:
        v1 = edge[0]; v2 = edge[1];
        #weight = eval(edge[2])
        G.add_edge(v1,v2)             #加入边
    return G

def save_graph(graph):
    pickle.dump(graph, open("../data/myGraphInfo.p", "wb"))
    #nx.write_gpickle(graph, "E:\\大三上2020秋\\1 现代程序设计技术\\Homework\\Week5\\data\\myGraphInfo.p")
    print("Graph Already Saved!")

def load_graph(filename):
    loaded_info = pickle.load(open("../data/"+filename,"rb"))
    #loaded_info = nx.read_gpickle(filename)
    print("Graph Already Loaded!")
    return loaded_info
