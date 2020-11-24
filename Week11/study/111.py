#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: 111.py
#@Software: PyCharm

class A:
    a=2
    def __init__(self):
        self.a=2
    pass

class B(A):
    a=2

    def __init__(self):
        self.a=3
    def dd(self):
        print()
    pass

class C(A):
    def __init__(self):
        self.a=4
    pass


def d():
    pass
# aa=B()
print(print(B.__dict__['dd']))
print(d())

# print(a)
