from django.contrib import admin
from .models import Slide, Game
from .models import SiteSettings
from .models import Game
from .models import Game, Package



admin.site.register(Slide)
admin.site.register(Game)
admin.site.register(SiteSettings)
admin.site.register(Package)