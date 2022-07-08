import requests
import pandas as pd



list_symbols = []
API = ' '
r = requests.get(API).json()
for i in range(0, 5300):
    list_symbols.append(r.get('data')[i].get('slug'))
    print(list_symbols[i])
with open('list.csv') as f:
    pd.Series(list_symbols).to_csv('list.csv', index=True, header=False)
