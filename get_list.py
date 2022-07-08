import requests
import pandas as pd



list_symbols = []
API = 'https://api.cryptorank.io/v1/currencies?limit=5300&api_key=42277916e311b55400c2a298eadd6ab6353a256ba9a24830bb9fcc15b2f3'
r = requests.get(API).json()
for i in range(0, 5300):
    list_symbols.append(r.get('data')[i].get('slug'))
    print(list_symbols[i])
with open('list.csv') as f:
    pd.Series(list_symbols).to_csv('list.csv', index=True, header=False)