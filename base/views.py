from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, ProductCart, Cart
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, RedirectView, FormView


class HomePage(ListView):
    template_name = 'base/home.html'
    context_object_name = 'categories'
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products'] = Product.objects.all()
        return context


class CategoryDetails(DetailView):
    template_name = 'base/products.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetails, self).get_context_data(*args, **kwargs)
        categories = Category.objects.all()
        products = Product.objects.filter(category=context['category']).filter(quantity__gt=0)

        if len(products) == 0:
            messages.error(self.request, 'This category is empty')

        context['categories'] = categories
        context['products'] = products

        return context


class CartView(ListView):
    template_name = 'base/cart.html'
    context_object_name = 'products'
    model = ProductCart
    summary = 0

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
            qs = super().get_queryset().filter(cart=cart)
            for prod in qs:
                self.summary += prod.product.price*prod.quantity
                print(prod.product.price)

            return qs

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(*args, **kwargs)
        cart = self.get_cart()

        if cart:
            context["cart"] = cart
            context["summary"] = self.summary
        return context


class Login(LoginView):
    template_name = 'base/login.html'
    page = 'login'

    def post(self, request, *args, **kwargs):
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
        return super().post(request, *args, **kwargs)


class Logout(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class Register(FormView):
    form_class = RegistrationForm
    success_url = '/'
    template_name = 'base/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context['form'] = RegistrationForm()
        return context


class AddToCart(LoginRequiredMixin, RedirectView):
    pattern_name = 'products'
    login_url = 'login'
    category = 0

    def post(self, request, **kwargs):
        quantity = int(self.request.POST['quantity'])
        pk = self.kwargs['pk']
        cart, c_created = Cart.objects.get_or_create(user=self.request.user)
        product = Product.objects.get(id=pk)
        product.quantity -= quantity
        product.save()
        product_cart, pc_created = ProductCart.objects.get_or_create(cart=cart, product=product)
        product_cart.quantity += quantity
        product_cart.save()
        messages.success(request, "Succesfully added to cart!")
        self.category = product.category.id
        return super().post(request, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, pk=self.category)


class DeleteFromCart(LoginRequiredMixin, RedirectView):
    pattern_name = 'cart'
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        quantity = int(request.POST['quantity'])
        product_cart = ProductCart.objects.get(id=self.kwargs['pk'])
        product = Product.objects.get(id=product_cart.product.id)

        product.quantity += quantity
        product.save()
        messages.error(request, "Succesfully removed from cart")

        product_cart.quantity -= quantity
        product_cart.save()
        if product_cart.quantity == 0:
            product_cart.delete()

        return redirect('cart')


class ProductDetails(DetailView):
    template_name = 'base/product_details.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

