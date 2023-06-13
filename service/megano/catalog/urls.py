from django.urls import path
from .views import Catalog, BannersList, CategoriesList

urlpatterns = [
    path('catalog/', Catalog.as_view(), name='products_list'),
    path('banners/', BannersList.as_view(), name='banners'),
    path('categories/', CategoriesList.as_view(), name='categories'),
]