from django.urls import path
from . import views
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('products/0', views.HomePage.as_view(), name='home_0'),
    path('products/<str:pk>', cache_page(CACHE_TTL)(views.CategoryDetails.as_view()), name='products'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('add_to_cart/<str:pk>', views.AddToCart.as_view(), name='add_to_cart'),
    path('delete_from_cart/<str:pk>', views.DeleteFromCart.as_view(), name='delete_from_cart'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('product_details/<str:pk>', views.ProductDetails.as_view(), name='product_details'),
    path('make_order', views.MakeOrder.as_view(), name='make_order'),
]

