from pokego.utils import requests_get
from bs4 import BeautifulSoup
from pyjsparser import parse as jsparse
import json
import re


def get_pokemonlist():
    rawdata = requests_get('https://cdn08.net/pokemongo/data/4629?ver=115')
    parsed = jsparse(rawdata.content.decode('utf-8'))
    rawpoke = json.loads(parsed['body'][0]['declarations'][0]['init']['arguments'][0]['value'])
    return rawpoke


def get_ptypelist():
    # https://9db.jp/pokemongo/data/1689 を参照
    return [
        {
            'id': 1,
            'name': 'ノーマル',
        },
        {
            'id': 3,
            'name': 'ほのお',
        },
        {
            'id': 4,
            'name': 'みず',
        },
        {
            'id': 5,
            'name': 'くさ',
        },
        {
            'id': 6,
            'name': 'でんき',
        },
        {
            'id': 7,
            'name': 'こおり',
        },
        {
            'id': 8,
            'name': 'かくとう',
        },
        {
            'id': 9,
            'name': 'どく',
        },
        {
            'id': 10,
            'name': 'じめん',
        },
        {
            'id': 2,
            'name': 'ひこう',
        },
        {
            'id': 11,
            'name': 'エスパー',
        },
        {
            'id': 12,
            'name': 'むし',
        },
        {
            'id': 13,
            'name': 'じめん',
        },
        {
            'id': 14,
            'name': 'どく',
        },
        {
            'id': 15,
            'name': 'ドラゴン',
        },
        {
            'id': 16,
            'name': 'あく',
        },
        {
            'id': 17,
            'name': 'はがね',
        },
        {
            'id': 18,
            'name': 'フェアリー',
        },
    ]


def get_wazaid_list(mode):
    rawdata = requests_get('https://9db.jp/pokemongo/data/1427')
    sp = BeautifulSoup(rawdata.content)
    if mode == 'normal':
        wl = sp.select_one('#wiki_wazalist1')
    elif mode == 'special':
        wl = sp.select_one('#wiki_wazalist2')
    else:
        raise ValueError('invalid mode')
    lis1 = wl.select_one('tbody').select('tr')
    
    results = [
        int(re.sub('^data/', '', elm.select('a')[1]['href']))
        for elm in lis1
    ]
    return results


def get_spwaza_by_id(wid):
    rawdata = requests_get('https://9db.jp/pokemongo/data/' + str(wid))
    sp = BeautifulSoup(rawdata.content)
    wname = re.sub('の性能$', '', sp.select_one('#toc0').text.strip())
    elm = sp.select_one('#data_body').select_one('table').select_one('tbody').select('tr')
    ptype_id = int(re.search('type=(\d+)$', elm[1].select_one('a')['href']).group(1))
    dmg_gr, dmg_tr = float(elm[2].select('td')[1].text.strip()), float(elm[2].select('td')[2].text.strip())
    gg_gr, gg_tr = float(re.search('gage([1-3])\.jpg$', elm[3].select('td')[1].select_one('img')['src']).group(1)), float(elm[3].select('td')[2].text.strip())
    rgt_gr = float(re.search('(\S+)秒$', elm[4].select('td')[1].text).group(1).strip())
    dmgt_gr = float(re.search('(\S+)秒$', elm[5].select('td')[1].text).group(1).strip())
    dps_gr = float(re.search('^(\S+) ', elm[6].select('td')[1].text).group(1).strip())
    dpe_gr, dpe_tr = float(elm[7].select('td')[1].text.strip()), float(elm[7].select('td')[2].text.strip())

    result = {
        'id': wid,
        'name': wname,
        'ptype_id': ptype_id,
        'gymraid': {
            'damage': dmg_gr,
            'gauge': gg_gr,
            'rigidity_time': rgt_gr,
            'damage_time': dmgt_gr,
            'dps': dps_gr,
            'dpe': dpe_gr,
        },
        'trainer': {
            'damage': dmg_tr,
            'gauge': gg_tr,
            'dpe': dpe_tr,
        }
    }
    return result


def get_waza_by_id(wid):
    rawdata = requests_get('https://9db.jp/pokemongo/data/' + str(wid))
    sp = BeautifulSoup(rawdata.content)
    wname = re.sub('の性能$', '', sp.select_one('#toc0').text.strip())
    elm = sp.select_one('#data_body').select_one('table').select_one('tbody').select('tr')
    ptype_id = int(re.search('type=(\d+)$', elm[1].select_one('a')['href']).group(1))
    dmg_gr, dmg_tr = float(elm[2].select('td')[1].text.strip()), float(elm[2].select('td')[2].text.strip())
    rgt_gr, rgt_tr = float(re.search('(\S+)秒$', elm[3].select('td')[1].text).group(1).strip()), float(re.search('([1-9]+)T$', elm[3].select('td')[2].text).group(1).strip())
    dmgt_gr = float(re.search('(\S+)秒$', elm[4].select('td')[1].text).group(1).strip())
    gg_gr, gg_tr = float(elm[5].select('td')[1].text.strip()), float(elm[5].select('td')[2].text.strip())
    dps_gr, dpt_tr = float(re.search('^(\S+) ', elm[6].select('td')[1].text).group(1).strip()), float(re.search('^(\S+) ', elm[6].select('td')[2].text).group(1).strip())
    eps_gr, ept_tr = float(elm[7].select('td')[1].text.strip()), float(elm[7].select('td')[2].text.strip())
    
    result = {
        'id': wid,
        'name': wname,
        'ptype_id': ptype_id,
        'gymraid': {
            'damage': dmg_gr,
            'rigidity_time': rgt_gr,
            'damage_time': dmgt_gr,
            'gauge_increase': gg_gr,
            'dps': dps_gr,
            'eps': eps_gr,
        },
        'trainer': {
            'damage': dmg_tr,
            'rigidity_time': rgt_tr,
            'gauge_increase': gg_tr,
            'dpt': dpt_tr,
            'ept': ept_tr,
        }
    }
    return result
