from django.contrib import admin
from .models import Product, ProductCart, Category

admin.site.register(Product)
admin.site.register(ProductCart)
admin.site.register(Category)