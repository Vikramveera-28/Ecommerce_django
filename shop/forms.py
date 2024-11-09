from django.contrib.auth.forms import UserCreationForm
from .models import User, Category
from django import forms


class AdminRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter User Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter User Email'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password Again'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Enter Product'}))
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control my-1'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control my-1', 'placeholder': 'Enter Description', 'rows': '5'}))
    status = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input my-1'}))

    class Meta:
        model = Category
        fields = [
            'name',
            'image',
            'description',
            'status'
        ]
        labels = {
            'name': 'Product Name',
            'image': "Product Image",
            'description': "Product Descriptions",
            'status': 'Status'
        }


class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Product'}))
    vender = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Vender Name'}))
    product_image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control my-1'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control my-1', 'placeholder': 'Description', 'rows': '4'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control my-1', 'placeholder': 'Quantity'}))
    original_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control my-1', 'placeholder': 'Original Price'}))
    selling_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control my-1', 'placeholder': 'Selling Price'}))

    class Meta:
        model = Category
        fields = [
            'name',
            'vender',
            'product_image',
            'description',
            'quantity',
            'original_price',
            'selling_price'
        ]
        labels = {
            'name': 'Product Name',
            'vender': "Vender",
            'product_image': "Image",
            'description': "Product Descriptions",
            'quantity': "Quantity",
            'original_price': "Original Price",
            'selling_price': "Selling Price",
        }