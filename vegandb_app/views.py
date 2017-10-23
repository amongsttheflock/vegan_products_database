from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views import View
from django.views.generic import DetailView
from .models import Shop, Product, Manufacturer, CATEGORIES, Messages
from .forms import SignUpForm, ManufacturerForm, ShopForm, AddProductForm, ModifyProductForm, AddMessageForm


class SearchView(View):
    def get(self, request):
        products = Product.objects.order_by('-added')[:6]

        return render(request, "carousel.html", {'products': products, })


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
        category = CATEGORIES[p_details.categories - 1][1]
        return render(request, 'product_details.html', {'p_details': p_details,
                                                        'category': category})


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


class UserMessagesView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_messages.html')


class UserMessagesReceivedView(LoginRequiredMixin, View):

    def get(self, request):
        messages = Messages.objects.filter(recipient=request.user.id).order_by("-sent")
        return render(request, 'user_messages_rec.html', {'messages': messages})


class UserMessagesSentView(LoginRequiredMixin, View):

    def get(self, request):
        messages = Messages.objects.filter(author=request.user.id).order_by("-sent")
        return render(request, 'user_messages_sent.html', {'messages': messages})


class MessageView(LoginRequiredMixin, DetailView):
    model = Messages
    template_name = 'message_details.html'


class CreateMessageView(LoginRequiredMixin, CreateView):
    form_class = AddMessageForm
    template_name = 'create_message.html'
    success_url = reverse_lazy('user_messages')

    def get_initial(self):
        initials = super(CreateMessageView, self).get_initial()
        initials['author'] = self.request.user
        return initials

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AddProductView(LoginRequiredMixin, CreateView):
    form_class = AddProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('user_dash')

    def get_initial(self):
        initials = super(AddProductView, self).get_initial()
        initials['user'] = self.request.user
        return initials

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ModifyProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ModifyProductForm
    template_name = 'modify_product.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

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

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

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

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['product_id'] != '0':
            return reverse('modify_product', kwargs={'pk': self.kwargs['product_id']})
        else:
            return reverse_lazy('add_product')
