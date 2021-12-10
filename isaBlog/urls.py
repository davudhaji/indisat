"""isaBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from post import views
from post.sitemaps import StaticViewSitemap,ElanSiteMap,ArticleSiteMap

app_name="isaBlog"


sitemaps={
    'static': StaticViewSitemap,
    'elan' : ElanSiteMap,
    'article' : ArticleSiteMap,
}


urlpatterns = [
    path('davudhaji/admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.index,name="index"),
    path('sitemap.xml', sitemap,{'sitemaps':sitemaps}),
    path('davudhaji/', views.about,name="about"),
    path('sticker/<int:id>',views.dynamic,name="dynamic"),
    path('sticker/<int:id>/buy/',views.buySticker,name="buySticker"),
    path('article/', include("post.urls")),
    path('user/', include("user.urls")),
    path('complete/', views.complete, name="complete"),




]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)