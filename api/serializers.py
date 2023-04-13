from base.models import Category, Product, Cart, ProductCart
from rest_framework import serializers
from django.contrib.auth.models import User


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # product_set = serializers.HyperlinkedRelatedField(many=True, view_name='product-detail',
                                                      # queryset=Product.objects.all())

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'product_set']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), view_name='category-detail')

    class Meta:
        model = Product
        fields = ['url', 'name', 'description', 'category', 'price', 'quantity']


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'products']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'cart_set']
