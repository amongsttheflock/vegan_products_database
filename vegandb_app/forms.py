from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Shop, Manufacturer, Product, CATEGORIES, Messages


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcjonalnie.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcjonalnie.')
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


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


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
        }


class ModifyProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
        }


class AddMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput,
        }
