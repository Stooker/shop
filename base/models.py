from django.db import models
from django.conf import settings
from django.contrib.admin import ModelAdmin


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    picture = models.ImageField(null=True, blank=True, default="index.jpeg")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductCart')

    # created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Koszyk {self.user}"


class ProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.cart} {self.product}"


class ProductCartAdmin(ModelAdmin):
    readonly_fields = ('id',)
