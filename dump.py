import argparse
import os
from pokego.minpoke.builder import (
    build_ptypes,
    build_pokemons,
    build_wazas,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', help='not in use')
    parser.add_argument('--storage-dir', default='_storage')
    ns = parser.parse_args()
    sdir = ns.storage_dir

    os.makedirs(sdir, exist_ok=True)

    ptypes_result = build_ptypes()
    pokemons_result = build_pokemons()
    wazas_result = build_wazas()

    for o in (ptypes_result + pokemons_result + wazas_result):
        _name = o['name']
        _value = o['value']
        _value.to_pickle(os.path.join(sdir, _name + '.pkl'))
        print(f'dump {_name} done.')


if __name__ == '__main__':
    main()
