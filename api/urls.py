from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet, UserViewSet, CartViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'user', UserViewSet, basename='user')
router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = [
    # path('', include()),
    path('', include(router.urls)),
]

