from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('products/<str:pk>', views.CategoryDetails.as_view(), name='products'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('add_to_cart/<str:pk>', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<str:pk>', views.delete_from_cart, name='delete_from_cart'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
]

