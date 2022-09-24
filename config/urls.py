from unicodedata import name
from django.contrib import admin
from django.urls import path,include

from homepage import views

#site ve modüllerin url yönlendirmeleri. yoğun modüllerin url bilgileri kendi içinde oluşturulup buraya include edilmistir.
urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.index,name="index"),
    path('user/',include("users.urls")),
    path('adverts/',include("adverts.urls")),
    path('404.html',views.page404,name="page404"),
    path('hakkimizda.html',views.hakkimizda,name="hakkimizda")

]