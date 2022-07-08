import lxml
import json
import time
import math
import requests
import pandas as pd
from posixpath import split
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, cpu_count

# 'Huobi Global', 'Binance', 'FTX', 'Kraken', 'Bybit'
pairs = {}
result = {'buy': {'name': [], 'price' : [], 'exchange' : []}, 'sell': {'name': [], 'price' : [], 'exchange' : []}, 'profit': 0}
settings = {'exception': {'symbol': ['BRL', 'KRW', 'UAH', 'TRY', 'RUB'], 'exchange': ['Hoo', 'EXX', 'EXMO', 'Mercatox', '0x Protocol'], 'profit': [5, 30]}, 'one_exchange': []}
#settings = {'exception': {'symbol': [], 'exchange': [], 'profit': [5, 30]}, 'one_exchange': ['Huobi Global', 'Binance', 'FTX', 'Kraken', 'Bybit', 'Lbank']}


def calculate(pairs, slug_name, x):
    filtered_oe = {'name': [], 'price' : [], 'exchange' : []}
    filtered_es = {'name': [], 'price' : [], 'exchange' : []}
    filtered_ee = {'name': [], 'price' : [], 'exchange' : []}
    info = pairs.pop(slug_name)
    max_prof = 0
    index_buy = 0
    index_sell = 0
    if len(settings.get('one_exchange')) != 0:
        for i in range(0, len(info.get('exchange'))):
            if info.get('exchange')[i] in settings.get('one_exchange'):
                filtered_oe.get('name').append(info.get('name')[i])
                filtered_oe.get('price').append(info.get('price')[i])
                filtered_oe.get('exchange').append(info.get('exchange')[i])
    else:
        filtered_oe = info
    if len(settings.get('exception').get('symbol')) != 0:
        for i in range(0, len(filtered_oe.get('name'))):
            if filtered_oe.get('name')[i].split('/')[0] not in settings.get('exception').get('symbol'):
                if filtered_oe.get('name')[i].split('/')[1] not in settings.get('exception').get('symbol'):
                    filtered_es.get('name').append(filtered_oe.get('name')[i])
                    filtered_es.get('price').append(filtered_oe.get('price')[i])
                    filtered_es.get('exchange').append(filtered_oe.get('exchange')[i])
    else:
        filtered_es = filtered_oe
    if len(settings.get('exception').get('exchange')) != 0:
        for i in range(0, len(filtered_es.get('exchange'))):
            if filtered_es.get('exchange')[i] not in settings.get('exception').get('exchange'):
                filtered_ee.get('name').append(filtered_es.get('name')[i])
                filtered_ee.get('price').append(filtered_es.get('price')[i])
                filtered_ee.get('exchange').append(filtered_es.get('exchange')[i])
    else:
        filtered_ee = filtered_es
    if len(filtered_ee.get('price')) != 0:
        for i in range(0, len(filtered_ee.get('price'))):
            for j in range(i + 1, len(filtered_ee.get('price'))):
                cur_prof = ((filtered_ee.get('price')[j] / filtered_ee.get('price')[i]) - 1) * 100
                if cur_prof > max_prof:
                    max_prof = cur_prof
                    index_buy = i
                    index_sell = j
    else:
        return
    result.update({'buy': {'symbol': filtered_ee.get('name')[index_buy], 'price' : filtered_ee.get('price')[index_buy], 'exchange' : filtered_ee.get('exchange')[index_buy]}, 'sell': {'symbol': filtered_ee.get('name')[index_sell], 'price' : filtered_ee.get('price')[index_sell], 'exchange' : filtered_ee.get('exchange')[index_sell]}, 'profit': max_prof})
    symbol_b = result.get('buy').get('symbol').split('/')
    symbol_s = result.get('sell').get('symbol').split('/')
    exchange_b = result.get('buy').get('exchange')
    exchange_s = result.get('sell').get('exchange')
    if result.get('profit') > settings.get('exception').get('profit')[0] and result.get('profit') < settings.get('exception').get('profit')[1]:
        print(str(x) + ' | ' + str(result), end = '\n')
                


def parser(URL_TEMPLATE, slug_name, x):
    pairs.update({slug_name: {'name': [], 'price' : [], 'exchange' : []}})
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "lxml")
    names = soup.find('thead', class_='')
    if names != None:
        names = names.tr.find_all("th")
        if names != None:
            try:
                for i in range(1, len(names)):
                    pairs.get(slug_name).get('exchange').append(str(names[i].a.text))
                    info = str(names[i]).split('<br/>')
                    pairs.get(slug_name).get('name').append(info[2].replace('</th>', ''))
                    pairs.get(slug_name).get('price').append(float(info[1].replace('$ ', '').replace(',', '.')))
            except:
                return
            calculate(pairs, slug_name, x)




if __name__ == '__main__':
    t_s= time.perf_counter()
    with open('list.csv') as f:
        slugs = {k: v.strip() for k, v in (line.split(',') for line in f)}
        x = 0
        procs = []
        multiprocessingCount = 10
        for i in range(2, 5300):
            cur_time = time.perf_counter() - t_s
            print(str(i) + ' ' + str(math.floor(cur_time)) + 's' + ' Speed = ' + str(round(i / cur_time, 2)) + 'n/s', end = '\r')
            slug_name = (slugs.get(str(i)))
            URL_TEMPLATE = "https://cryptorank.io/price/" + slug_name + "/arbitrage"
            proc = Process(target = parser,args=(URL_TEMPLATE, slug_name, i))
            procs.append(proc)
            proc.start()
            if x == multiprocessingCount:
                for proc in procs:
                    proc.join()
                x = 0
            x += 1
            

