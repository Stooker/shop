from django.contrib import admin
from .models import Product, Cart, Category, ProductCart

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(ProductCart)