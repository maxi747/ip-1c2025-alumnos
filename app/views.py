from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene dos listados: uno de las imágenes de la API y otro de favoritos,
# ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)
    else:
        favourite_list = []
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })

# función utilizada en el buscador
def search(request):
    name = request.POST.get('query', '').strip()
    if name == '':
        images = services.getAllImages()
    else:
        images = services.filterByCharacter(name)
    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)
    else:
        favourite_list = []
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })

# función utilizada para filtrar por tipo
def filter_by_type(request):
    type_value = request.POST.get('type', '').strip()
    if type_value:
        images = services.filterByType(type_value)
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)
        else:
            favourite_list = []
        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })
    return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', {
        'favourite_list': favourite_list
    })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services.saveFavourite(request)
    return redirect(request.GET.get('next', 'home'))

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')