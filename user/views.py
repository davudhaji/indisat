from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from . import forms
from django.contrib.auth.models import User
# Create your views here.
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
#from django.shortcuts import HttpResponseRedirect
from post.models import Article,ElanCategory,ArticleImage,ArticleCategory,PacketsUsers,Elan,ElanImage

from django.core.files.storage import FileSystemStorage

from django.contrib.auth.decorators import login_required
from PIL import Image
import PIL
import os
import glob

valid = [".jpg",".jpeg",".png",".jfif"]


cavab = None
def dec(fun):
    def wrapper(data):
        son = fun(data)
        print(data.user.password[:6],"dataaa22222")
        global cavab
        if data.user.password[:6] == "pbkdf2":
            cavab = True
            return son
        else:
            cavab = False
            return redirect("/user/wc/")

    return wrapper

def kole(ls):
    allinone = ls
    one =[]
    for i in allinone:
        for j in i:
            one+=[j]



    def SortKey(word):  # burdaki word'a sorted funksiyasi "one" listinin icerisindeki elmentleri gezir ve SortKeye gonderir davami--
        return word.created_date # burdada biz created_date(yeni meselcun one[0].create_date kimi) e gore sortlasdiracaqimizi bildiririik.

    one = sorted(one,key=SortKey)[::-1]  #Sort modulunun key parametri heyat qurtariri ! :D



    palasa = len(one)//4 + 1
    x = 0

    son=[]
    for i in range(palasa):
        son+=[one[x:x+4]]
        x+=4

    return son


def warningChange(request):
    messages.warning(request,"Facebook ve Ya Google İle Daxil olmusunuzsa parolu dəyişdirə bilmərsiniz")
    return redirect("/")

def UserLogout(request):
    logout(request)
    messages.success(request,"Hesabinizdan Cixis Etdiniz")
    return redirect("index")


def register(request):
    if request.user_agent.is_mobile: #mobile

        if request.method == "POST":
            pass
        else:

            return render(request,"mobile/sign-up.html")



    if request.method=="POST":
        try:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")

                newUser = User(first_name=first_name,last_name=last_name,username=username,email=email)
                newUser.set_password(password)
                newUser.save()

                Packet= PacketsUsers()
                Packet.user=newUser
                Packet.packet='nrml'
                Packet.save()


                messages.success(request, 'Qeydiyatdan Ugurla Kecdiniz !')

                return redirect("index")
        except:
            messages.warning(request, 'Bele Isdifadeci Adi Artiq Movcuddur!')

            return redirect("/user/register")
        else:

            form = forms.RegisterForm()

            content={
                "form":form
            }

            messages.warning(request, 'Parollari Duzgun Yazin')
            return render(request,"register.html",content)
    else:
        form = forms.RegisterForm()

        content={
            "form":form
        }

        return render(request,"register.html",content)

def LoginUser(request):

    if request.user_agent.is_mobile: #mobile versiyasi

        if request.POST:
            username=request.POST['username']
            password=request.POST['pass']
            
            newUser = authenticate(request,username=username,password=password)

            if newUser is None:
                
                messages.warning(request, 'Isdifadeci Adi Veya Parol Yanlisdir')
                
                return render(request,"mobile/sign-in.html")
            
            messages.success(request, 'Ugurla Daxil Oldunuz')
            
            login(request,newUser)
            
            return redirect("/")
        else:

            return render(request,"mobile/sign-in.html")


    form = forms.LoginForm(request.POST or None)

    content = {
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")


        newUser = authenticate(request,username=username,password=password)

        if newUser is None:


            messages.warning(request, 'Isdifadeci Adi Veya Parol Yanlisdir')
            return render(request,"login.html",content)

        messages.success(request, 'Ugurla Daxil Oldunuz')
        login(request,newUser)

        return redirect("index")




    return render(request,"login.html",content)


@login_required(login_url="/user/login")
def dashboard(request):
    keyword=request.GET.get("elan")
    print(keyword)
    if keyword:
        articles = Article.objects.filter(author=request.user,title__contains=keyword)[::-1]

        return render(request,'dashboard.html',{"articles":articles})



    articles = Article.objects.filter(author=request.user)
    print(articles,"ARTICLEESS")
    content = {

        "articles":articles[::-1],

    }






    return render(request,"dashboard.html",content)



@login_required(login_url='/user/login')
def vip(request):


    content={
        "vip":'salam'
    }

    return render(request,"vip.html",content)





@login_required(login_url="/user/login")
def sticker(request):
    if request.method == "POST":
        form = forms.StickerForm(request.POST,request.FILES)

        if form.is_valid():
            Sticker = form.save(commit=False)
            Sticker.author = request.user
            imgHead = request.FILES.get("image")
            if not (imgHead.name[-4:] in valid or imgHead.name[-5:] in valid ):

                messages.warning(request,"Şəkili Düzgün Daxil Edin !")
                return redirect("/")
            ctgry = request.POST.get("status")
            Sticker.status = ctgry
            Sticker.packet = 'nrml'

            fs = FileSystemStorage()
            file_path=fs.save(imgHead.name,imgHead)

            Sticker.image = file_path



            #Sticker.product = Article.objects.get(id=Sticker.id)

            Sticker.save()

            ac  = ArticleCategory()

            ac.product = Sticker
            ac.category= ctgry
            ac.save()


            try:
                files = request.FILES.getlist("file[]")
                for img in files:
                    if not (img.name[-4:] in valid or img.name[-5:] in valid ):
                        messages.warning(request,"Şəkili Düzgün Daxil Edin !")
                        return redirect("/")

                    print (img)
                    newfs=FileSystemStorage()
                    newPath= newfs.save(img.name,img)



                    newImage = ArticleImage(product=Sticker,product_image=newPath)
                    newImage.save()
                if request.user_agent.is_mobile:#mobile
                    return redirect(reverse('post:productDetails',kwargs={"id":Sticker.id,"ad":"sticker"}))
                
                else:
                    return redirect(reverse('dynamic',kwargs={"id":Sticker.id})) # burda dynamic esas url faylinda oldugu ucun qabaqina isaBlog yazilmir cunki main di ozu birinci ora baxir





            except:



                if request.user_agent.is_mobile:#mobile
                    return redirect(reverse('post:productDetails',kwargs={"id":Sticker.id,"ad":"sticker"}))

                else:
                    return redirect(reverse('dynamic',kwargs={"id":Sticker.id}))



    form = forms.StickerForm()
    content={
        "form":form,
    }


    if request.user_agent.is_mobile:#mobile
        return redirect(reverse('post:productDetails',kwargs={"id":Sticker.id,"ad":"sticker"}))

    else:
        return redirect(reverse('dynamic',kwargs={"id":Sticker.id}))

def elan(request):
    if request.method == "POST":
        form = forms.ElanForm(request.POST,request.FILES)

        if form.is_valid():
            Sticker = form.save(commit=False)
            imgHead = request.FILES.get("image")
            ctgry = request.POST.get("status")
            Sticker.status = ctgry
            Sticker.packet = 'nrml'

            if not (imgHead.name[-4:] in valid or imgHead.name[-5:] in valid ):

                messages.warning(request,"Şəkili Düzgün Daxil Edin !")
                return redirect("/")


            fs = FileSystemStorage()
            file_path=fs.save(imgHead.name,imgHead)

            Sticker.image = file_path

            print(imgHead,"IMGGG HEEAADDD")

            #Sticker.product = Article.objects.get(id=Sticker.id)

            Sticker.save()




            ac  = ElanCategory()

            ac.product = Sticker
            ac.category= ctgry
            ac.save()



            try:
                files = request.FILES.getlist("file[]")
                for img in files:
                    print (img)
                    if not (img.name[-4:] in valid or img.name[-5:] in valid ):
                        messages.warning(request,"Şəkili Düzgün Daxil Edin !")
                        return redirect("/")

                    newfs=FileSystemStorage()
                    newPath= newfs.save(img.name,img)



                    newImage = ElanImage(product=Sticker,product_image=newPath)
                    newImage.save()

                if request.user_agent.is_mobile:#mobile
                    return redirect(reverse('post:productDetails',kwargs={"id":Sticker.id,"ad":"elan"}))
               
                else:
                    messages.success(request, 'Elanınız Uğurla yerləsdirildi')
                    return redirect(reverse('user:productDetails',kwargs={"id":Sticker.id}))




            except:


                if request.user_agent.is_mobile:#mobile
                    return redirect(reverse('post:productDetails',kwargs={"id":Sticker.id,"ad":"elan"}))

                else:
                    messages.success(request, 'Elanınız Uğurla yerləsdirildi')
                    return redirect(reverse('user:elanDinamik',kwargs={"id":Sticker.id}))  
                    #burda reverse user in icerisindeki urls baxir ve adi elanDinamik olan urlni cagiriri ve yaninada id ni yerlesdirir
        
        if request.user_agent.is_mobile:
            return redirect(reverse('post:productDetails',kwargs={"id":Sticker.id,"ad":"elan"}))

        else:
            messages.warning(request, '"Məhsul Haqqında" Bölməsini doldurmalısınız')
            return redirect('/user/elan')


    else:

        form=forms.ElanForm()



        if request.user_agent.is_mobile:
            return render(request,"mobile/mobElan.html",{"form":form})

        else:

            return render(request,"Elan.html",{"form":form})


def elanDinamik(request,id):

    articlenow = get_object_or_404(Elan,id=id)
    articles = Article.objects.filter(status=articlenow.status,packet='nrml')[::-1][:4] # [:10] Butun Articllar Sonuncu 10 dene

    elanlar = Elan.objects.filter(status=articlenow.status,packet='nrml')[::-1][:4] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq

    Premiumarticles = Article.objects.filter(status=articlenow.status,packet='pre')[::-1][:4] # [:10] Butun Articllar Sonuncu 10 dene

    Premiumelanlar = Elan.objects.filter(status=articlenow.status,packet='pre')[::-1][:4] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq

    son = kole([articles,elanlar])
    pre = kole([Premiumarticles,Premiumelanlar])

    try:
        articleImages=ElanImage.objects.filter(product = articlenow)
        print(articleImages,'\n',articleImages[0].product_image.url,"BUUUUU ARTICCCLEEE IMAGEESSSDIR")
        content = {
            'article':articlenow,
            'articleImages':articleImages,
            'son':son,
            'pre':pre,
        }

        return render(request,"product.html",content)
    except:


        content = {
            "article":articlenow,
            'son':son,
            'pre':pre,
        }

        return render(request,"product.html",content)


@login_required(login_url="/user/login")
def settings(request):
    try:
        if request.method == "POST":
            print(request.POST)
            user1 = get_object_or_404(User,id=request.user.id)
            user1.username = request.POST.get("username")#request.POST.get("username")[0],last_name=request.POST.get("last_name")[0],first_name=request.POST.get("first_name")[0],email=request.POST.get("email")[0]
            user1.last_name = request.POST.get("last_name")
            user1.first_name = request.POST.get("first_name")
            user1.email = request.POST.get("email")

            user1.save()

            messages.success(request,"Melumatlariniz Yenilendi")

            return redirect("/")
    except:

        messages.warning(request,"Belə bir isdifadəçi adı artıq mövcüddur")

        return redirect("/user/settings/")



    user = get_object_or_404(User,id=request.user.id)
    userForm = forms.UserForm(instance=user)

    return render(request,"settings.html",{"form":userForm})
@dec
def change(request):

    return redirect("/user/password/")


class PasswordReverse(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = "/user/passSuccess/"




def success(request):

    messages.success(request,"Parolunuz dəyişdirildi")
    return redirect("/user/password")

@login_required(login_url="/user/login")
def buy(request,packet):

    return render(request,"buy.html",{"packet":packet})

@login_required(login_url="/user/login/")
def buyElan(request,id):

    return render(request,"buy.html",{"id":id,"type":"elan"})