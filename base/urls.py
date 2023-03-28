from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:pk>', views.products_of_category, name='products'),
    path('cart', views.user_cart, name='cart'),
    path('add_to_cart/<str:pk>', views.add_to_cart, name='add_to_cart'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
]

