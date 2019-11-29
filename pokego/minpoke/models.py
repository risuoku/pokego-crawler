import pandas as pd


ptypes_schema = {
    'columns': ['minpoke_id', 'name'],
    'type': [int, str],
}

pokemons_schema = {
    'columns': ['minpoke_id', 'name', 'number', 'generation', 'attack', 'defense', 'hp'],
    'type': [int, str, int, int, int, int, int],
}

pokemons_ptypes_schema = {
    'columns': ['pokemon_minpoke_id', 'ptype_minpoke_id'],
    'type': [int, int]
}

pokemons_wazas_schema = {
    'columns': ['pokemon_minpoke_id', 'waza_minpoke_id'],
    'type': [int, int],
}

pokemons_spwazas_schema = {
    'columns': ['pokemon_minpoke_id', 'waza_minpoke_id'],
    'type': [int, int],
}

wazas_schema = {
    'columns': ['minpoke_id', 'name', 'ptype_minpoke_id'],
    'type': [int, str, int],
} 
spwazas_schema = {
    'columns': ['minpoke_id', 'name', 'ptype_minpoke_id'],
    'type': [int, str, int],
}

wazas_trainer_schema = {
    'columns': ['minpoke_id', 'damage', 'rigidity_time', 'gauge_increase', 'dpt', 'ept'],
    'type': [int, float, float, float, float, float],
}

wazas_gymraid_schema = {
    'columns': ['minpoke_id', 'damage', 'rigidity_time', 'damage_time', 'gauge_increase', 'dps', 'eps'],
    'type': [int, float, float, float, float, float, float],
}

spwazas_trainer_schema = {
    'columns': ['minpoke_id', 'damage', 'gauge', 'dpe'],
    'type': [int, float, float, float],
}

spwazas_gymraid_schema = {
    'columns': ['minpoke_id', 'damage', 'gauge', 'rigidity_time', 'damage_time', 'dps', 'dpe'],
    'type': [int, float, float, float, float, float, float],
}
    

def df_with_schema(schema):
    if 'columns' not in schema or 'type' not in schema:
        raise KeyError('columns and type must be set in this schema')
    columns = schema['columns']
    dtype_dict = dict(zip(columns, schema['type']))
    
    def _func(data):
        df = pd.DataFrame(data, columns=columns)
        df.astype(dtype_dict)
        return df
    
    return _func


# define functions
get_ptypes_df = df_with_schema(ptypes_schema)
get_pokemons_df = df_with_schema(pokemons_schema)
get_pokemons_ptypes_df = df_with_schema(pokemons_ptypes_schema)
get_pokemons_wazas_df = df_with_schema(pokemons_wazas_schema)
get_pokemons_spwazas_df = df_with_schema(pokemons_spwazas_schema)
get_wazas_df = df_with_schema(wazas_schema)
get_spwazas_df = df_with_schema(spwazas_schema)
get_wazas_trainer_df = df_with_schema(wazas_trainer_schema)
get_wazas_gymraid_df = df_with_schema(wazas_gymraid_schema)
get_spwazas_trainer_df = df_with_schema(spwazas_trainer_schema)
get_spwazas_gymraid_df = df_with_schema(spwazas_gymraid_schema)
