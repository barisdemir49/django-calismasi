import email
from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse

from adverts.models import MyKewyords
from .forms import RegisterForm,LoginForm,ForgetPassForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.core.mail import send_mail,BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from django.urls import reverse_lazy

import adverts

# Kullanıcı modülü ile bağımlı ve harici arayüz ve uygulamalar ile kullanıcının kendi hesabını yönetmesi
#Kullanıcı Oturum açma işlemi
def loginUser(request):
    form =LoginForm(request.POST or None)
    context={
        "form":form
    }
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        if user is None:
            messages.warning(request,"Hatalı kullanıcı adı veya parola!")
        
        login(request,user)
        messages.success(request,"Oturumunuz başarıyla açıldı")
        return redirect("users:dashboard")

    return render(request,"user/login.html",context)



#Kullanıcı oturum sonlandırma işlemi
def logoutUser(request):
    logout(request)
    messages.success(request,"Oturumunuz başarıyla kapatıldı")
    return redirect("index")




#kayıt olma formu üzerinden yeni üyelik kaydının alınması
def register(request):
    form =RegisterForm(request.POST or None)
    if form.is_valid():
        first_name=form.cleaned_data.get("first_name")
        last_name=form.cleaned_data.get("last_name")
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        email=form.cleaned_data.get("email")

        newUser=User(username=username)
        newUser.set_password(password)
        newUser.email=email
        newUser.first_name=first_name
        newUser.last_name=last_name

        newUser.save()
        login(request,newUser)
        messages.success(request,"Başarıyla kayıt oldunuz...")
        return redirect('index')

    context = {
        "form":form
    }
    return render(request,"user/register.html",context)



# barisdemir@kartepeinternet.com.tr
#Kullanıcı şifresini unutması durumunda email adresini girerek şifre resetleme linkini almasını sağlayacak kısım
def forgetpass(request):
    form = ForgetPassForm(request.POST or None)
    if form.is_valid():
        email =form.cleaned_data.get("email")
        data=get_object_or_404(User,email=email)
        if data:
            subject = "Şifre Yenileme Linki"
            c = {
				"email":email,
				'domain':'127.0.0.1:8000',
				"uid": urlsafe_base64_encode(force_bytes(data.pk)),
				'token': default_token_generator.make_token(data),
				'protocol': 'http',
		 	    }
            emailData = render_to_string("user/reset_pass.txt", c)

            try:
                send_mail(subject,emailData,'admin@admin.com',[email])
            except BadHeaderError as e: 
                return HttpResponse(e)
            messages.success(request,"Şifre değiştirme linki email adresinize gönderlmiştir.")
            return redirect ("index")
    context = {
        "form":form
    }
    return render(request,"user/forgetpass.html",context)



#şifre resetleme linkine tıklandığında yeni şifre girilecek işlemler
def resetpass(request):
    return render(request,"user/resetpass.html")


class PasswordChangeView(PasswordChangeView):
    form =PasswordChangeView
    success_url: reverse_lazy('dashboard')

#Sistemde oturum açan üyenin kendi paneli
@login_required(login_url='/user/login')
def dashboard(request):
    context=adverts.views.advertsContext(request)
    return render(request,"dashboard.html",context)


#Kullanıcı sifresini güncellemek isterse
@login_required(login_url='/user/login')
def password_success(request):
    messages.success(request,"Şifreniz başarıyla değiştirildi")
    return render(request,"dashboard.html")

#Kullanıcı genel bilgilerini güncellemek isterse
@login_required(login_url='/user/login')
def changeprofile(request):
    return render(request,"user/changeprofile.html")
    
#Kullanıcı genel iş arama tercihlerini güncellemek isterse
@login_required(login_url='/user/login')
def advertsOptions(request):
    context=adverts.views.myAdvertKeyword(request)
    return render(request,"advertsOptions.html",context)
