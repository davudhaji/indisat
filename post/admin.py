from django.contrib import admin
from .models import Article,ArticleImage,ArticleCategory,PacketsUsers,Elan,ElanImage,ElanCategory

# Register your models here.
class ImageInlines(admin.TabularInline):
    model = ArticleImage
    extra = 2
    min_num =0
    max_num = 15

class ElanInlines(admin.TabularInline):
    model = ElanImage
    extra = 2
    min_num =0
    max_num = 15

@admin.register(ArticleCategory)
class CategoryArticle(admin.ModelAdmin):
    list_filter=["product","category"]
    list_display=["product","category"]

    class Meta:
        model = ArticleCategory

@admin.register(ElanCategory)
class CategoryArticle(admin.ModelAdmin):
    list_filter=["product","category"]
    list_display=["product","category"]

    class Meta:
        model = ElanCategory



@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_filter=["created_date","qiymet"]
    list_display=["title","author","created_date","packet","qiymet"]
    list_display_links=["title"]
    search_fields=["title",'content']
    inlines = [ImageInlines]

    class Meta:
        model=Article

@admin.register(ArticleImage)
class AdminArticleImage(admin.ModelAdmin):

    class Meta:
        model = ArticleImage

@admin.register(PacketsUsers)
class AdminUserPacket(admin.ModelAdmin):
    search_fields=['packet']
    list_display=['user','packet']

    class Meta:
        model = PacketsUsers


@admin.register(Elan)
class AdminElan(admin.ModelAdmin):
    list_display=['user','title','qiymet','packet']
    search_fields=['title','user','qiymet']
    inlines=[ElanInlines]
    class Meta:
        model = Elan



@admin.register(ElanImage)
class AdminElanImages(admin.ModelAdmin):

    class Meta:
        model = ElanImage