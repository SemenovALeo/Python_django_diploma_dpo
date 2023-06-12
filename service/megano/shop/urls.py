from django.urls import path
from shop import views



urlpatterns = [
    path('products/popular', views.productsPopular.as_view()),

]
