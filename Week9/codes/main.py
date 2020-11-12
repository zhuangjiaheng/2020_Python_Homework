#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: main.py
#@Software: PyCharm

import os
from functools import wraps
from playsound import playsound

import RelationNetwork as rn

def check_file(filepath):
    def decorater(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print("@check_file:function_name:",wrapper.__name__)  # 如何给decorater装饰
            #if not os.path.isdir(filepath):
            if not os.path.exists(os.path.dirname(filepath)):
                print("Warining:The input file dir doesn't exist. "+
                      "It's created automatically\n"+
                      f"filepath:{filepath}")
                os.makedirs(os.path.dirname(filepath))
            func(*args,**kwargs)
        return wrapper
    return decorater





def sound(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        #print(kwargs)
        print("@sound:function_name:",wrapper.__name__)
        func(*args,**kwargs)
        playsound("../sound/notice.mp3")
    return wrapper


@sound
@check_file("../images/1.png")
@profile
def main(*args):  #句子序号,一个或多个
    C = rn.RelationNetwork('../data/test_relation_part.json',
                           '../data/test_text.json',
                           '../data/relation_label_tag.txt')
    f = C.lazy_vis()
    f(*list(args),label_show=True,save_pth = "../images/2.png")
    #f(0,1,2,4,5,6,29,label_show=False)
    # 含有I的是有问题的 如3,

if __name__ == "__main__":main(0)
