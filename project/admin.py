from django.contrib import admin

# Register your models here.

from .models import ClothingItem, Outfit, Event, Friendship

admin.site.register(ClothingItem)
admin.site.register(Outfit)
admin.site.register(Event)
admin.site.register(Friendship)