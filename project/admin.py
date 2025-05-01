from django.contrib import admin

# Register your models here.

from .models import ClothingItem, Outfit, Event, Friendship, RSVP, Profile

admin.site.register(ClothingItem)
admin.site.register(Outfit)
admin.site.register(Event)
admin.site.register(Friendship)
admin.site.register(RSVP)
admin.site.register(Profile)