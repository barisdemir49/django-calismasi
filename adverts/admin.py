from pyexpat import model
from django.contrib import admin

# Register your models here.
from .models import Advert, RecourseAdverts

@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display=["title","author","createdDate","isActive"]
    search_fields=["title"]
    list_filter=["createdDate"]
    class Meta:
        model=Advert

@admin.register(RecourseAdverts)
class RecourseAdvertsAdmin(admin.ModelAdmin):
    list_display=["advert","author","createdDate"]
    search_fields=["advert","auther"]
    list_filter=["createdDate"]
    
    class Meta:
        model= RecourseAdverts