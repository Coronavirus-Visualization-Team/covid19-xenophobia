import pandas as pd
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('model')
args = parser.parse_args()

FILENAME = args.filename

df = pd.DataFrame([], columns=['date', 'id', 'coordinates', 'full_text', 'hashtags', 'pred'])
df.to_csv('pred_' + FILENAME, encoding='utf-8', index=False)

model = pickle.load(open(args.model,'rb'))
reader = pd.read_csv(FILENAME, encoding='utf-8', parse_dates=['date'], chunksize=5000)

for chunk in reader:
    chunk['pred'] = np.zeros(len(chunk), dtype=int)
    for i, row in chunk.iterrows():
        chunk.at[i, 'pred'] = model.predict([row['full_text']])[0]
    chunk.to_csv('pred_' + FILENAME, mode='a', encoding='utf-8', index=False, header=False)