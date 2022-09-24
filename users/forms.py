import email
from django import forms


class RegisterForm(forms.Form):
    first_name=forms.CharField(max_length=20,label="Adınız")
    last_name=forms.CharField(max_length=20,label="Soy Adınız")
    username=forms.CharField(max_length=20,label="Kullanıcı Adınız")
    password=forms.CharField(max_length=20,label="Şifreniz",widget=forms.PasswordInput)
    configm=forms.CharField(max_length=20,label="Şifrenizi Doğrulayınız",widget=forms.PasswordInput)
    email=forms.CharField(max_length=50,label="Email Adresiniz")


    def clean(self):
        first_name=self.cleaned_data.get("first_name")
        last_name=self.cleaned_data.get("last_name")
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        confirm=self.cleaned_data.get("confirm")
        email=self.cleaned_data.get("email")

        if password and confirm and password!=confirm:
            raise forms.ValidationError("Parollalarınız aynı değil!")

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20,label="Kullanıcı Adınız")
    password=forms.CharField(max_length=20,label="Şifreniz",widget=forms.PasswordInput)

    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
            

class ForgetPassForm(forms.Form):
    email=forms.EmailField(max_length=100,label="E-mail adresiniz")

    def clean(self):
        email=self.cleaned_data.get("email")

class addKeywords(forms.Form):
    keywords=forms.CharField(max_length=20, label="İş Arama Etiketi")

    def clean(self):
        keywords=self.cleaned_data.get("keywords")