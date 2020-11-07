import preprocessor as p
import pandas as pd
import numpy as np
import pickle
import string
import os
import re
import csv
import argparse
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('--model', default="clf.pickle")
args = parser.parse_args()

assert os.path.splitext(args.input)[1] == '.tsv', 'input must be a .tsv file'
assert os.path.splitext(args.model)[1] == '.pickle', 'model must be a .pickle file'

FILENAME = args.input
MODEL = pickle.load(open(args.model,'rb'))
KEYWORDS = 'china|chinese|asia|asian|chinazi|chink|chingchong|gook|wuflu|wu flu|kungflu|kung flu|wuhan'

data = pd.read_csv(FILENAME, encoding='utf-8', delimiter='\t', usecols=[1, 4, 5], parse_dates=[1], quoting=csv.QUOTE_NONE)
data.columns = ['tweet_date', 'tweet_full_text', 'tweet_lang']

data = data[data['tweet_full_text'].str.contains(KEYWORDS, flags=re.IGNORECASE, regex=True).fillna(False)]
data = data[data['tweet_lang'].str.match('en').fillna(False)]

p.set_options(p.OPT.URL, p.OPT.MENTION)
nlp = spacy.load('en_core_web_sm')
count_dict = {}

for i, row in data.iterrows():
    cleaned = p.clean(row['tweet_full_text'])
    words = nlp(cleaned)
    tokens = [word.lemma_.lower() if word.lemma_ != '-PRON-' else word.lower_ for word in words]
    tokens = [t for t in tokens if t not in string.punctuation]
    text = ' '.join(tokens)
    
    pred = MODEL.predict([text])[0]
    date = row['tweet_date']

    if date in count_dict.keys():
        count_dict[date][0] -= pred
        count_dict[date][1] += 1
    else:
        count_dict[date] = [-pred, 1]

count_arr = [[x, count_dict[x][0], count_dict[x][1]] for x in count_dict.keys()]
counts = pd.DataFrame(count_arr, columns=['date', 'neg_count', 'total'])
counts.to_csv(os.path.splitext(FILENAME)[0] + '_counts.csv', encoding='utf-8', index=False, header=False)