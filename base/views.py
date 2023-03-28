from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import base.models
from .models import Category, Product
# Create your views here.


def home(request):

    categories = Category.objects.all()
    context = {'categories':categories}

    return render(request, 'base/home.html', context)


def products_of_category(request, pk):

    category = Category.objects.get(id=pk)

    try:
        products = Product.objects.get(category=category)
    except Product.DoesNotExist:
        products = {}
        messages.error(request, 'This category is empty')

    context = {'category':category, 'products':products}

    return render(request, 'base/products.html', context)