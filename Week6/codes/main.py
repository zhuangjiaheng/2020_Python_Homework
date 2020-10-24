#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: main.py
#@Software: PyCharm

import os
import random
import PhoneBook as pb
from xpinyin import Pinyin
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def random_name():
    name = ""
    for i in range(3):
        name += chr(random.randint(97, 122))  # 取小写字母
    return name

def random_tel(i):
    has_tel = []
    while True:
        yidong = ['134','135','136','137','138','139','147','150','151',
                  '152','157','158','159','172','178','182','183','184',
                  '187','188','195','197','198']
        liantong = ['130','131','132','145','155','156','166','175','176',
                   '185','186','196']
        dianxin = ['133','149','153','180','181','189','173','177','190',
                   '191','193','199']
        if i % 3 == 0:
            pre_tel = random.choice(yidong)
        elif i % 3 == 1:
            pre_tel = random.choice(liantong)
        else:
            pre_tel = random.choice(dianxin)
        tel = pre_tel + str(random.randint(10000000,99999999))
        if tel not in has_tel:
            has_tel.append(tel)
            break
    return tel
        #ranint包含两侧

def random_mail(i):
    post_mail = ["@qq.com","@buaa.edu.cn","@126.com","@163.com"]
    has_mail = []
    while True:
        ret = ""
        for j in range(11):
            num = random.randint(0, 9)
            letter = chr(random.randint(97, 122))#取小写字母
            Letter = chr(random.randint(65, 90))#取大写字母
            s = str(random.choice([num,letter,Letter]))
            ret += s
        if ret +post_mail[i % 4] not in has_mail:
            has_mail.append(ret +post_mail[i % 4])
            break
    return ret + post_mail[i % 4]

def random_img(i):
    ABS_PATH = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ABS_PATH, f'image/protrait{i}'), \
           random.randint(200,300),random.randint(200,300)

def is_chinese(data):
    '''
    define whether a name is chinese name
    :param data: name
    :return: bool
    '''
    if data >= u'\u4e00' and data <= u'\u9fa5':
        return True
    else:
        return False


def search_all(phonebook,method="name"):
    # create name hash dictionary
    name_list = []; tel_list = []; mail_list = []
    for d in phonebook.person_list:
        name_list.append(d["person"].name)
        tel_list.append(d["person"].tel)
        mail_list.append(d["person"].mail)
    id_name_dict = dict(zip(name_list,phonebook.id_list))
    id_tel_dict = dict(zip(tel_list, phonebook.id_list))
    id_mail_dict = dict(zip(mail_list, phonebook.id_list))
    #print(id_name_dict,id_tel_dict,id_mail_dict)
    #print(id_tel_dict.keys())

    # calculate the time
    # search
    s_time = 0; hs_time = 0
    for name in id_name_dict.keys():
        p, search_time = phonebook.search(name, method)
        s_time += search_time
    print(f"{method}_search_time:",s_time)
    #hash search
    for i in range(100):
        if method == "name":
            for name in id_name_dict.keys():
                p, search_time = phonebook.hash_search(name,id_name_dict,method)
                hs_time += search_time
        elif method == "tel":
            for tel in id_tel_dict.keys():
                p, search_time = phonebook.hash_search(tel, id_tel_dict, method)
                hs_time += search_time
        elif method == "mail":
            for mail in id_mail_dict.keys():
                p, search_time = phonebook.hash_search(mail, id_mail_dict, method)
                hs_time += search_time
    print(f"{method}_hash_search_time",hs_time/100)


def show_efficiency():
    name_list = ['姓名查询', '电话查询', '邮件查询']
    # per_time by search
    # num_list = [0.0000748,0.00019372,0.00019852]
    # num_list1 = [0.000366716,0.000765456,0.00071416]
    # num_list2 = [0.000629918,0.001380862,0.001414134]
    # all_time by hash_search
    num_list = [0.0002, 0.00024, 0.0003]
    num_list1 = [0.00112, 0.00136, 0.00094]
    num_list2 = [0.00212, 0.00318, 0.0023]

    x = list(range(len(num_list)))
    total_width, n = 0.9, 3
    width = total_width / n

    plt.bar(x, num_list, width=width, label='N=1000', fc='skyblue')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, num_list1, width=width, label='N=5000', tick_label=name_list, fc='orange')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, num_list2, width=width, label='N=10000', fc='pink')
    plt.title("所有对象哈希查询总时间")
    plt.legend()
    plt.show()

def show_comparision():
    x = [1000,5000,10000]
    plt.plot(x,[374,1637.125,2971.311321],label ="姓名查询",linewidth=3,marker='o')
    plt.plot(x,[807.1666667,2814.176471,4342.333333],label ="电话查询",linewidth=3,marker='o')
    plt.plot(x,[661.7333333,3798.723404,6148.408696], label="邮件查询",linewidth=3,marker='o')

    plt.title("优化效果比较")
    plt.legend()
    plt.show()


def create(n):
    phonebook = pb.PhoneBook()
    for i in range(n):
        file,length,width = random_img(i)
        temp_i = pb.Portrait(file,length,width)
        temp_p = pb.Person(random_name(),random_tel(i),
                           random_mail(i),temp_i)
        phonebook.append_person(temp_p)
    return phonebook


def main():
    random.seed(0)
    '''create'''
    phonebook = create(5000)

    '''modify'''
    # print("-----Before Modify-----")
    # p,_ = phonebook.search("lef","name")
    # print("person:",p.__dict__)
    #
    #
    # p.renew_properties("name","zjh")  #modify the instance
    # time.sleep(3)
    # phonebook.renew_person(p)
    # print("-----After Modify-----")
    # print("person:",p.__dict__)
    # print("phonebook:",phonebook.__dict__["person_list"])

    '''def language'''



    '''search'''
    # print("name:")
    # search_all(phonebook,"name")
    # print("tel:")
    # search_all(phonebook,"tel")
    # print("mail:")
    # search_all(phonebook,"mail")

    '''efficiency'''
    #show_efficiency()
    #show_comparision()

    '''order'''
    # period1 = phonebook.order_print("name")
    # period2 = phonebook.order_print("tel")
    # period3 = phonebook.order_print("mail")
    # print(period1,period2,period3)

    '''chinese phonebook'''
    # cphonebook = create(10)
    # name_list = ["张三","李四","王五","赵六","张三强",
    #              "赵三","刘一","赵四","一二三","四五六"]
    # for i in range(10):
    #     temp_person = cphonebook.__dict__["person_list"][i]["person"]
    #     temp_person.renew_properties("name",name_list[i])
    #     #print(temp_person.__dict__)
    #     cphonebook.renew_person(temp_person)
    # print(cphonebook.__dict__)

    '''chinese_search'''
    # ans,_ = cphonebook.chinese_search("zs")
    # print("Search Result:")
    # for i in ans:
    #     print(i.__dict__)

    '''chinese_sort'''
    # print("Sorted Result")
    # cphonebook.chinese_order()
    # ans, _ = cphonebook.chinese_search("zs")
    # for i in ans:
    #     print(i.__dict__)

    '''save and load'''
    phonebook.mysave()
    phonebook.myload("PhoneBook.p")

if __name__ == "__main__" :main()
