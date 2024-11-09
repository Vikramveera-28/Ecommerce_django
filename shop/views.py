import os
from django.shortcuts import render, redirect
from .forms import AdminRegistrationForm, CategoryForm, ProductForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, User, Cart, Favorite
import datetime
from django.http import JsonResponse
import json


# Create your views here.

def home(request):
    treading_item = Product.objects.filter(treading=1)
    length = len(treading_item)
    return render(request, "User/Home.html", {'treading_item': treading_item,'length': length })


def admin_home(request):
    category_len = len(Category.objects.all())
    product_len = len(Product.objects.all())
    user_len = len(User.objects.all())
    return render(request, "Admin/Admin.html",
                  {'category_len': category_len, 'product_len': product_len, 'user_len': user_len})


def register(request):
    form = AdminRegistrationForm()
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Register")
            return redirect('/login')
    return render(request, "Admin/Register.html", {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwk = request.POST.get('password')
            user = authenticate(request, username=name, password=pwk)
            if user is not None:
                login(request, user)
                messages.success(request, "LogIn Successfully")
                return redirect('/home')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/login')
        return render(request, "Admin/Login.html")


def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Successfully")
    return redirect('/')


def collection(request):
    information = Category.objects.filter(status=0)
    return render(request, "User/Collection.html", {'information': information})


def collection_view(request, name):
    if Category.objects.filter(name=name):
        vender = []
        for data in Product.objects.filter(category__name=name, status=0):
            vender.append(data.vender)
        vender = set(vender)

        if request.method == 'POST':
            company = request.POST.get('Vender')
            datas = Product.objects.filter(category__name=name, status=0, vender=company)
            return render(request, "User/Collection_View.html", {'collection_datas': datas, 'name': name, 'venders': vender})
        else:
            datas = Product.objects.filter(category__name=name, status=0)
            return render(request, "User/Collection_View.html", {'collection_datas': datas, 'name': name, 'venders': vender})


def product_view(request, cname, pname):
    if Category.objects.filter(name=cname):
        if Product.objects.filter(name=pname):
            product_data = Product.objects.filter(name=pname).first()
            return render(request, "User/Product_View.html", {'product': product_data, 'pname': pname})
        else:
            messages.error(request, "Product Not Fount")
            return redirect('collection')
    else:
        messages.error(request, "Product Not Fount")
        return redirect('collection')


def category(request):
    form = CategoryForm()
    if request.method == 'POST':
        filled_form = CategoryForm(request.POST, request.FILES)
        if filled_form.is_valid():
            Name = request.POST.get('name')
            Image = request.FILES.get('image')
            Description = request.POST.get('description')
            if request.POST.get('status'):
                Status = True
            else:
                Status = False
            Category.objects.create(name=Name, image=Image, description=Description, status=Status).save()

            messages.success(request, "New Category has Created")
        else:
            messages.error(request, "Invalid Details")
    information = Category.objects.all()
    return render(request, "Admin/Category.html", {'form': form, 'information': information})


def product(request):
    category_option = Category.objects.all()
    information = Product.objects.all()
    form = ProductForm()
    if request.method == 'POST':
        filled_form = ProductForm(request.POST, request.FILES)
        if filled_form.is_valid():
            Option = request.POST.get('category')
            Name = request.POST.get('name')
            Vender = request.POST.get('vender')
            Image = request.FILES.get('product_image')
            Description = request.POST.get('description')
            Quantity = request.POST.get('quantity')
            Original = request.POST.get('original_price')
            Selling = request.POST.get('selling_price')

            Category_Option = Category.objects.get(name=Option)
            Created = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")

            Product.objects.create(category=Category_Option, name=Name, vender=Vender, product_image=Image,
                                   description=Description, quantity=Quantity, original_price=Original,
                                   selling_price=Selling, status=False, treading=False, create_at=Created).save()
            messages.success(request, "New Product has Created")
        else:
            print("Invalid")
            messages.error(request, "Invalid Details")
    return render(request, "Admin/Product.html",
                  {'information': information, 'form': form, 'category_option': category_option})


def edit_category(request, id):
    data = Category.objects.get(pk=id)
    if request.method == 'POST':
        Name = request.POST.get('name')
        Image = request.FILES.get('Image')
        Description = request.POST.get('description')

        data.name = Name
        data.image = Image
        data.description = Description
        data.save()
        redirect('/category')

    return render(request, "Admin/Edit_Category.html", {'data': data})


def edit_product(request, id):
    data = Product.objects.get(pk=id)
    if request.method == 'POST':
        Category_Option = request.POST.get('name')
        Name = request.POST.get('name')
        Vender = request.POST.get('vender')
        Image = request.FILES.get('Image')
        Description = request.POST.get('description')
        Quantity = request.POST.get('quantity')
        Original = request.POST.get('original')
        Selling = request.POST.get('selling')

        data.name = Name
        data.vender = Vender
        data.product_image = Image
        data.description = Description
        data.quantity = Quantity
        data.original_price = Original
        data.selling_price = Selling
        data.status = False
        data.treading = False
        data.save()
        return redirect('/product')

    return render(request, "Admin/Edit_Product.html", {'data': data})


def delete_category(request, id):
    data = Category.objects.filter(pk=id)
    data.delete()
    os.remove(data.image.path)
    return redirect('/category')


def delete_product(request, id):
    data = Product.objects.filter(pk=id)
    data.delete()
    return redirect('/product')


def customer_register(request):
    return render(request, "User/Customer_Registration.html")


def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            # print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "User/Cart.html", {'cart': cart})
    else:
        return redirect('admin_home')


def remove_to_cart(request, id):
    cart = Cart.objects.filter(pk=id)
    cart.delete()
    return redirect('cart')


def fav(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favorite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product Already in Favorite'}, status=200)
                else:
                    Favorite.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'Product added to favorite'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Favorite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def favorite_page(request):
    favItem = Favorite.objects.all()
    return render(request, "User/Favorite.html", {'favItem': favItem})


def remove_to_fav(request, id):
    fav = Favorite.objects.filter(pk=id)
    fav.delete()
    return redirect('favorite')
