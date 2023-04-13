import rest_framework.pagination
from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CategorySerializer, ProductSerializer, UserSerializer, CartSerializer
from base.models import Category, Product, Cart
from django.contrib.auth.models import User
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# @method_decorator([cache_page(CACHE_TTL)], name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['price', 'id']
    pagination_class = rest_framework.pagination.CursorPagination
    ordering = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # search_fields = ['name']
    rest_framework.pagination.CursorPagination.ordering = ['id']
    pagination_class = rest_framework.pagination.CursorPagination

    @action(detail=False, methods=['get'])
    def sth(self, request, *args, **kwargs):
        qs = Category.objects.all().order_by('created')

        return Response({'status': 'ok'})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
