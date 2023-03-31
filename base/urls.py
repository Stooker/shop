from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('products/<str:pk>', views.CategoryDetails.as_view(), name='products'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('add_to_cart/<str:pk>', views.AddToCart.as_view(), name='add_to_cart'),
    path('delete_from_cart/<str:pk>', views.DeleteFromCart.as_view(), name='delete_from_cart'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('product_details/<str:pk>', views.ProductDetails.as_view(), name='product_details'),
]

