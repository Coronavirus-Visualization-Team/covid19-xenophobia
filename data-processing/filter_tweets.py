import preprocessor as p
import pandas as pd
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

FILENAME = args.filename

df = pd.DataFrame([], columns=['date', 'id', 'coordinates', 'full_text', 'hashtags'])
df.to_csv('filtered_' + FILENAME, encoding='utf-8', index=False)

reader = pd.read_csv(FILENAME, encoding='utf-8', parse_dates=['date'], chunksize=5000)
p.set_options(p.OPT.URL, p.OPT.MENTION)

line, text = 0, ''

try:
    for chunk in reader:
        chunk = chunk.fillna('')
        filtered = chunk[chunk['full_text'].str.contains('china|chinese|asia|asian|chinazi|chink|chingchong|gook|wuflu|wu flu|kungflu|kung flu|wuhan', flags=re.IGNORECASE, regex=True)]
        for i, row in filtered.iterrows():
            filtered.at[i, 'full_text'] = p.clean(row['full_text'])
            line, text = line + 1, p.clean(row['full_text'])
        #print(filtered['full_text'].iloc[0])
        filtered.to_csv('filtered_' + FILENAME, mode='a', encoding='utf-8', index=False, header=False)
except Exception as e:
    print(('Error line %d: %s' % (line, str(type(e)))))
    print(text)