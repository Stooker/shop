from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:pk>', views.products_of_category, name='products'),
]

