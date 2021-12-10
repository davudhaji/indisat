from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Elan,Article

class StaticViewSitemap(Sitemap):

    def items(self):
        return ["about","index","post:create"]

    def location(self,item):
        return reverse(item)

class ElanSiteMap(Sitemap):

    def items(self):
        return Elan.objects.all()

class ArticleSiteMap(Sitemap):

    def items(self):

        return Article.objects.all()