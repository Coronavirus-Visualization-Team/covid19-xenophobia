import preprocessor as p
import pandas as pd
import numpy as np
import pickle
import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('--model', default="clf.pickle")
args = parser.parse_args()

FILENAME = args.filename
MODEL = pickle.load(open(args.model,'rb'))
KEYWORDS = 'china|chinese|asia|asian|chinazi|chink|chingchong|gook|wuflu|wu flu|kungflu|kung flu|wuhan'

data = pd.read_csv(FILENAME, encoding='utf-8', delimiter='\t', usecols=[1, 4, 5], parse_dates=[1])
data.columns = ['tweet_date', 'tweet_full_text', 'tweet_lang']

data = data[data['tweet_full_text'].str.contains(KEYWORDS, flags=re.IGNORECASE, regex=True)]
data = data[data['tweet_lang'].str.match('en')]

p.set_options(p.OPT.URL, p.OPT.MENTION)

count_dict = {}

for i, row in data.iterrows():
    cleaned_text = p.clean(row['tweet_full_text'])
    pred = MODEL.predict([row['tweet_full_text']])[0]
    date = row['tweet_date']

    if date in count_dict.keys():
        count_dict[date][0] -= pred
        count_dict[date][1] += 1
    else:
        count_dict[date] = [-pred, 1]

count_arr = [[x, count_dict[x][0], count_dict[x][1]] for x in count_dict.keys()]
count_arr.sort(key=(lambda x: x[0]))
counts = pd.DataFrame(count_arr, columns=['date', 'neg_count', 'total'])
counts.to_csv(os.path.splitext(FILENAME)[0] + '_counts.csv', encoding='utf-8', index=False)