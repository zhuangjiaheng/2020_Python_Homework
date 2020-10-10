#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: test.py
#@Software: PyCharm


# import pickle
# import networkx as nx
#
# dg = nx.Graph()
# dg.add_edge('a', 'b')
# dg.add_edge('a', 'c')
# dg.add_edge('a', 'd')
# dg.add_edge('b', 'e')
# print (dg.edges())
#
# pickle.dump(dg, open('graph.txt', 'wb'))
# dg2 = pickle.load(open('graph.txt','rb'))
#
# print(dg == dg2)
# print(dimpg.degree == dg2.degree)
# print(dg.degree)
# print(dg2.degree)


import numpy as np
from GraphStat.NetworkBuilder import Graph
import matplotlib.pyplot as plt
import networkx as nx


G = Graph.load_graph("myGraphInfo.p")
nx.draw(G)

# Edges = nx.edges(G)
# i=0
# for edge in Edges:
#     if i<=20 :
#         i+=1
#         print(edge[0],edge[1])   #str
