from django.urls import path

from cart.views import BasketOfProductsView

app_name = 'cart'

urlpatterns = [
    path('basket/', BasketOfProductsView.as_view(), name='basket'),
    path('orders/', BasketOfProductsView.as_view(), name='cart'),
]
