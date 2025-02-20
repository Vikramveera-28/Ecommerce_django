from django.shortcuts import render, redirect
from .models import AdminId, AdminLoggedIn
from user.models import Category, Products, UserId, OrderItem, CartItem, FavoriteItem, Address
from django.contrib import messages


def adminLoginConfirmation(func):
    def inner(request, *args, **kwargs):
        try:
            logged_admin = AdminLoggedIn.objects.first()
            if logged_admin:
                admin = logged_admin
                return func(request, admin=admin, *args, **kwargs)
            else:
                return redirect('admin_login')
        except Exception as e:
            print(f'Error: {str(e)}')
            return redirect('admin_login')
    return inner


@adminLoginConfirmation
def HomePage(request, admin=None):
    categorys = len(Category.objects.all())
    products = len(Products.objects.all())
    users = len(UserId.objects.all())
    return render(request, "Admin_Pages/Index.html", {'Admin': admin, 'Users': users, 'Categories': categorys, 'Products': products})


@adminLoginConfirmation
def AdminLoginPage(request, admin=None):
    if request.method == "POST":
        UserName = request.POST.get("userName")
        Password = request.POST.get("password")
        try:
            User = AdminId.objects.get(userName=UserName)
            if Password == User.password:
                AdminLoggedIn.objects.get_or_create(user=User)
                messages.success(request, f"Welcome: {UserName}")
                return redirect('/admin')
            else:
                messages.error(request, "Passwords are mismatch")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "Admin_SignIn/Login.html", {'Admin': admin})


@adminLoginConfirmation
def AdminLogoutPage(request, admin=None):
    try:
        admin.delete()
        messages.success(request, f"Successfully {admin} Admin is Logged Out")
        return redirect('admin_login')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")


@adminLoginConfirmation
def AdminCategoryPage(request, admin=None):
    category = Category.objects.all()
    return render(request, "Admin_Pages/Admin_category.html", {'Admin': admin, 'Category': category})


@adminLoginConfirmation
def RemoveCategory(request, id, admin=None):
    try:
        category = Category.objects.get(pk=id)
        category.delete()
        messages.success(request, f"Successfully {category.name} is deleted")
        return redirect('admin_category')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")


@adminLoginConfirmation
def EditCategory(request, id, admin=None):
    category = Category.objects.get(pk=id)
    if request.method == "POST":
        Name = request.POST.get('name')
        Image = request.FILES.get('image')
        Description = request.POST.get('description')
        Status = request.POST.get('status')
        try:
            category.name = Name
            category.descriptions = Description
            category.status = Status
            if Image:
                category.image = Image
            else:
                category.image = category.image
            category.save()
            messages.success(request, f"Successfully {Name} is Edited")
            return redirect(f'/admin/edit_category/{id}')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "Admin_Pages/Edit_category.html", {'Category': category, 'Admin': admin})


@adminLoginConfirmation
def AdminProductPage(request, admin=None):
    products = Products.objects.all()
    if request.method == "POST":
        category = request.POST.get('category')
        if category == "All":
            products = Products.objects.all()
        else:
            products = Products.objects.filter(category__name=category)
        return render(request, "Admin_Pages/Admin_product.html", {'Admin': admin, 'Products': products})
    return render(request, "Admin_Pages/Admin_product.html", {'Admin': admin, 'Products': products})


@adminLoginConfirmation
def RemoveProduct(request, id, admin=None):
    try:
        product = Products.objects.get(pk=id)
        product.delete()
        messages.success(request, f"Successfully {product.name} is Deleted")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('admin_product')


@adminLoginConfirmation
def EditProduct(request, id, admin=None):
    product = Products.objects.get(pk=id)
    if request.method == 'POST':
        Name = request.POST.get('name')
        Vender = request.POST.get('vender')
        Image = request.FILES.get('image')
        Description = request.POST.get('description')
        Quantity = request.POST.get('quantity')
        EMI = request.POST.get('emi')
        OriginalPrice = request.POST.get('originalPrice')
        SellingPrice = request.POST.get('sellingPrice')
        Status = request.POST.get('status')
        Treading = request.POST.get('treading')

        try:
            product.name = Name
            product.vender = Vender
            if Image:
                product.image = Image
            else:
                product.image = product.image
            product.descriptions = Description
            product.quantity = Quantity
            product.emi = EMI
            product.original_price = OriginalPrice
            product.selling_price = SellingPrice
            product.status = Status
            product.treading = Treading
            product.save()
            messages.success(request, f"Successfully {Name} is Edited")
            return redirect(f'/admin/edit_product/{id}')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "Admin_Pages/Edit_product.html", {'Admin': admin, 'Product': product})


@adminLoginConfirmation
def CheckOrdersPage(request, admin=None):
    orders = OrderItem.objects.filter(delivery=False)
    if request.method == "POST":
        User = request.POST.get("user")
        Payment = request.POST.get("payment")
        orders = OrderItem.objects.filter(user__userName=User, payment=Payment, delivery=False)
    users = []
    for order in orders:
        users.append(order.user.userName)
    Users = set(users)
    return render(request, "Admin_Pages/Orders_check.html", {'Admin': admin, 'Orders': orders, 'Users': Users})


@adminLoginConfirmation
def AcceptOrders(request, id, admin=None):
    order = OrderItem.objects.get(pk=id)
    if order.payment:
        order.delivery = True
        order.save()
        messages.success(request, "That item is successfully delivery")
    else:
        messages.error(request, "That user not finished the payment")
    return redirect('check_order')


@adminLoginConfirmation
def AddCategory(request, admin=None):
    if request.method == "POST":
        Name = request.POST.get("name")
        Image = request.FILES.get("image")
        Description = request.POST.get("descriptions")
        Status = request.POST.get("status")

        try:
            Category.objects.get_or_create(
                name=Name,
                image=Image,
                descriptions=Description,
                status=Status
            )
            messages.success(request, "Successfully Category Added")
            return redirect('admin_category')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "Admin_Pages/Add_category.html", {'Admin': admin})


@adminLoginConfirmation
def AddProduct(request, admin=None):
    categorys = Category.objects.all()
    if request.method == "POST":
        Ctgy = request.POST.get('category')
        Category_name = Category.objects.get(name=Ctgy)
        Name = request.POST.get('name')
        Vender = request.POST.get('vender')
        Image = request.FILES.get('image')
        Quantity = request.POST.get('quantity')
        Rating = request.POST.get('rating')
        Descriptions = request.POST.get('descriptions')
        OriginalPrice = request.POST.get('originalPrice')
        SellingPrice = request.POST.get('sellingPrice')
        Emi = request.POST.get('emi')
        Status = request.POST.get('status')
        Treading = request.POST.get('treading')

        try:
            Products.objects.get_or_create(
                category=Category_name,
                name=Name,
                vender=Vender,
                image=Image,
                descriptions=Descriptions,
                quantity=Quantity,
                rating=Rating,
                emi=Emi,
                original_price=OriginalPrice,
                selling_price=SellingPrice,
                status=Status,
                treading=Treading
            )
            messages.success(request, "Successfully Product Added")
            return redirect('admin_product')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "Admin_Pages/Add_product.html", {'Admin': admin, 'Category': categorys})


@adminLoginConfirmation
def userPage(request, admin=None):
    details = Address.objects.all()
    return render(request, "Admin_Pages/Users.html", {'Admin': admin, 'Details': details})


@adminLoginConfirmation
def DeleteUser(request, id, admin=None):
    try:
        address = Address.objects.get(pk=id)
        address.user.delete()
        messages.success(request, f"Successfully user( {address.user} ) is deleted")
        return redirect('user')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
