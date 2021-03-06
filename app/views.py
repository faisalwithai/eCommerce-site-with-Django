from itertools import product
from statistics import quantiles
from unicodedata import category
from django.shortcuts import redirect, render
from django.views import View
from .models import Cart, Product, OrderPlaced, Customer
import json
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .forms import CustomerProfileForm, CustomerRegistrationFrom, UserCreationForm
from django.contrib.auth.decorators import login_required

# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        topwears = Product.objects.filter(category='TW')
        laptop = Product.objects.filter(category='L')
        data = {
            'mobiles': mobiles,
            'topwears': topwears,
            'laptop': laptop
        }
        return render(request, 'app/home.html', context=data)

# def product_detail(request):
#  return render(request, 'app/productdetail.html')


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_inCard = False
        if request.user.is_authenticated:
            item_inCard = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_inCard':item_inCard})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product is not None:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                shipping_amount = 70.0
                total_amount = amount + shipping_amount

        return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'shipping_amount': shipping_amount, 'amount': amount})

@login_required
def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount = 70.0

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount = 70.0

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount = 70.0
        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation !! Profile Updated')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

@login_required
def address(request):
    addre = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addre': addre, 'active': 'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})

# def change_password(request):
#  return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'Sumsing' or data == 'Nokia':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Below':
        mobile = Product.objects.filter(
            category='M').filter(discounted_price__lt=20000)
    elif data == 'Above':
        mobile = Product.objects.filter(
            category='M').filter(discounted_price__gt=20000)
    return render(request, 'app/mobile.html', {'mobile': mobile})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationFrom()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registration Successfull!")
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 0.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            shipping_amount = 70.0
        total_amount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
