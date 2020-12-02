#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: y.py
#@Software: PyCharm


# import random
import os
from multiprocessing import Process, Queue



path = "../texts/THUCN_small"


class Task(Process):
    def __init__(self, name,q):
        super().__init__(args=(q,))
        self._name = name
        self.q = q

    @property
    def name(self):
        return self._name

    def run(self):
        print('here')
        # global q
        c = self.q.get()
        print(c)
        if c is None:
            print('em')
            return


if __name__ == '__main__':
    pos = os.listdir(path)
    plist = []
    q, qq = Queue(), Queue()

    for i in range(2):
        p = Task('process-ji{}'.format(i + 1),q)
        plist.append(p)

    for p in plist:
        p.start()

    for p in plist:
        p.join()

    for i in pos:
        q.put(i)

    print('main')
    while 1:
        cc = qq.get()
        print(cc)

    print("n={} in main".format(n))