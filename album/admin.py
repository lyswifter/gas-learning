from django.contrib import admin
from .models import Album, Track

# Register your models here.

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("album_name", "artist")
    search_fields = list_display
    list_filter = list_display

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("album", "order", "title", "duration")
    search_fields = list_display
    list_filter = list_display
