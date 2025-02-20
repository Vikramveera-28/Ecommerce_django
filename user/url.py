from django.urls import path
from . import views

urlpatterns = [
    # Index page
    path('', views.IndexPage, name='index'),
    # logged user's home page
    path('home', views.homePage, name='home'),
    # Sign Page
    path('login', views.LoginPage, name='login'),
    path('logout', views.LogoutPage, name='logout'),
    path('register', views.RegisterPage, name='register'),
    # Category and product page
    path('category', views.CategoryPage, name='category'),
    path('product/<str:cname>', views.ProductPage, name='product'),
    path('product_view/<str:cname>/<str:pname>', views.ProductViewPage, name='product_view'),
    # Cart Page
    path('cart', views.CartPage, name='cart'),
    path('addCart/<str:cname>/<str:pname>', views.AddCart, name='add_to_cart'),
    path('remove_cart/<int:id>', views.RemoveCart, name='remove_cart'),
    # Favorite Page
    path('favorite', views.FavoritePage, name='favorite'),
    path('addFav/<str:cname>/<str:pname>', views.AddFav, name='add_fav'),
    path('remove_fav/<int:id>', views.RemoveFav, name='remove_fav'),
    # Payment Page
    path('payment/<int:id>', views.PaymentPage, name='payment'),
    # Order Page
    path('order', views.OrderPage, name='order'),
    path('addOrder/<str:cname>/<str:pname>', views.AddOrder, name='add_order'),
    path('remove_order/<int:id>', views.RemoveOrder, name='remove_order'),
    path('order_details/<int:id>', views.OrderDetailsPage, name='order_details'),
    # Profile Page
    path('profile', views.ProfilePage, name='profile'),
    path('edit_profile/<int:id>', views.EditProfilePage, name='edit_profile'),
    path('add_amount/<int:id>', views.EditAmount, name='add_amount'),
    # Delivery Page
    path('delivery', views.Delivery, name='delivery'),
    path('delivery/<int:id>', views.DeliveryPage, name='delivery'),
]