from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, ProductCart, Cart
from .forms import RegistrationForm


def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    return render(request, 'base/home.html', context)


def products_of_category(request, pk):
    categories = Category.objects.all()
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category=category)

    if len(products) == 0:
        messages.error(request, 'This category is empty')

    # except:
    #     products = {}
    #     messages.error(request, 'This category is empty')

    context = {'category': category, 'products': products, 'categories': categories}

    return render(request, 'base/products.html', context)


def user_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        products = ProductCart.objects.filter(cart=cart)
        context = {"cart": cart, 'products': products}
    except:
        context = {}
        messages.error(request, "Your cart is empty")
    return render(request, 'base/cart.html', context)


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnt exist')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid data')
    context = {'page': page}
    return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)

    context = {'form': form}
    return render(request, 'base/login.html', context)


@login_required(login_url='login')
def add_to_cart(request, pk):

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])

    cart, c_created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=pk)
    product_cart, pc_created = ProductCart.objects.get_or_create(cart=cart, product=product)


    product_cart.quantity += quantity
    product_cart.save()




    category = product.category.id
    return products_of_category(request, category)
