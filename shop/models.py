import os.path
from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
def get_File_Name(request, file_Name):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_file = "%s%s" % (now_time, file_Name)
    return os.path.join('uploads/', new_file)


class Category(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    image = models.FileField(upload_to=get_File_Name, null=True, blank=True)
    description = models.CharField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False, blank=False)
    vender = models.CharField(max_length=30, null=False, blank=False)
    product_image = models.FileField(upload_to=get_File_Name, null=True, blank=True)
    description = models.CharField(max_length=500, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    treading = models.BooleanField(default=False, help_text="0-default, 1-treading")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def discount(self):
        return 100 - ((self.selling_price / self.original_price) * 100)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_qty * self.product.selling_price


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
