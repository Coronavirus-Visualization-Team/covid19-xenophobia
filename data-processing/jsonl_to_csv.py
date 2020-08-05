import jsonlines
import gzip
import shutil
import os
import pandas as pd
from pathlib import Path

data = []
counter = 0

df = pd.DataFrame(data, columns=['date', 'id', 'coordinates', 'full_text', 'hashtags'])
df.to_csv('output.csv', encoding='utf-8', index=False)

for path in Path('.').iterdir():
    if not path.name.endswith('.jsonl.gz'):
        continue

    print(path)
    path2 = 'temp.jsonl'

    with gzip.open(path, 'rb') as f_in:
        with open(path2, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    with jsonlines.open(path2) as reader:

        for obj in reader:

            if obj['full_text'][:2] == 'RT' or obj['lang'] != 'en':
                continue

            tweet_data = [str(path)[21:31],
                          obj['id_str'],
                          obj['coordinates'],
                          obj['full_text'],
                          [h['text'] for h in obj['entities']['hashtags']]]
            data.append(tweet_data)

    counter += 1
    if counter == 24:
        df = pd.DataFrame(data, columns=['date', 'id', 'coordinates', 'full_text', 'hashtags'])
        df.to_csv('output.csv', mode='a', encoding='utf-8', index=False, header=False)
        data = []
        counter = 0

    os.remove(path)
    os.remove(path2)

df = pd.DataFrame(data, columns=['date', 'id', 'coordinates', 'full_text', 'hashtags'])
df.to_csv('output.csv', mode='a', encoding='utf-8', index=False, header=False)
