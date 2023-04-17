from django.urls import path
from .views import *

urlpatterns = [
    path('',Index.as_view(),name="home"),
    path('search/',search,name="search_page"),
    path('category/',Categories.as_view(),name="categories"),
    path('category_detail/<int:pk>/',Category_Detail.as_view(),name="category_detail"),
    path('product/<int:pk>/',Product_Detail.as_view(),name="product_detail"),
    path('zakazat/<int:id>/',zakazat,name="zakazat"),
    path('pod_category/<int:pk>/',Pod_Category_Detail.as_view(),name="pod_category_detail"),

    path('reg/',signup,name="reg"),
    path('rating/<int:id>/',rating,name="rating_product")
]