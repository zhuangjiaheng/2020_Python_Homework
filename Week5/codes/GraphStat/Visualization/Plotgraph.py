#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: Plotgraph.py.py
#@Software: PyCharm

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def plotdgree_distribution(graph,log=True):
    '''
    度的分布图
    :param graph: Networkx graph
    :param log: whether log(X-axis) or not
    :return:distribution plot
    '''

    degs = dict(nx.degree(graph))
    degs_list = degs.values()
    if log:
        bin_edges = 10 ** np.arange(0.8, np.log10(max(degs_list)) + 0.1, 0.1)
        plt.hist(degs_list, bins=bin_edges)  # bin控制有几条柱
        plt.xscale('log')
        tick_locs = [10, 30, 100, 300, 1000]
        plt.xticks(tick_locs, tick_locs)
    else:
        plt.hist(degs_list,bins=range(150))

    plt.xlabel("degree", fontsize=14)
    plt.ylabel("frequency", fontsize=14)
    plt.title("degree distribution", fontsize=14)
    plt.show()

def plotedge_distribution(relation_dict):
    redunt = ["dw","sw","sd","mw","md","ms"]
    for s in redunt:
        relation_dict[s[::-1]] += relation_dict[s]
        del relation_dict[s]
    c = lambda relation_list:["pink" if re in ["wm","sm","dm"]
                              else "orange" for re in relation_list]
    plt.bar(relation_dict.keys(),relation_dict.values(),
            color = c(relation_dict.keys()))

    for a, b in zip(relation_dict.keys(), relation_dict.values()):
        plt.text(a, b + 0.05, f"{b}", ha='center', va='bottom', fontsize=8)

    plt.xlabel("relation_type", fontsize=14)
    plt.ylabel("Counts", fontsize=14)
    plt.title("Relation Distribution", fontsize=14)



    plt.show()