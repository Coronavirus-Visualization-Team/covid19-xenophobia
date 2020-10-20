import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

FILENAME = args.filename

date_dict = {}
reader = pd.read_csv(FILENAME, encoding='utf-8', parse_dates=['date'], chunksize=5000)

for chunk in reader:
    for i, row in chunk.iterrows():
        date = row['date']
        if date in date_dict.keys():
            date_dict[date][0] -= row['pred']
            date_dict[date][1] += 1
        else:
            date_dict[date] = [-row['pred'], 1]

date_arr = [[d, date_dict[d][0], date_dict[d][1]] for d in date_dict.keys()]
date_arr.sort(key=(lambda x: x[0]))
df = pd.DataFrame(date_arr, columns=['date', 'neg_count', 'total'])
df.to_csv('count_' + FILENAME, encoding='utf-8', index=False)
