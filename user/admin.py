from django.contrib import admin
from .models import UserId, UserLoggedIn, Category, Products, CartItem, FavoriteItem, OrderItem, Address, UserAmount

admin.site.register(UserId)
admin.site.register(UserLoggedIn)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(CartItem)
admin.site.register(FavoriteItem)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(UserAmount)