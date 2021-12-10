from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from PIL import Image
import PIL
import os
import glob


# Create your models here.

STATUS_CHOICES = [
    ('mnz', 'Mənzillər'),
    ('ovo', 'Obyektlər və ofislər'),
    ('trp', 'Torpaq'),
    ('qrj', 'Qarajlar'),
    ('vvb', 'Villalar, bağ evləri'),
    ('mvi', 'Mebel və interyer'), # Categoriyalarin hamisini Bir bir yaz ! amk
    ('tvt','Temir Ve Tikinti'),
    ('btk','Bitkiler'),
    ('mt','Məişət texnikası'),
    ('qab','Qab-qacaq və mətbəx ləvazimatları'),
    ('ka','Komputer Aksesuarlari'),
    ('nvn','Noutbuklar və Netbuklar'),
    ('pc','Masaüstü kompüterlər'),
    ('nvs','Nömrələr və SİM-kartlar'),
    ('mnt','Komponentlər və monitorlar'),
    ('ft','Foto texnika'),
    ('vls','Velosipedlər'),
    ('ma','Musiqi alətləri'),
    ('iva','İdman və asudə'),
    ('tlf','Telefonlar'),
    ('pve','Planşet və elektron kitablar'),
    ('oav','Ofis avadanlığı və istehlak'),
    ('op','Oyunlar Pultlar ve programlar'),
    ('ehv','Ehtiyat hissələri və aksesuarlar'),
    ('afv','Avtobuslar və xüsusi texnika'),
    ('avt','Avtomobillər'),
    ('aqr','Aqrotexnika'),
    ('mvm','Motoskiletler Ve Mopedler'),
    ('sn','Su nəqliyyatı'),
    ('itl','İtlər'),
    ('huv','Hevanlar ücün Məhsullar'),
    ('dh','Digər heyvanlar'),
    ('psk','Pişiklər'),
    ('qsl','Quşlar'),
    ('avb','Akvarium və balıqlar'),
    ('dgr','Digər'),


]

USER_PACKETS = [

    ('nrml','Normal'),
    ('vip','VIP'),
    ('dmnd','DIAMOND'),
    ('pre','PREMIUM'),

]

ARTICLE_PACKETS=[
    ('nrml','Normal'),
    ('vip','VIP'),
    ('dmnd','DIAMOND'),
    ('pre','PREMIUM'),
]





class Elan(models.Model):
    user = models.CharField(max_length=50,verbose_name="İsdifadəçi Adı")
    title = models.CharField(max_length=50,verbose_name="Başlıq Yazısı ")
    content = RichTextField(verbose_name="Mehsul Haqqında")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Yaradilma Tarixi")
    status = models.CharField(max_length=3,choices=STATUS_CHOICES,verbose_name='category',default=None)
    nomre = models.IntegerField(verbose_name="Telefon Nömrəsi")
    image = models.ImageField(blank=True,verbose_name="Səkil Əlavə Et")
    qiymet = models.IntegerField(verbose_name="Qiymət")
    packet = models.CharField(choices=ARTICLE_PACKETS,verbose_name="Paketler",default="Normal",max_length=50)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
            img.save(self.image.path,optimize=True,quality=30)
        except:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("user:elanDinamik", args=[self.id])





class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Isdifadeci")
    title = models.CharField(max_length=50,verbose_name="Basliq")
    content = RichTextField(verbose_name="Mehsul Hakkinda")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Yaradilma Tarixi")
    status = models.CharField(max_length=3,choices=STATUS_CHOICES,verbose_name='category',default=None)
    nomre = models.IntegerField(verbose_name="Telfon Nomresi")
    image = models.ImageField(blank=True,verbose_name="Sekil Elave Et")
    qiymet = models.IntegerField(verbose_name="Qiymet")
    packet = models.CharField(choices=ARTICLE_PACKETS,verbose_name="Paketler",default="Normal",max_length=50)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
            img.save(self.image.path,optimize=True,quality=30)
        except:
            super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("dynamic", args=[self.id])


class ArticleImage(models.Model):
    product = models.ForeignKey('Article',on_delete=models.CASCADE)
    product_image = models.ImageField(blank=True,upload_to="images/")

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.product_image.path)
            img.save(self.product_image.path,optimize=True,quality=30)
        except:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.product.title + "Image"


class ElanImage(models.Model):
    product = models.ForeignKey('Elan',on_delete=models.CASCADE)
    product_image = models.ImageField(blank=True,upload_to="images/")
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.product_image.path)
            img.save(self.product_image.path,optimize=True,quality=30)
        except:
            super().save(*args, **kwargs)
    def __str__(self):
        return self.product.title + "Image"





class ArticleCategory(models.Model):
    product = models.ForeignKey('Article',on_delete=models.CASCADE)
    category = models.CharField(max_length=50,choices=STATUS_CHOICES,verbose_name="Category")

    def __str__(self):
        return self.category

class ElanCategory(models.Model):
    product = models.ForeignKey('Elan',on_delete=models.CASCADE)
    category = models.CharField(max_length=50,choices=STATUS_CHOICES,verbose_name="Category")

    def __str__(self):
        return self.category






class PacketsUsers(models.Model):
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Isdifadeci")
    packet = models.CharField(choices=USER_PACKETS,verbose_name="Paketler",default="Normal",max_length=50)

    def  __str__(self):
        return self.user.username


"""

class PacketsArticle(models.Model):
    elan = models.ForeignKey("Article",on_delete=models.CASCADE,verbose_name="Elan")
    packet = models.CharField(choices=ARTICLE_PACKETS,verbose_name="Paketler",default="Normal",max_length=50)
    def  __str__(self):
        return self.elan.title

class PacketElan(models.Model):
    elan = models.ForeignKey("Elan",on_delete=models.CASCADE,verbose_name="Elan")
    packet = models.CharField(choices=ARTICLE_PACKETS,verbose_name="Paketler",default="Normal",max_length=50)
    def  __str__(self):
        return self.elan.title

"""