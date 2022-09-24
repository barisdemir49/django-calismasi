from django.contrib import admin
from django.urls import path

from . import views
app_name="adverts"
urlpatterns = [

    path('detail/<slug:slug>',views.advertDetail,name="advertDetail"),
    path('',views.adverts,name="adverts"),
    path('recourse/<uuid:id>',views.AddRecourseAdvert,name="recourse"),
    path('removeKeyword/<int:id>',views.removeKeyword,name="removeKeyword"),

]