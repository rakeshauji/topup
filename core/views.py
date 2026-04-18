from django.shortcuts import render, get_object_or_404
from .models import Slide, Game, Package
from .models import Order
from .models import Game, Package, Order


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

    if request.method == "POST":
        package = get_object_or_404(Package, id=request.POST['package'])

        Order.objects.create(
            game=game,   # 👈 MUST ADD THIS
            package=package,
            player_id=request.POST['player_id'],
            payment_method=request.POST['payment'],
            contact=request.POST['contact']
        )

    return render(request, 'game_detail.html', {
        'game': game,
        'packages': packages
    })

def package_detail(request, id):
    package = Package.objects.get(id=id)
    return render(request, 'package_detail.html', {'package': package})