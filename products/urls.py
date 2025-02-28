from django.urls import path
from .views import ProductAPIView, ProductDetailAPIView


app_name='products'

urlpatterns = [
    path('', ProductAPIView.as_view(), name='products-list'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]