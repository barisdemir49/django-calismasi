from email import message
from multiprocessing import context
from turtle import title
from unittest import result
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.forms import addKeywords


from .models import Advert,RecourseAdverts,MyKewyords

# Tüm iş ilanlarının gösterilmesi
def advertsContext(request):
    if request.GET.get('q'):
        q=request.GET.get('q')
        data=Advert.objects.filter(isActive=True).filter(
            Q(title__icontains=q) | 
            Q(content__icontains=q) |
            Q(tags__icontains=q)
        ).distinct()
    else:    
        data = Advert.objects.filter(isActive=True)
   
    paginator=Paginator(data,2)
    page=request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data=paginator.page(paginator.num_pages)

    context ={
            "data":data
        }
    return context   

#kullanıcın kaydettiği kriterlere göre iş ilanlarını gösterme
def advertsContextMyKeywords(request):
    pass

#iş ilanlarının listesi. Arama kriterlerine göre filtrelenerek liste oluşturulur. advertsContext üzerinden gelen cotextt verisini aktarır
def adverts(request):
    context =advertsContext(request)
    return render(request,"adverts.html",context)


# iş ilanı detay bilgisi.    
def advertDetail(request,slug):
    data = Advert.objects.filter(slug=slug).first()

    if data:
        tags=data.tags.split(',')
    else:
        return redirect("page404")

    context ={
        "data":data,
        "tags":tags
    }
    return render(request,"advert.html",context)

# ilana başvur
def AddRecourseAdvert(request,id):
    advert=get_object_or_404(Advert,uuid=id)
    
    application=RecourseAdverts(
        author=request.user
    )
    application.advert=advert
    application.save()
    messages.success(request,"Başvurunuz başarıyla alındı.")
    return redirect("/adverts/detail/"+advert.slug)

# iş arama kriterlerim
def myAdvertKeyword(request):
    data = MyKewyords.objects.filter(author=request.user)
    form = addKeywords(request.POST or None)
    if form.is_valid():
        keywords=form.cleaned_data.get("keywords")
        newKeyword= MyKewyords(
            author=request.user,
            keywrods=keywords
        )
        newKeyword.save()
        messages.success(request,"Kriteriniz Eklendi")
    context ={
            "data":data,
            "form":form
        }
    return context  


#Kullanıcı İş İlanı Kelimesini silmek isterse
@login_required(login_url='/user/login')
def removeKeyword(request,id):

    keyword=get_object_or_404(MyKewyords,id=id,author=request.user)
    keyword.delete()
    
    messages.success(request,"Başvurunuz başarıyla alındı.")
    return redirect("users:advertsoptions")