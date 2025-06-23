from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    print("🔵 En la vista HOME")
    images = services.getAllImages()
    favourite_list = []
    print("🔴 images:", images)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '').strip()  # toma lo que el usuario escribe y elimina espacios en blanco

    if name == '':
        # Si no puso nada, mostramos todos los Pokémon (como la galería)
        images = services.getAllImages()
    else:
        # Si escribió algo, filtramos por nombre (total o parcial)
        images = services.filterByCharacter(name)

    favourite_list = []
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

# función utilizada para filtrar por el tipo del Pokémon
def filter_by_type(request):
    type = request.POST.get('type', '')
    print("🔎 Buscando tipo:", type)  # DEBUG: muestra qué tipo está llegando
    if type != '':
        images = services.filterByType(type)
        favourite_list = []
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')