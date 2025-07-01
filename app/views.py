from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.services import services

def index_page(request):
    return render(request, 'index.html')

def home(request):
    images = services.getAllImages()  #recupera el listado completo de imagenes y guarda en variable images
    if request.user.is_authenticated:  #si el usuario que hace el request inició sesion
        fav_cards     = services.getAllFavourites(request)  #devuelve lista de tarjetas 
        favourite_ids = [c.id for c in fav_cards] #extrae solo el atributo id de cada tarjeta,construyendo la lista favourites_ids
    else:
        favourite_ids = []  #lista vacía en caso de no estar logueados
    return render(request, 'home.html', {
        'images': images,
        'favourite_ids': favourite_ids,
    })

def search(request):
    name = request.POST.get('query','').strip() # Obtener el parámetro 'query' del POST y eliminar espacios 
    images = services.getAllImages() if not name else services.filterByCharacter(name) # Si 'name' está vacío, recuperar todas las imágenes; si no, filtrar por personaje
    if request.user.is_authenticated: 
        fav_cards     = services.getAllFavourites(request)  #Obtener todas las tarjetas favoritas del usuario
        favourite_ids = [c.id for c in fav_cards] #Extraer solo los IDs de las tarjetas favoritas
    else:
        favourite_ids = [] #si no esta autenticado lista vacía 

    # Renderizar la plantilla 'home.html', pasando las imágenes y los IDs de favoritos como contexto
    return render(request, 'home.html', {
        'images': images,
        'favourite_ids': favourite_ids,
    })

def filter_by_type(request):
    t = request.POST.get('type','').strip() # Obtener el parámetro 'type' del POST y eliminar espacios
    if not t:  # Si no se especificó ningún tipo, redirigir a la vista 'home'
        return redirect('home')
    images = services.filterByType(t)  # Filtrar las imágenes según el tipo solicitado
    if request.user.is_authenticated:  #controla si esta autenticado
        fav_cards     = services.getAllFavourites(request)
        favourite_ids = [c.id for c in fav_cards]
    else:
        favourite_ids = []
    return render(request, 'home.html', {
        'images': images,
        'favourite_ids': favourite_ids,
    })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        #Llamamos al servicio que convierte el formulario en Card y guarda en la BD
        services.saveFavourite(request)
        #Tras guardar, redirigimos a la URL indicada en el parámetro ?next= o al home por defecto
    return redirect(request.GET.get('next','home'))

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        #Llamamos al servicio que borra el favorito cuyo ID viene en request.POST
        services.deleteFavourite(request)
        #Tras borrar, redirigimos al listado de favoritos
    return redirect('favoritos')

@login_required
def getAllFavouritesByUser(request):
    fav_cards = services.getAllFavourites(request) #lista de favoritos por usuario 
    return render(request, 'favourites.html', {
        'favourite_list': fav_cards
    }) #se renderiza la plantilla pasando la lista de favoritos

@login_required
def exit(request):
    logout(request)
    return redirect('home')