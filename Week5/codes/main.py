#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: main.py
#@Software: PyCharm

import networkx as nx
from GraphStat.Visualization import Plotgraph,Plotnodes
from GraphStat.NetworkBuilder import *

def main():
    '''

    :return:
    '''

    '''build and print the Node dictionary'''
    nodes_dict = []
    with open("../data/newmovies.txt",encoding="UTF-8") as f:
        cursor = int(f.readline().split(" ")[-1])         #读完第一行,游标下移
        txt = f.read().splitlines()
        txt = [t.split("\t") for t in txt]
    for i in range(cursor+1):       #从0开始,到cursor
        nodes_dict.append(Node.init_node(txt[i]))
        #Node.print_node(nodes_dict[i],show_others=False)
    Node.print_node(nodes_dict[0],show_others=True)
    Node.print_node(nodes_dict[11446],show_others=True)
    # for i in range(100):
    #     print(i,nodes_dict[i])


    '''Built and print the graph'''
    node_list = [str(i) for i in range(cursor+1)]
    #print(node_list)
    G = Graph.init_graph(node_list,txt[cursor+2:len(txt)])
    Graph.save_graph(G)
    G = Graph.load_graph("myGraphInfo.p")

    '''Statistic'''
    #print("Degree_Distribution:\n",Stat.cal_dgree_distribution(G))
    print("Average_Degree:\n",Stat.cal_average_dgree(G))
    type_dict = Node.get_attr(nodes_dict, attr='Vtype')
    attr_dict = Node.get_attr(nodes_dict, attr='Vweight')
    #print("Type_Dict:\n",type_dict)
    relation_dict = Stat.cal_relation_distribution(G, type_dict)
    print("Relation_Dict:\n",relation_dict)
    dy = Stat.density(relation_dict,type_dict)
    print("Relation_Density:\n",dy)

    '''Visualization'''
    Plotgraph.plotdgree_distribution(G,log=True)
    Plotnodes.plot_nodes_attr(type_dict,'type')
    #Plotnodes.plot_nodes_attr(attr_dict,'weight',type_dict=type_dict)
    #Plotgraph.plotedge_distribution(relation_dict)
    Plotgraph.plotedge_distribution(dy)

if __name__=='__main__':main()