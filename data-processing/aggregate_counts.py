import pandas as pd 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

FILENAME = args.filename

reader = pd.read_csv(FILENAME, encoding='utf-8', parse_dates=[0])
date_dict = {}

for _, row in reader.iterrows():
    date = row[0]
    if date in date_dict.keys():
        date_dict[date][0] += row[1]
        date_dict[date][1] += row[2]
    else:
        date_dict[date] = [row[1], row[2]]

date_arr = [[d, date_dict[d][0], date_dict[d][1]] for d in date_dict.keys()]
date_arr.sort(key=(lambda x: x[0]))
df = pd.DataFrame(date_arr, columns=['date', 'neg_count', 'total'])
df.to_csv('agg.csv', encoding='utf-8', index=False)