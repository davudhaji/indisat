from django import forms

from django.core.exceptions import ValidationError
from post.models import Article,Elan
from multiupload.fields import MultiFileField
from django.contrib.auth.models import User



class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50,label="Ad")
    last_name = forms.CharField(max_length=50,label="Soyad")
    username = forms.CharField(max_length=50,label="Isdifadeci Adi")
    email = forms.EmailField(max_length=50,label="Email")
    password = forms.CharField(max_length=20,label="Parol",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=50,widget=forms.PasswordInput,label="Tekrar Parol")

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if (password != confirm and password!="") or password=="":
            raise ValidationError("Parollari Duzgun Daxil Et")

            #burda django mejsaylari ile mesaj gonder parollarda seflik olduqu hakda

        values={
            "first_name":first_name,
            "last_name":last_name,
            "username":username,
            "email":email,
            "password":password,

        }

        return values 


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,label="Username")
    password = forms.CharField(max_length=50,label="Parol",widget=forms.PasswordInput)
    
    """
    Burda clean ozu oz ozune yaranir hec bir sert qoymadiqimaza gore bos bosuna clean metodunu yazmaqa ehtiyac yoxdur.
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        values = {
            "username":username,
            "password":password,
        }
        return values
    """

class StickerForm(forms.ModelForm):


    class Meta:
        model = Article
        fields = ['title','content','nomre','qiymet']


class ElanForm(forms.ModelForm):
    
    class Meta:
        model = Elan
        fields = ['user','title','content','nomre','qiymet']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

