from django.urls import path
from .views import OrderAPIView, OrderDetailAPIView


app_name='orders'

urlpatterns = [
    path('', OrderAPIView.as_view(), name='orders-list'),
    path('<int:pk>', OrderDetailAPIView.as_view(), name='order-detail'),
]