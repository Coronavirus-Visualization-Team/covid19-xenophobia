import argparse
import pandas as pd
import random
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

FILENAME = args.filename

if not os.path.isfile('selected.csv'):
    df = pd.DataFrame([], columns=['date', 'id', 'coordinates', 'full_text', 'hashtags'])
    df.to_csv('selected.csv', encoding='utf-8', index=False)
    print('created file selected.csv')

reader = pd.read_csv(FILENAME, encoding='utf-8', parse_dates=['date'], chunksize=683)

for chunk in reader:
    chunk = chunk.fillna('')
    rand = random.randint(0, 682)
    for i, row in chunk.iterrows():
        if i % 683 == rand:
            df = pd.DataFrame([row])
            df.to_csv('selected.csv', mode='a', encoding='utf-8', index=False, header=False)
            break