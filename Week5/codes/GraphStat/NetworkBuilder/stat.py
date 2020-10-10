#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: stat.py.py
#@Software: PyCharm

import networkx as nx
def cal_average_dgree(graph):
    '''
    计算网络中的平均度

    :param graph: Networkx Graph
    :return: average_degree
    '''
    Vnum = nx.number_of_nodes(graph)
    Enum = nx.number_of_edges(graph)
    average_degree = Enum * 2 / Vnum  # 2E/V
    return average_degree


def get_attr_distribution(attr_dict,feature):
    if feature in ['type','country']:    #定性统计量
        count_dict = {}
        for item in attr_dict.values():
            count_dict[item] = count_dict.get(item, 0) + 1
        Dict = count_dict
    elif feature in ['weight']:          #定量统计量
        attr_value = list(map(int, attr_dict.values()))
        attr_key = list(map(int, attr_dict.keys()))
        Dict = dict(zip(attr_key,attr_value))
        #print(Dict)
    return Dict

    pass
def cal_dgree_distribution(graph):
    '''
    计算网络的度分布

    :param graph: Networkx Graph
    :return: degree_distribution
    '''
    return dict(nx.degree(graph))

def cal_relation_distribution(graph,tpye_dict):
    '''
    classify the relationship

    :param graph: the networkx graph
    :param tpye_dict: dict(Vid,Vtype)
    :return: dict with 10 relation
    '''
    relation_dict = {"ww":0,"dd":0,"ss":0,"mm":0,
                     "wd":0,"ws":0,"ds":0,"wm":0,"dm":0,"sm":0,
                     "dw":0,"sw":0,"sd":0,"mw":0,"md":0,"ms":0}
    Edges = nx.edges(graph)
    for edge in Edges:      #str
        v1=edge[0];v2=edge[1]
        relation = tpye_dict[v1][0]+tpye_dict[v2][0]
        relation_dict[relation] += 1
    return relation_dict


def density(relation_dict,tpye_dict):
    tpye_dict = get_attr_distribution(tpye_dict,"type")
    for rlt in relation_dict:
        div = 1
        for v in rlt:
            if v == "w" : div *= tpye_dict["writer"]
            elif v == "s": div *= tpye_dict["starring"]
            elif v == "d": div *= tpye_dict["director"]
            elif v== "m": div *= tpye_dict["movie"]
        relation_dict[rlt] /= div
    return relation_dict
