from orders.views import Orders, OrderDetail, PaymentView
from django.urls import path

urlpatterns = [
    path("orders/", Orders.as_view()),
    path("orders/<int:pk>/", OrderDetail.as_view()),
    path("payment/<int:pk>/", PaymentView.as_view()),
]
