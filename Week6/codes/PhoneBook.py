#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: PhoneBook.py
#@Software: PyCharm

import time
import pickle
from xpinyin import Pinyin

class Person:
    '''
    Person Class
    properties:id,name,tel,mail,port
    methods:renew_properties,get_properties
    '''
    ID = 0
    def __init__(self,name,tel,mail,port):
        Person.ID += 1
        self.id = Person.ID
        self.name = name
        self.tel = tel
        self.mail = mail
        self.port = port


    def renew_properties(self,prop,value):
        if prop == "name":
            self.name = value
        elif prop == "tel":
            self.tel = value
        elif prop == "mail":
            self.mail = value
        elif prop == "port":
            self.port = value

    def get_properties(self,prop):
        return self.__dict__[prop]

class Portrait:
    '''
    Portrait Class
    properties:addr,length,width
    methods:renew_properties,get_properties
    '''
    def __init__(self,addr,length,width):
        self.addr = addr
        self.length = length
        self.width = width

    def renew_properties(self,prop,value):
        self.__dict__[prop] = value

    def get_properties(self,prop):
        return self.__dict__[prop]


class PhoneBook(Person):
    '''
    Portrait Class
    properties:person_count,person_list
    methods:renew_properties,get_properties
    '''
    def __init__(self):
        self.person_count = 0
        self.person_list = []
        self.id_list = []

    def append_person(self,p:Person):
        '''
        add the person to the PhoneBook
        :param p: Person Class
        :return: None
        '''
        if p.id not in self.id_list:
            person_dict = {}
            person_dict["person"] = p
            person_dict["add_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            person_dict["renew_time"] = None
            #add the prop
            self.person_count += 1
            self.person_list.append(person_dict)
            self.id_list.append(p.id)
        else:
            print(f"Warning: Person {p.name} has already existed")

    def renew_person(self,p:Person):
        '''
        renew the person in the PhoneBook
        :param p: Person Class
        :return: None
        '''
        if p.id in self.id_list:
            d = self.person_list[self.id_list.index(p.ID)]
            d["renew_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            print(f"Warning: Can't Find Person {p.name}")

    def search(self,data,method="name"):
        '''
        search the person from phonebook by method
        :param method: the way the search the phonebook
        :param data: the content of the search_key
        '''
        start = time.time()
        if method not in ["name","tel","mail"]:
            print(f"Warning: Cannot Use {method} to Search the PhoneBook!")
        for d in self.person_list:
            if method == "name" and d["person"].name == data:
                break
            elif method == "tel" and d["person"].tel == data:
                break
            elif method == "mail" and d["person"].mail == data:
                break
        return d["person"],time.time()-start

    def hash_search(self,data,hash_dict,method="name"):
        '''
        search the person from phonebook using hash_search with hash_dict
        :param method: the way the search the phonebook
        :param hash_dict: hash dict based on method
        :param data: the content of the search_key
        '''
        start = time.time()
        idx = hash_dict[data] - 1    #pb.id_list:1-5000
        #print(self.person_list[idx]["person"].__dict__)
        return self.person_list[idx],time.time()-start

    def order_print(self,method="name",desc=False):
        start = time.time()
        if method not in ["name","tel","mail"]:
            print(f"Warning: Cannot Use {method} to Sort the PhoneBook!")
        elif method == "name":
            temp_list = sorted(self.person_list, key=lambda x: x["person"].name, reverse=desc)
        elif method == "tel":
            temp_list = sorted(self.person_list, key=lambda x: x["person"].tel, reverse=desc)
        elif method == "mail":
            temp_list = sorted(self.person_list, key=lambda x: x["person"].mail, reverse=desc)
        for d in temp_list:
            print(d["person"].__dict__)
        return time.time()-start


    def chinese_search(self,data):
        start_time = time.time()
        p = Pinyin()
        person_list = self.person_list
        search_list = []
        for d in person_list:
            temp_name = d["person"].name
            if data == p.get_initials(temp_name, u'').lower():
                search_list.append(d["person"])
        return search_list,time.time() - start_time


    def chinese_order(self):
        p = Pinyin()
        temp_list = sorted(self.person_list, key=lambda x: p.get_initials(
                            x["person"].name,u'').lower())
        for d in temp_list:
            print(d["person"].__dict__)
        return temp_list


    def mysave(self):
        with open('../data/PhoneBook.txt', 'w') as f:
            f.write("id\tname\ttel\tmail\tadd_time\trenew_time\n")
            person_list = self.__dict__["person_list"]
            for d in person_list:
                person_info = d["person"].__dict__
                for info in list(person_info.values())[:4]:  #projection some attr
                    f.write(str(info)+"\t")
                f.write(str(d["add_time"])+"\t"+str(d["renew_time"]))
                f.write("\n")
        pickle.dump(self, open("../data/PhoneBook.p", "wb"))


    def myload(self,filename):
        data = pickle.load(open("../data/"+filename,"rb"))
        print(data)
# p = Person("zjh0","123","1@qq.com","image1")
# print(p.__dict__)
# p.renew_properties("name","zjh")
# print(p.__dict__)
# for prop in ["id","name","mail","port","tel"]:
#     print("{:4} : {:}".format(prop,p.get_properties(prop)))

# p2 = Portrait("1/2/3.png",123,234)
# print("*** Before Change ***")
# for prop in p2.__dict__.keys():
#     print(prop,p2.get_properties(prop))
# p2.renew_properties("addr","1/2.png")
# print("*** After Change ***")
# for prop in p2.__dict__.keys():
#     print(prop, p2.get_properties(prop))
#
# pb = PhoneBook()
# p = Person("zjh","123","1@qq.com","image1")
# p2 = Person("zjh_2","456","2@qq.com","image2")
# print("p:",p.__dict__,p.id)
# print("p2:",p2.__dict__,p2.id)
# pb.append_person(p)
# pb.append_person(p2)
# print(pb.__dict__)
# # time.sleep(1)
# p.renew_properties("name","zjh_1")
# pb.renew_person(p)
# print(pb.__dict__)
# temp_p,temp_time = pb.search("zjh_1","name")
# print("temp_p",temp_p.__dict__,"tmep_time",temp_time)
# period = pb.order_print("name")
# print(period)
#


# p1 = Person("庄嘉恒","123","1@qq.com","image1")
# p2 = Person("庄减恒","123","1@qq.com","image1")
# p3 = Person("庄乘恒","123","1@qq.com","image1")
# PB = PhoneBook()
# PB.append_person(p1)
# PB.append_person(p2)
# PB.append_person(p3)
#
# ans,_ = PB.chinese_search("庄嘉恒")
# for i in ans:
#     print(i.__dict__)



