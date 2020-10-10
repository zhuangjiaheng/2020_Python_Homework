#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: node.py.py
#@Software: PyCharm

def init_node(information):
    '''
    Return  a dictionary, key is the attribute name of node
    while the item is the data of attribute
    (返回字典，key为节点的属性，值为对应的属性值)

    :param information: One specify line in the txt
    :return: a dictionary with attributes of a node
    '''
    node_dict = {}
    attr_list = ["Vid","Vname","Vweight","Vtype","Vothers"]
    for i in range(len(attr_list)):
        node_dict[attr_list[i]] = information[i]
    return node_dict


def _get_attr_(node, key):
    '''
    To get the attribute of a word(获取节点的属性)

    :param node: the dictionary of the node
    :param key: the attribute of the node
    :return: the node's attribute value
    '''
    return node[key]

def get_attr(nodes_dict,attr='Vtype'):
#获取对应的节点属性
    attr_dict = {}
    for node in nodes_dict:
        attr_dict[_get_attr_(node,'Vid')] = _get_attr_(node,attr)
    return attr_dict

def print_node(node,show_others=True):
    '''
    #显示节点全部信息（利用format或者f函数）

    :param node:
    :param show_others:
    :return:
    '''
    print("Id:{Vid}\tName:{Vname}\tWeight:{Vweight}\tType:{Vtype}"
          .format(**node))
    if show_others == True:
        print("\t\tOthers：",node["Vothers"])


