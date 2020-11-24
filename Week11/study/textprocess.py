#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: textprocess.py
#@Software: PyCharm


# from sklearn.feature_extraction.text import TfidfVectorizer
# document = ["I have a pen.",
#             "I have an apple."]
# tfidf_model = TfidfVectorizer().fit(document)
# sparse_result = tfidf_model.transform(document)     # 得到tf-idf矩阵，稀疏矩阵表示法
# print(sparse_result)
# # (0, 3)	0.814802474667   # 第0个字符串，对应词典序号为3的词的TFIDF为0.8148
# # (0, 2)	0.579738671538
# # (1, 2)	0.449436416524
# # (1, 1)	0.631667201738
# # (1, 0)	0.631667201738
# print(sparse_result.todense())                     # 转化为更直观的一般矩阵
# # [[ 0.          0.          0.57973867  0.81480247]
# #  [ 0.6316672   0.6316672   0.44943642  0.        ]]
# print(tfidf_model.vocabulary_)                      # 词语与列的对应关系


# from nltk.tokenize import sent_tokenize
# mytext = "Hello Adam, how are you? I hope everything is going well. Today is a good day, see you dude."
# print(sent_tokenize(mytext))

from sklearn.feature_extraction.text import TfidfVectorizer

s = ['文本 分词 工具 可 用于 对 文本 进行 分词 处理',
     '常见 的 用于 处理 文本 的 分词 处理 工具 有 很多']
tfidf = TfidfVectorizer(stop_words=None,
                        token_pattern=r"(?u)\b\w\w+\b", max_features=6)
weight = tfidf.fit_transform(s).toarray()
word = tfidf.get_feature_names()

print('vocabulary list:\n')
vocab = tfidf.vocabulary_.items()
vocab = sorted(vocab, key=lambda x: x[1])
print(vocab)
print('IFIDF词频矩阵:')
print(weight)

for i in range(len(weight)):
    # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，
    # 第二个for便利某一类文本下的词语权重
    print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    for j in range(len(word)):
        print(word[j], weight[i][j])  # 第i个文本中，第j个次的tfidf值
