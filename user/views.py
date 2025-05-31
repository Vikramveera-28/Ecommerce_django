from django.shortcuts import render, redirect
from .models import UserId, UserLoggedIn, Category, Products, CartItem, FavoriteItem, OrderItem, Address, UserAmount
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import get_object_or_404

# ------------------------------ Functions ------------------------------
def login_confirmation(func):
    def inner(request, *args, **kwargs):
        try:
            user_logged_in = UserLoggedIn.objects.first()
            if user_logged_in:
                user = user_logged_in
                return func(request, user=user, *args, **kwargs)
            else:
                messages.error(request, "User Not Fount")
                return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('login')
    return inner


def logout_confirmation(func):
    def inner(request):
        try:
            user_logged_in = UserLoggedIn.objects.first()
            if not user_logged_in:
                return func(request)
            else:
                return redirect('home')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return inner


def get_spending_money():
    logged_user = UserLoggedIn.objects.first()
    User = UserId.objects.get(userName=logged_user)
    List = OrderItem.objects.filter(user=User, payment=True)
    money = 0
    for mny in List:
        money += (mny.quantity * mny.product.selling_price)
    return money


# ------------------------------ LogIn ------------------------------
@logout_confirmation
def LoginPage(request):
    if request.method == "POST":
        UserName = request.POST.get('userName')
        Password = request.POST.get('password')
        try:
            User = UserId.objects.get(userName=UserName)
            if check_password(Password, User.password):
                UserLoggedIn.objects.get_or_create(user=User)
                messages.success(request, f"Welcome: {User.userName}")
                return redirect('home')
            else:
                messages.error(request, f"Passwords are mismatch")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "SignIn/Login.html")


# ------------------------------ Logout ------------------------------
@login_confirmation
def LogoutPage(request, user=None):
    try:
        user.delete()
        messages.success(request, f"Successfully {user} is logged out")
        return redirect('login')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")


# ------------------------------ Register ------------------------------
@logout_confirmation
def RegisterPage(request):
    Required = None
    if request.method == "POST":
        try:
            Name = request.POST.get('userName')
            Email = request.POST.get('email')
            Password1 = request.POST.get('password1')
            Password2 = request.POST.get('password2')
            if Password1 == Password2:
                UserId.objects.create(
                    userName=Name,
                    password=make_password(Password1),
                    email=Email
                )
                messages.success(request, f"Successfully new user {Name} is created")
                return redirect('login')
            else:
                messages.error(request, "Passwords are mismatch")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "SignIn/Register.html", {'Required': Required})


# ------------------------------ Home Page ------------------------------
def IndexPage(request):
    return render(request, "Index.html")


@login_confirmation
def homePage(request, user=None):
    products = Products.objects.filter(treading=1)
    return render(request, "Pages/Home.html", {'User': user, 'Products': products})


# ------------------------------ Products Pages ------------------------------
@login_confirmation
def CategoryPage(request, user=None):
    category = Category.objects.filter(status=0)
    return render(request, "Pages/Products/Category.html", {'User': user, 'Category': category})


@login_confirmation
def ProductPage(request, cname, user=None):
    products = Products.objects.filter(category__name=cname, status=0)
    return render(request, "Pages/Products/Products.html", {'Products': products, 'Name': cname, 'User': user})


@login_confirmation
def ProductViewPage(request, cname, pname, user=None):
    if Category.objects.filter(name=cname):
        if Products.objects.filter(name=pname):
            Product = Products.objects.get(name=pname)
            relative = Products.objects.filter(vender=Product.vender)
            return render(request, "Pages/Products/Product_details.html",
                          {'Product': Product, 'Relative': relative, 'User': user})
        else:
            messages.error(request, "Product Not Fount")
            redirect('category')
    else:
        messages.error(request, f"Category Not Fount")
        redirect('category')


# ------------------------------ Cart ------------------------------
@login_confirmation
def CartPage(request, user=None):
    User = UserId.objects.get(userName=user)
    cart = CartItem.objects.filter(user=User)
    return render(request, "Pages/Lists/Cart.html", {'Carts': cart, 'User': user})


@login_confirmation
def AddCart(request, cname, pname, user=None):
    if Category.objects.filter(name=cname):
        if Products.objects.filter(name=pname):
            Product = Products.objects.get(name=pname)
            User = UserId.objects.get(userName=user)
            quantity = request.GET.get('quantity', 1)
            if CartItem.objects.filter(product=Product, user=User).exists():
                messages.error(request, "Product already added to cart")
                return redirect(f'/product_view/{cname}/{pname}')
            else:
                CartItem.objects.create(
                    user=User,
                    product=Product,
                    quantity=quantity
                )
                messages.success(request, "Successfully added item to cart")
                return redirect(f'/product_view/{cname}/{pname}')
        else:
            messages.error(request, "Product Not Fount")
            return redirect(f'/product_view/{cname}/{pname}')
    else:
        messages.error(request, f"Category Not Fount")
        return redirect(f'/product_view/{cname}/{pname}')


@login_confirmation
def RemoveCart(request, id, user=None):
    try:
        cart = CartItem.objects.get(pk=id)
        cart.delete()
        messages.success(request, f"Successfully card item ( {cart.product.name} ) is removed")
        return redirect('cart')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")


# ------------------------------ Favorite ------------------------------
@login_confirmation
def FavoritePage(request, user=None):
    User = UserId.objects.get(userName=user)
    favorite = FavoriteItem.objects.filter(user=User, favorite=True)
    return render(request, "Pages/Lists/Favorite.html", {'Favorites': favorite, 'User': user})


@login_confirmation
def AddFav(request, cname, pname, user=None):
    if Category.objects.filter(name=cname):
        if Products.objects.filter(name=pname):
            Product = Products.objects.filter(name=pname).first()
            User = UserId.objects.get(userName=user)
            favorite = request.GET.get('quantity', 1)
            if favorite:
                fav = FavoriteItem.objects.get_or_create(product=Product, user=User)
                fav[0].product = Product
                fav[0].user = User
                if fav[0].favorite:
                    fav[0].favorite = False
                    messages.error(request, f"Successfully item removed to favorite")
                    fav[0].save()
                else:
                    fav[0].favorite = True
                    fav[0].save()
                    messages.success(request, f"Successfully item added to favorite")
            return redirect(f'/product_view/{cname}/{pname}')
        else:
            messages.error(request, "Product Not Fount")
            return redirect(f'/product_view/{cname}/{pname}')
    else:
        messages.error(request, "Category Not Fount")
        return redirect(f'/product_view/{cname}/{pname}')


@login_confirmation
def RemoveFav(request, id, user=None):
    try:
        favorite = FavoriteItem.objects.get(pk=id)
        favorite.delete()
        messages.success(request, f"Successfully favorite item ( {favorite.product.name} ) is deleted")
        return redirect('favorite')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")


# ------------------------------ Order ------------------------------
@login_confirmation
def OrderPage(request, user=None):
    User = UserId.objects.get(userName=user)
    order = OrderItem.objects.filter(user=User, payment=False)
    return render(request, "Pages/Lists/Order.html", {'User': user, 'Orders': order})


@login_confirmation
def AddOrder(request, cname, pname, user=None):
    if Category.objects.filter(name=cname):
        if Products.objects.filter(name=pname):
            Product = Products.objects.get(category__name=cname, name=pname)
            User = UserId.objects.get(userName=user)
            qty = int(request.GET.get('quantity', 1))
            if qty > 0:
                OrderItem.objects.get_or_create(
                    user=User,
                    product=Product,
                    quantity=qty,
                    delivery=False
                )
                messages.success(request, f"Successfully {Product.name} is added to order list")
            else:
                messages.error(request, f"Invalid quantity value")
            return redirect(f'/product_view/{cname}/{pname}')
    else:
        messages.error(request, f"Category not fount")
        return redirect(f'/product_view/{cname}/{pname}')


@login_confirmation
def RemoveOrder(request, id, user=None):
    try:
        order = OrderItem.objects.get(pk=id)
        order.delete()
        messages.success(request, f"Successfully order item ( {order.product.name} ) is deleted")
        return redirect('order')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")


@login_confirmation
def OrderDetailsPage(request, id, user=None):
    ordered_item = OrderItem.objects.get(pk=id)
    return render(request, "Pages/Lists/Order_details.html", {'User': user, 'Ordered': ordered_item})


# ------------------------------ Payment ------------------------------
@login_confirmation
def PaymentPage(request, id, user=None):
    User = UserId.objects.get(userName=user)
    product = OrderItem.objects.get(pk=id)
    address = Address.objects.get(user=User)
    amount = UserAmount.objects.get(user=User)
    if request.method == 'POST':
        Order = OrderItem.objects.get(pk=id)
        card_number = int(request.POST.get('cardNo'))
        pin_number = int(request.POST.get('pinNo'))
        if card_number == address.card and pin_number == address.card_pin:
            total_Price = Order.quantity * Order.product.selling_price
            if total_Price < amount.amount:
                # Edit and save the Amount
                Price = amount.amount - total_Price
                amount.user = amount.user
                amount.amount = Price
                amount.save()

                # Edit and save the Order
                Order.user = Order.user
                Order.product = Order.product
                Order.quantity = Order.quantity
                Order.payment = True
                Order.save()
                messages.success(request, f"Successfully Paid to item {Order.product.name}")
                return redirect(f'/delivery/{id}')
            else:
                messages.error(request, f"Your Money Not enough to payment the this item")
        else:
            messages.error(request, f"Invalid card and pin number")
            return redirect(f'/payment/{id}')
    return render(request, "Pages/Products/Payment.html",
                  {'Product': product, 'User': user, 'Address': address, 'Amount': amount})


# ------------------------------ Profile ------------------------------
@login_confirmation
def ProfilePage(request, user=None):
    User = UserId.objects.get(userName=user)
    profile = get_object_or_404(Address, user=User)
    Amount = UserAmount.objects.get(user=User)
    Spand_amount = get_spending_money()
    return render(request, "Pages/Profile/Profile.html",
                  {'Profile': profile, 'User': user, 'Amount': Amount, 'Spand_amount': Spand_amount})


@login_confirmation
def EditProfilePage(request, id, user=None):
    Profile = Address.objects.get(pk=id)
    if request.method == "POST":
        Image = request.FILES.get("image")
        Mobile = request.POST.get("mobile")
        Town = request.POST.get("town")
        District = request.POST.get("district")
        State = request.POST.get("state")
        Pin = request.POST.get("pin")
        CardNo = request.POST.get("cardNo")
        PinNo = request.POST.get("pinNo")

        try:
            if Image:
                Profile.image = Image
            else:
                Profile.image = Profile.image
            Profile.mobile = Mobile
            Profile.town = Town
            Profile.district = District
            Profile.state = State
            Profile.pin = Pin
            Profile.card = CardNo
            Profile.card_Pin = PinNo
            Profile.save()
            messages.success(request, f"Successfully Your profile is edited")
            return redirect(f'/edit_profile/{id}')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "Pages/Profile/Edit_profile.html", {'Profile': Profile, 'User': user})


@login_confirmation
def EditAmount(request, id, user=None):
    try:
        User_amount = UserAmount.objects.get(pk=id)
        Amount = int(User_amount.amount + 5000)
        User_amount.user = User_amount.user
        User_amount.amount = Amount
        User_amount.save()
        messages.success(request, f"Successfully Your amount increase by Rs.5000/-")
        return redirect('profile')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")


# ------------------------------ Delivery ------------------------------
@login_confirmation
def DeliveryPage(request, id, user=None):
    User = UserId.objects.get(userName=user)
    delivery = OrderItem.objects.get(pk=id, user=User, payment=True)
    deliveries = OrderItem.objects.filter(user=User, payment=True)
    return render(request, "Pages/Lists/Delivery.html",
                  {'User': user, 'Delivery': delivery, 'Deliveries': deliveries})


@login_confirmation
def Delivery(request, user=None):
    User = UserId.objects.get(userName=user)
    deliveries = OrderItem.objects.filter(user=User, payment=True)
    return render(request, "Pages/Lists/Delivery.html", {'User': user, 'Deliveries': deliveries})
