from django.shortcuts import render, get_object_or_404
from .models import Slide, Game, Package


def home(request):
    slides = Slide.objects.all()
    games = Game.objects.all()
    packages = Package.objects.all()

    return render(request, 'home.html', {
        'slides': slides,
        'games': games,
        'packages': packages
    })

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    packages = Package.objects.filter(game=game)

    return render(request, 'game_detail.html', {
        'game': game,
        'packages': packages
    })