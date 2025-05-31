from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import os


def get_file_name(request, file_Name):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    new_file = "%s%s" % (now_time, file_Name)
    return os.path.join('uploads/', new_file)


class UserId(models.Model):
    class Meta:
        app_label = 'user'
    userName = models.CharField(max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.userName


class Address(models.Model):
    user = models.OneToOneField(UserId, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_file_name, null=True, blank=True, default="")
    mobile = models.BigIntegerField(null=False, blank=False)
    town = models.CharField(max_length=50, null=False, blank=False)
    district = models.CharField(max_length=50, null=False, blank=False, default="")
    state = models.CharField(max_length=50, null=False, blank=False)
    pin = models.IntegerField(null=False, blank=False)
    card = models.IntegerField(null=False, blank=False, default=1111, validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    card_pin = models.IntegerField(null=False, blank=False, default=1111, validators=[MinValueValidator(1000), MaxValueValidator(9999)])

    def __str__(self):
        return self.user.userName


class UserLoggedIn(models.Model):
    user = models.ForeignKey(UserId, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.userName


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.FileField(upload_to=get_file_name, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    vender = models.CharField(max_length=50, null=False, blank=False)
    image = models.FileField(upload_to=get_file_name, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    rating = models.IntegerField(null=False, blank=False)
    emi = models.BooleanField(default=False, help_text="0-noEMI, 1-EMI")
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    treading = models.BooleanField(default=False, help_text="0-default, 1-treading")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def discount(self):
        return 100 - ((self.selling_price / self.original_price) * 100)

    def saving_amount(self):
        return self.original_price - self.selling_price


class CartItem(models.Model):
    user = models.ForeignKey(UserId, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def total_price(self):
        return self.quantity * self.product.selling_price

    def total_saving(self):
        return self.quantity * self.product.saving_amount


class OrderItem(models.Model):
    user = models.ForeignKey(UserId, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    delivery = models.BooleanField(default=False, help_text="0-NotDelivery, 1-Delivery")
    payment = models.BooleanField(default=False, help_text="0-NotPaid, 1-Paid")
    price = models.IntegerField(editable=False)

    def __str__(self):
        return f'{self.quantity} item of {self.product.name}'

    def total_amount(self):
        return self.quantity * self.product.original_price

    def total_price(self):
        return self.quantity * self.product.selling_price

    def calculating_price(self):
        return self.quantity * self.product.selling_price

    def price(self, *args, **kwargs):
        self.price = self.calculating_price()
        super().save(*args, **kwargs)

    def total_saving_amount(self):
        return self.quantity * (self.product.original_price - self.product.selling_price)


class FavoriteItem(models.Model):
    user = models.ForeignKey(UserId, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False, help_text='0-False, 1-True')

    def __str__(self):
        return f'{self.favorite} of {self.product.name}'

    def total_discount(self):
        return self.quantity * self.product.saving_amount


class UserAmount(models.Model):
    user = models.OneToOneField(UserId, on_delete=models.CASCADE)
    amount = models.BigIntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f'{self.user.userName} have {self.amount} Amount'
