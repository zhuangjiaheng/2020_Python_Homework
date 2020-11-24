#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: RandomWalk.py
#@Software: PyCharm

import random
import numpy as np
import matplotlib.pyplot as plt


def my_randn(sigma2,mu=0):
    while True:
        u = random.random()
        v = random.random()
        x = np.sqrt(-2 * np.log(u)) * np.cos(2 * np.pi * v)
        x = x * sigma2 + mu
        yield x


def random_walk(mu,x0,sigma2,N):
    n = 0
    x = x0
    while (n<N):
        yield x
        x = x + mu + next(my_randn(sigma2))
        n += 1
    return 'done'


def main():
    random.seed(21)

    mu1 = -1 + 2 * random.random()
    print("mu1=",mu1)
    g1 = random_walk(mu1, 0, 1, 100)
    mu2 = -1 + 2 * random.random()
    g2 = random_walk(mu2, 0, 1, 100)
    g3 = random_walk(mu1, 0, 4, 100)

    G = zip(g1, g2, g3)
    for i in G:
        print(i)

    # l1 = list(g1)
    # l2 = list(g2)
    # l3 = list(g3)
    #
    # plt.plot(list(range(100)),l1,label='mu1,N(0,1)')
    # plt.plot(list(range(100)),l2,label='mu2,N(0,1)')
    # plt.plot(list(range(100)),l3,label='mu1,N(0,4)')
    # plt.legend()
    # plt.show()

if __name__ == "__main__":main()