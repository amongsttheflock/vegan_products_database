from django.shortcuts import render
from django.template.response import TemplateResponse
from django import forms
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView
from random import randint
from .models import Shop, Product, Manufacturer, CATEGORIES
from .forms import SignUpForm, ProductForm


class SearchView(View):
    def get(self, request):
        p_list = [randint(1, len(Product.objects.all())) for i in range(6)]
        ctx = {
            'p1': Product.objects.get(pk=p_list[0]),
            'p2': Product.objects.get(pk=p_list[1]),
            'p3': Product.objects.get(pk=p_list[2]),
            'p4': Product.objects.get(pk=p_list[3]),
            'p5': Product.objects.get(pk=p_list[4]),
            'p6': Product.objects.get(pk=p_list[5]),
        }
        return render(request, "carousel.html", ctx)


class ResultsView(View):

    def get(self, request):
        keyword = request.GET.get('keyword')
        shop_id = request.GET.get('shop')
        cat_id = request.GET.get('category')
        man_id = request.GET.get('manufacturer')
        kwargs = {}

        if keyword != '':
            kwargs['name__icontains'] = keyword
        if shop_id != '0':
            kwargs['shops'] = shop_id
        if cat_id != '0':
            kwargs['categories'] = cat_id
        if man_id != '0':
            kwargs['manufacturer_id'] = man_id
        print(kwargs)
        products = Product.objects.filter(**kwargs)
        return render(request, 'results.html', {'products': products, 'request': request})


class ShowProductView(View):
    def get(self, request, product_id):
        p_details = Product.objects.get(pk=product_id)
        return render(request, 'product_details.html', {'p_details': p_details})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class UserDetailView(View):

    def get(self, request, user_id):
        products = Product.objects.filter(user_id=self.kwargs['user_id']).order_by("-added")
        user = User.objects.get(pk=user_id)
        return render(request, 'user_details.html', {'products': products,
                                                     'user': user})


class UserDashView(LoginRequiredMixin, View):

    def get(self, request):
        products = Product.objects.filter(user_id=request.user.id).order_by("-added")
        return render(request, 'user_dashboard.html', {'products': products})


class AddProductView(CreateView):
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('user_dash')

    def get_initial(self):
        initials = super(AddProductView, self).get_initial()
        initials['user'] = self.request.user
        return initials


class ModifyProductView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'modify_product.html'
    success_url = reverse_lazy('user_dash')
