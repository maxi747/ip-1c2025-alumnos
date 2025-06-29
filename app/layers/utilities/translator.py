import ast
from django.contrib.auth import get_user
from app.layers.utilities.card import Card

# Usado cuando la información viene de la API
def fromRequestIntoCard(poke_data):
    return Card(
        id     = poke_data.get('id'),
        name   = poke_data.get('name'),
        height = poke_data.get('height'),
        weight = poke_data.get('weight'),
        base   = poke_data.get('base_experience'),
        image  = safe_get(poke_data, 'sprites', 'other', 'official-artwork', 'front_default'),
        types  = getTypes(poke_data),
    )

def getTypes(poke_data):
    return [
        safe_get(t, 'type', 'name')
        for t in poke_data.get('types', [])
        if safe_get(t, 'type', 'name')
    ]

# Usado cuando la información viene del template
def fromTemplateIntoCard(request):
    data = request.POST
    # construyo la Card directamente con user e id en el orden que espera el __init__
    return Card(
        name   = data.get("name"),
        height = int(data.get("height", 0)),
        base   = int(data.get("base", 0)),
        weight = int(data.get("weight", 0)),
        image  = data.get("image"),
        types  = [t.strip() for t in data.get("types","").split(",") if t.strip()],
        user   = get_user(request),                # asigno el usuario aquí
        id     = int(data.get("id", 0)),           # y el id
    )

def fromRepositoryIntoCard(repo_dict):
    # 'types' puede venir ya como lista o como string; lo normalizamos a lista
    raw_types = repo_dict.get('types', [])
    if isinstance(raw_types, str):
        try:
            types_list = ast.literal_eval(raw_types)
        except Exception:
            types_list = []
    else:
        types_list = raw_types

    return Card(
        id     = repo_dict.get('id'),
        name   = repo_dict.get('name'),
        height = repo_dict.get('height'),
        weight = repo_dict.get('weight'),
        base   = repo_dict.get('base_experience'),
        types  = types_list,
        image  = repo_dict.get('image'),
        user   = None,
    )

def safe_get(dic, *keys):
    for key in keys:
        if not isinstance(dic, dict):
            return None
        dic = dic.get(key, {})
    return dic or None