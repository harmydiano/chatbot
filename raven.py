import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import itertools

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)
a = open("brain.txt", 'r')
strip_list = [l.strip() for l in a]
foo =list(grouper(strip_list,2))
convo_frame = pd.Series(dict(foo)).to_frame().reset_index()
convo_frame.columns = ['q', 'a']
def raven_msg(msg):
    vectorizer = TfidfVectorizer(ngram_range=(1,3))
    vec = vectorizer.fit_transform(convo_frame['q'])
    my_q = vectorizer.transform([msg])
    cs = cosine_similarity(my_q, vec)
    rs = pd.Series(cs[0]).sort_values(ascending=False)
    top5 = rs.iloc[0:5]
    #print(top5)
    #print(convo_frame.iloc[top5.index]['q'])
    rsi = rs.index[0]
    return (convo_frame.iloc[rsi]['a'])
