from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as view
from . import views

app_name="user"
                        #MENBE
urlpatterns = [       #Funkisya Adi Backend
                        #  |
                      #    ^
    path('register/', views.register,name="register"),
    path('login/', views.LoginUser,name="login"),
    path('logout/', views.UserLogout,name="logout"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('sticker/', views.sticker,name="sticker"),
    path('vip/', views.vip,name="vip"),
    path('settings/', views.settings,name="settings"),
    path('yoxla/', views.change,name="yoxla"),
    path('wc/', views.warningChange,name="warningChange"),
    #path('password/', view.PasswordChangeView.as_view(template_name="pass.html")),
    #path('password/',views.PasswordChangeView.as_view(template_name="pass.html"),name="password"),
    path('password/',views.PasswordReverse.as_view(template_name="pass.html"),name="password"),
    path('elan/', views.elan,name="elan"),
    path('buy/<str:packet>', views.buy,name="buy"),
    path('passSuccess/', views.success,name="passSuccess"),
    path('elan/<int:id>', views.elanDinamik,name="elanDinamik"),
    path('elan/<int:id>/buy/', views.buyElan,name="buyElan"),




]
