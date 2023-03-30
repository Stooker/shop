from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, ProductCart, Cart
from .forms import RegistrationForm
from django.views.generic import ListView, DetailView, View, TemplateView


class HomePage(ListView):
    template_name = 'base/home.html'
    context_object_name = 'categories'
    model = Category


class CategoryDetails(DetailView):
    template_name = 'base/products.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetails, self).get_context_data(*args, **kwargs)
        categories = Category.objects.all()
        products = Product.objects.filter(category=context['category'])

        if len(products) == 0:
            messages.error(self.request, 'This category is empty')

        context['categories'] = categories
        context['products'] = products

        return context


# class ProductsOfCat(TemplateView):
#     template_name = 'base/products.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductsOfCat, self).get_context_data(**kwargs)
#         pk = self.kwargs['pk']
#         context['categories'] = Category.objects.all()
#         context['category'] = Category.objects.get(id=pk)
#         context['products'] = Product.objects.filter(category=Category.objects.get(id=pk))
#
#         if len(context['products']) == 0:
#             messages.error(self.request, 'This category is empty')
#
#         return context

class CartView(ListView):
    template_name = 'base/cart.html'
    context_object_name = 'products'
    model = ProductCart

    def get_cart(self):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except:
            messages.error(self.request, "Your cart is empty")
            return False
        return cart

    def get_queryset(self):
        cart = self.get_cart()
        if cart:
            qs = super().get_queryset()
            return qs.filter(cart=cart)

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(*args, **kwargs)
        cart = self.get_cart()

        if cart:
            context["cart"] = cart
        return context



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
    print(f'added {pk}')
    cart, c_created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=pk)
    product_cart, pc_created = ProductCart.objects.get_or_create(cart=cart, product=product)

    product_cart.quantity += quantity
    product_cart.save()
    category = product.category.id
    return redirect('products', category)


@login_required(login_url='login')
def delete_from_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
    product_cart = ProductCart.objects.get(id=pk)
    product_cart.delete()

    return redirect('cart')
