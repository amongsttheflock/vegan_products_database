from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Shop, Manufacturer, Product, CATEGORIES


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcjonalnie.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcjonalnie.')
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['photo'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['ingredients'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['categories'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['shops'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['manufacturer'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
        }


class ShopForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Shop
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
        }


class ManufacturerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ManufacturerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Manufacturer
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
        }
