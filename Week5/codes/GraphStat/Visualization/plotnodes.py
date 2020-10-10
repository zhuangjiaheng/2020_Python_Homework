#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: plotnodes.py.py
#@Software: PyCharm

import matplotlib.pyplot as plt
from GraphStat.NetworkBuilder import Stat

def plot_nodes_attr(attr_dict,feature,type_dict=None):
    Dict = Stat.get_attr_distribution(attr_dict,feature)
    print(Dict)
    # print(sorted(Dict.values()))
    # plt.plot(list(range(34283)),Dict.values())
    # plt.show()
    color_dict = {"starring":"red","writer":"green",
                  "director":"purple","movie":"blue"}
    haslegend = {"starring":0,"writer":0,
                  "director":0,"movie":0}
    #attr_dict根据类型处理成可直接画图的结构
    if feature in ['type', 'country']:        #定性分类数据
        plt.bar(Dict.keys(), Dict.values())
        for a, b in zip(Dict.keys(), Dict.values()):
            plt.text(a, b + 0.05, f"{b}", ha='center', va='bottom', fontsize=10)

        plt.xlabel(feature, fontsize=14)
        plt.ylabel("Counts", fontsize=14)
        plt.title(f"{feature} distribution", fontsize=14)
    elif feature in ['weight']:               #定量数据
        for key in Dict.keys():
            temp_type = type_dict[str(key)]
            print(key,Dict[key],temp_type)
            if haslegend[temp_type] == 0:
                plt.scatter(key, Dict[key],s=5,
                            color=color_dict[temp_type],label=temp_type)
                haslegend[temp_type] = 1
                continue
            plt.scatter(key, Dict[key], s=5,
                        color=color_dict[temp_type])
        #Dict (Vid,Vattr)  typedict ("Vid",Vtype)
        plt.xlabel("Points", fontsize=14)
        plt.ylabel(feature, fontsize=14)
        plt.title(f"{feature} distribution", fontsize=14)
        plt.legend()
    plt.show()
