from django.contrib import admin
from .models import Slide, Game
from .models import SiteSetting
from .models import Game
from .models import Game, Package
from .models import Order
from .models import SiteSetting



admin.site.register(Slide)
admin.site.register(Game)
admin.site.register(Package)
admin.site.register(Order)
admin.site.register(SiteSetting)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'player_id', 'package_name', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('player_id', 'user__username')