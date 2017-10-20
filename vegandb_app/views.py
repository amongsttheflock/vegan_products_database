from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views import View
from django.views.generic import DetailView
from random import randint
from .models import Shop, Product, Manufacturer, CATEGORIES
from .forms import SignUpForm, ManufacturerForm, ShopForm


class SearchView(View):
    def get(self, request):
        # all_ids = Product.objects.values_list('id', flat=True).order_by('-id')
        # product_list = set()
        # while len(product_list) != 6:
        #     for i in all_ids:
        #         product_list.add(Product.objects.get(pk=i))

        # products = list(product_list)

        # ctx = {
        #     'p1': products[0],
        #     'p2': products[1],
        #     'p3': products[2],
        #     'p4': products[3],
        #     'p5': products[4],
        #     'p6': products[5],
        # }
        return render(request, "home.html")


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

        products = Product.objects.filter(**kwargs)
        return render(request, 'results.html', {'products': products,
                                                'request': request})


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
            user = authenticate(username=username,
                                password=raw_password)
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


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'add_product.html'
    success_url = reverse_lazy('user_dash')

    def get_initial(self):
        initials = super(AddProductView, self).get_initial()
        initials['user'] = self.request.user
        return initials


class ModifyProductView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'modify_product.html'

    def get_initial(self):
        initials = super(ModifyProductView, self).get_initial()
        initials['user'] = self.request.user
        return initials

    def get_success_url(self):
        return reverse('product_details', kwargs={'product_id': self.object.id})


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('user_dash')


class AddShopView(LoginRequiredMixin, CreateView):
    form_class = ShopForm
    template_name = 'add_shop.html'

    def get_initial(self):
        initials = super(AddShopView, self).get_initial()
        initials['user'] = self.request.user
        return initials

    def get_success_url(self):
        if self.kwargs['product_id'] != '0':
            return reverse('modify_product', kwargs={'pk': self.kwargs['product_id']})
        else:
            return reverse_lazy('add_product')


class AddManufacturerView(LoginRequiredMixin, CreateView):
    form_class = ManufacturerForm
    template_name = 'add_manufacturer.html'

    def get_initial(self):
        initials = super(AddManufacturerView, self).get_initial()
        initials['user'] = self.request.user
        return initials

    def get_success_url(self):
        if self.kwargs['product_id'] != '0':
            return reverse('modify_product', kwargs={'pk': self.kwargs['product_id']})
        else:
            return reverse_lazy('add_product')
