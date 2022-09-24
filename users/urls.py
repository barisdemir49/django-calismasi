from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as authViews
from django.urls import reverse_lazy

from . import views
from .views import PasswordChangeView


app_name="users"
urlpatterns = [
    path('login',views.loginUser,name="loginUser"),
    path('logout',views.logoutUser,name="logoutUser"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('register',views.register,name="register"),
    path('forgetpass',views.forgetpass,name="forgetpass"),
    path('resetpass/<uidb64>/<token>/',authViews.PasswordResetConfirmView.as_view() ,name="resetpass"),
    path('success_password',views.password_success,name='password_success'),
    path('changepass',PasswordChangeView.as_view(
        template_name='user/changeMyPass.html',
        success_url=reverse_lazy('users:password_success')
    ),name="changepass"),
    path('changeprofile',views.changeprofile,name="changeprofile"),
    path('adverts-options',views.advertsOptions,name="advertsoptions"),

]