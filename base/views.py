from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Product
# Create your views here.


def home(request):

    categories = Category.objects.all()
    context = {'categories':categories}

    return render(request, 'base/home.html', context)


def products_of_category(request, pk):

    products = Product.object.get(id=pk)

    context = {'products':products}

    return render(request, 'products.html')