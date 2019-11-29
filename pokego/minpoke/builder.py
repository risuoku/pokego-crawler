from .models import (
    get_ptypes_df,
    get_pokemons_df,
    get_pokemons_ptypes_df,
    get_pokemons_wazas_df,
    get_pokemons_spwazas_df,
    get_wazas_df,
    get_spwazas_df,
    get_wazas_trainer_df,
    get_wazas_gymraid_df,
    get_spwazas_trainer_df,
    get_spwazas_gymraid_df,
)
from .loader import (
    get_ptypelist,
    get_pokemonlist,
    get_wazaid_list,
    get_waza_by_id,
    get_spwaza_by_id,
)
import re
import time
import itertools


def build_ptypes():
    ptypelist = get_ptypelist()
    d = [(pt['id'], pt['name']) for pt in ptypelist]
    result = get_ptypes_df(d)
    return result


def build_pokemons():
    def _is_valid_pokemon(raw_poke_obj): # 対象ポケモンが実装済みかどうかの判定
        return 'waza1' in raw_poke_obj and 'waza2' in raw_poke_obj

    raw_pokemonlist = get_pokemonlist()
    valid_raw_pokemonlist = [(k, v) for k, v in raw_pokemonlist.items() if _is_valid_pokemon(v)]
    valid_pokemonlist = [
        {
            'id': int(re.search('p([0-9]+)$', k).group(1)),
            'name': v['name'],
            'attack': int(v['atk']),
            'defense': int(v['def']),
            'hp': int(v['hp']),
            'generation': int(v['gen']),
            'number': int(v['no']),
            'ptypes': [v['type1']] + ([] if 'type2' not in v else [v['type2']]),
            'wazas': [int(a) for a in v['waza1']],
            'spwazas': [int(a) for a in v['waza2']],
        }
        for k, v in valid_raw_pokemonlist
    ]

    pokemons_result = get_pokemons_df([
        [o['id'], o['name'], o['number'], o['generation'], o['attack'], o['defense'], o['hp']]
        for o in valid_pokemonlist
    ])

    pokemons_ptypes_result = get_pokemons_ptypes_df(list(itertools.chain.from_iterable([
        [
            [o['id'], pt]
            for pt in o['ptypes']
        ]
        for o in valid_pokemonlist
    ])))
    
    pokemons_wazas_result = get_pokemons_wazas_df(list(itertools.chain.from_iterable([
        [
            [o['id'], pt]
            for pt in o['wazas']
        ]
        for o in valid_pokemonlist
    ])))
    
    pokemons_spwazas_result = get_pokemons_spwazas_df(list(itertools.chain.from_iterable([
        [
            [o['id'], pt]
            for pt in o['spwazas']
        ]
        for o in valid_pokemonlist
    ])))
    return pokemons_result, pokemons_ptypes_result, pokemons_wazas_result, pokemons_spwazas_result


def build_wazas():
    wazaid_list = get_wazaid_list('normal')
    spwazaid_list = get_wazaid_list('special')
    waza_list = []
    spwaza_list = []
    
    for idx, wid in enumerate(wazaid_list[:10]):
        waza_list.append(get_waza_by_id(wid))
        time.sleep(1)
    
    for idx, wid in enumerate(spwazaid_list[:10]):
        spwaza_list.append(get_spwaza_by_id(wid))
        time.sleep(1)
    
    wazas_result = get_wazas_df([
        [o['id'], o['name'], o['ptype_id']]
        for o in waza_list
    ])

    spwazas_result = get_spwazas_df([
        [o['id'], o['name'], o['ptype_id']]
        for o in spwaza_list
    ])

    wazas_trainer_result = get_wazas_trainer_df([
        [
            o['id'], o['trainer']['damage'], o['trainer']['rigidity_time'],
            o['trainer']['gauge_increase'], 
            o['trainer']['dpt'], o['trainer']['ept']
        ]
        for o in waza_list
    ])

    wazas_gymraid_result = get_wazas_gymraid_df([
        [
            o['id'], o['gymraid']['damage'], o['gymraid']['rigidity_time'],
            o['gymraid']['damage_time'], o['gymraid']['gauge_increase'],
            o['gymraid']['dps'], o['gymraid']['eps']
        ]
        for o in waza_list
    ])

    spwazas_trainer_result = get_spwazas_trainer_df([
        [
            o['id'], o['trainer']['damage'], o['trainer']['gauge'], o['trainer']['dpe'],
        ]
        for o in spwaza_list
    ])

    spwazas_gymraid_result = get_spwazas_gymraid_df([
        [
            o['id'], o['gymraid']['damage'], o['gymraid']['gauge'], 
            o['gymraid']['rigidity_time'], o['gymraid']['damage_time'],
            o['gymraid']['dps'], o['gymraid']['dpe'],
        ]
        for o in spwaza_list
    ])

    return (wazas_result, spwazas_result,
        wazas_trainer_result, wazas_gymraid_result,
        spwazas_trainer_result, spwazas_gymraid_result)
