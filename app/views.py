from unicodedata import category
from django.shortcuts import render
from django.views import View
from .models import Cart, Product, OrderPlaced, Customer
import json
from django.contrib import messages
from .forms import CustomerProfileForm, CustomerRegistrationFrom, UserCreationForm

# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        topwears = Product.objects.filter(category='TW')
        laptop = Product.objects.filter(category='L')
        data = {
            'mobiles':mobiles,
            'topwears':topwears,
            'laptop':laptop
        }
        return render(request, 'app/home.html', context=data)

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product})

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user, product=product).save()
    return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation !! Profile Updated')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


def address(request):
    addre = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', {'addre':addre, 'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'Sumsing' or data == 'Nokia':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Below':
        mobile = Product.objects.filter(category='M').filter(discounted_price__lt=20000)
    elif data == 'Above':
        mobile = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
    return render(request, 'app/mobile.html', {'mobile':mobile})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationFrom()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registration Successfull!")
        return render(request, 'app/customerregistration.html', {'form':form})

def checkout(request):
 return render(request, 'app/checkout.html')
