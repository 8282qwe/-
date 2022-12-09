from django.contrib import admin
from .models import Discountrate, Movies, Movieschedule, People, Theater, Theaterseat, Ticketing, Board

# Register your models here.
admin.site.register(Discountrate)
admin.site.register(Movies)
admin.site.register(Movieschedule)
admin.site.register(People)
admin.site.register(Theater)
admin.site.register(Theaterseat)
admin.site.register(Ticketing)
admin.site.register(Board)
