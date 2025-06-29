# capa DAO de acceso/persistencia de datos.

from sqlite3 import IntegrityError
from app.models import Favourite



def save_favourite(fav):
    try:
        # Usamos update_or_create sobre la PK id para evitar colisiones
        obj, created = Favourite.objects.update_or_create(
            id=fav.id,             # lookup sobre el mismo campo PK
            defaults={
                'name':            fav.name,
                'types':           fav.types,
                'height':          fav.height,
                'weight':          fav.weight,
                # Aquí cambiamos fav.base_experience por fav.base
                'base_experience': fav.base,
                'image':           fav.image,
                'user':            fav.user,
            }
        )
        return obj
    except IntegrityError as e:
        print(f"Error de integridad al guardar el favorito: {e}")
        return None
    
def get_all_favourites(user):
    return list(Favourite.objects.filter(user=user).values(
        'id', 'name', 'height', 'weight', 'types','base_experience', 'image'
    ))


def delete_favourite(fav_id):
    try:
        favourite = Favourite.objects.get(id=fav_id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {fav_id} no existe o no pertenece al usuario.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False
