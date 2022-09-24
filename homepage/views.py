from django.shortcuts import render

# Temel anasayfa ile ilgili işlemlerin ve yönlendirmelerin yapıldığı işlemler
def index(request):
    return render(request,"index.html")

def page404(request):
    return render(request,"404.html")

def hakkimizda(request):
    return render(request,"hakkimizda.html")