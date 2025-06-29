from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.services import services

def index_page(request):
    return render(request, 'index.html')

def home(request):
    images = services.getAllImages()
    if request.user.is_authenticated:
        fav_cards     = services.getAllFavourites(request)
        favourite_ids = [c.id for c in fav_cards]
    else:
        favourite_ids = []
    return render(request, 'home.html', {
        'images': images,
        'favourite_ids': favourite_ids,
    })

def search(request):
    name = request.POST.get('query','').strip()
    images = services.getAllImages() if not name else services.filterByCharacter(name)
    if request.user.is_authenticated:
        fav_cards     = services.getAllFavourites(request)
        favourite_ids = [c.id for c in fav_cards]
    else:
        favourite_ids = []
    return render(request, 'home.html', {
        'images': images,
        'favourite_ids': favourite_ids,
    })

def filter_by_type(request):
    t = request.POST.get('type','').strip()
    if not t:
        return redirect('home')
    images = services.filterByType(t)
    if request.user.is_authenticated:
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
        services.saveFavourite(request)
    return redirect(request.GET.get('next','home'))

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def getAllFavouritesByUser(request):
    fav_cards = services.getAllFavourites(request)
    return render(request, 'favourites.html', {
        'favourite_list': fav_cards
    })

@login_required
def exit(request):
    logout(request)
    return redirect('home')