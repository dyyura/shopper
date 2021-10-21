from django.urls import path
from rest_framework.urls import urlpatterns
from rest_framework.routers import DefaultRouter
from product.views import *

routers = DefaultRouter()

routers.register('product', ProductViewSet)
routers.register('category', CategoryViewSet)
routers.register('cartproduct', CartProductViewSet)
routers.register('cart', CartViewSet)
routers.register('customer', CustomerViewSet)
routers.register('order', OrderViewSet)

urlpatterns + routers
