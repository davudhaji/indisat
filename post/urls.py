from django.contrib import admin
from django.urls import path

from . import views

app_name="post"

urlpatterns = [
    path('create/', views.create,name="create"),
    path('delete/<int:id>', views.deleteArticle,name="delete"),
    path('category/<str:ctgry>/<str:nov>', views.Category,name="category"),
    path('product-details/<str:ad>/<int:id>', views.productDetails,name="productDetails"),
    path('categorys/',views.PageCategory,name="PageCategory")
   # path('update/<int:id>', views.updateArticle,name="update"),

]
