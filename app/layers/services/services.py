# app/layers/services/services.py
# capa de servicio/lógica de negocio

from django.contrib.auth import get_user
from ..transport import transport
from ...config import config
from ..persistence.repositories import (
    save_favourite as repo_save,
    get_all_favourites,
    delete_favourite as repo_delete
)
from ..utilities.translator import (
    fromRequestIntoCard,
    fromTemplateIntoCard,
    fromRepositoryIntoCard
)


# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    print("[getAllImages] Ejecutando la función en el archivo correcto")
    # 1) traer un listado de imágenes crudas desde la API
    listaImagenes = transport.getAllImages()
    # 2) convertir cada img. en una Card
    listaCard = []
    for elem in listaImagenes:
        card = fromRequestIntoCard(elem)
        listaCard.append(card)
    print(f"[getAllImages] Trajo {len(listaCard)} tarjetas")  # Debug
    return listaCard


# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []
    for card in getAllImages():
        if name.lower() in card.name.lower():
            filtered_cards.append(card)
    return filtered_cards


# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []
    for card in getAllImages():
        if type_filter.lower() in [t.lower() for t in card.types]:
            filtered_cards.append(card)
    return filtered_cards


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    """
    Convierte el POST del formulario en un objeto Card y lo guarda en la BD.
    """
    card = fromTemplateIntoCard(request)
    return repo_save(card)


# lista todos los favoritos del usuario (usado desde template 'favourites.html')
def getAllFavourites(request):
    """
    Trae todos los registros de Favourite para el usuario y los mapea a Cards.
    """
    user = get_user(request)
    repo_list = get_all_favourites(user)            # devuelve lista de dicts
    return [fromRepositoryIntoCard(d) for d in repo_list]


# eliminar un favorito (usado desde el template 'favourites.html')
def deleteFavourite(request):
    """
    Borra un favorito según el id recibido en POST.
    """
    fav_id = int(request.POST.get('id', 0))
    return repo_delete(fav_id)


# obtiene de TYPE_ID_MAP el id correspondiente a un tipo según su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)