from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='admin'),
    path('login', views.AdminLoginPage, name='admin_login'),
    path('logout', views.AdminLogoutPage, name='admin_logout'),
    # Category Page
    path('admin_category', views.AdminCategoryPage, name='admin_category'),
    path('remove_category/<int:id>', views.RemoveCategory, name='remove_category'),
    path('edit_category/<int:id>', views.EditCategory, name='edit_category'),
    path('add_category', views.AddCategory, name='add_category'),
    # Add Product Page
    path('admin_product', views.AdminProductPage, name='admin_product'),
    path('remove_product/<int:id>', views.RemoveProduct, name='remove_product'),
    path('edit_product/<int:id>', views.EditProduct, name='edit_product'),
    path('add_product', views.AddProduct, name='add_product'),
    # Check Order
    path('check_order', views.CheckOrdersPage, name='check_order'),
    path('accept_order/<int:id>', views.AcceptOrders, name='accept_order'),
    # User Page
    path('user', views.userPage, name='user'),
    path('delete_user/<int:id>', views.DeleteUser, name='delete_user'),
]
