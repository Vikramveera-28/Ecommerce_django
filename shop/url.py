from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('home', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('collection', views.collection, name='collection'),
    path('collection_view/<str:name>', views.collection_view, name='collection_view'),
    path('product_view/<str:cname>/<str:pname>', views.product_view, name='product_view'),
    path('category', views.category, name='category'),
    path('product', views.product, name='product'),
    path('edit_category/<int:id>', views.edit_category, name='edit_category'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('addtocart', views.add_to_cart, name='addtocart'),
    path('removetocart/<int:id>', views.remove_to_cart, name='removetocart'),
    path('cart', views.cart, name='cart'),
    path('fav', views.fav, name='fav'),
    path('favorite', views.favorite_page, name='favorite'),
    path('removetofav/<int:id>', views.remove_to_fav, name='removetofav'),
]

