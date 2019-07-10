from django.contrib import admin

# Register your models here.
from .models import Playlist

from .models import Suser

admin.site.register(Playlist)
admin.site.register(Suser)