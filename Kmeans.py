import numpy as np
import pandas as pd
import jieba
import jieba.analyse
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from gensim.models import Word2Vec
import logging
import multiprocessing
import sys

# 開始做訓練
data_df = pd.read_csv('content.csv')
# 載入結巴大字典和自訂停用詞
jieba.set_dictionary('./extra_dict/dict.txt.big')
jieba.analyse.set_stop_words("./extra_dict/stop_words.txt")


# cut function
def cut(p):
    return " ".join(jieba.cut(p))


data_df.Content = data_df["Content"].apply(cut)
# split切割資料集, 選定種子
x_train, x_test, y_train, y_test = train_test_split(data_df.Content, data_df.Type, test_size=0.1, random_state=683)
# for i in range(250):
# print("第", i + 1, "個", accuracy_score(pre, y_test))
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logger.info("running %s" % ' '.join(sys.argv))
w2v_model = Word2Vec(data_df['Content'].apply(lambda x: x.split(' ', -1)),  # input要是list不是str
                     min_count=10,
                     size=200,
                     workers=multiprocessing.cpu_count())  # 訓練skip-gram模型


def AvgVector(w2v_model, sentence):
    vec = []
    for i in sentence.split(' ', -1):
        if i in w2v_model.wv.index2word:
            vec.append(w2v_model[i])
    vector = np.mean(vec, axis=0)
    vector = pd.Series(vector)
    return vector


w2v_train = x_train.apply(lambda x: AvgVector(w2v_model, x))
w2v_test = x_test.apply(lambda x: AvgVector(w2v_model, x))
print(w2v_train)

# count_vec = CountVectorizer()
# x_train_vec = count_vec.fit_transform(x_train)
# x_test_vec = count_vec.transform(x_test)
# clf = MultinomialNB(alpha=0.01)
# clf.fit(x_train_vec, y_train)
#
# for k in range(2, 15):
#     test = KMeans(n_clusters=k)
#     test.fit(data_df["Content"])
#     s = silhouette_score(data_df["Content"], test.labels_)
#     print(k, ":", s)
