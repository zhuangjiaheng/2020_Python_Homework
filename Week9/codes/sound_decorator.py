#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: sound_decorator.py
#@Software: PyCharm

from functools import wraps
from playsound import playsound

# def sound(func):
#     @wraps(func)
#     def wrapper(*args,**kwargs):
#         print(wrapper.__name__)
#         playsound("../sound/notice.mp3")
#         func(*args,**kwargs)
#     return wrapper
#
# @sound
# def now():
#     print("func now")
# now()


# def a_new_decorator(a_func):
#     def wrapTheFunction():
#         print("I am doing some boring work before executing a_func()")
#         a_func()
#         print("I am doing some boring work after executing a_func()")
#         playsound("sound/notice.mp3")
#
#     return wrapTheFunction
#
# @a_new_decorator
# def a_function_requiring_decoration():
#     """Hey you! Decorate me!"""
#     print("I am the function which needs some decoration to "
#           "remove my foul smell")
#
# a_function_requiring_decoration()


def check_file(filepath):
    @wraps(wraps)
    def decorater(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print(filepath)
            print("function_name:", wrapper.__name__,decorater.__name__)
            func(*args,**kwargs)
        return wrapper
    return decorater

@check_file('../image')
def now():
    print("func now")
now()