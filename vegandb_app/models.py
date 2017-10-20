from django.db import models
from django.contrib.auth.models import User


CATEGORIES = (
    (1, "Dania gotowe"),
    (2, "Słodkie"),
    (3, "Mrożonki"),
    (4, "Na kanapki"),
    (5, "Wegański Nabiał"),
)


class Shop(models.Model):
    name = models.CharField(max_length=140, verbose_name='Nazwa')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=140, verbose_name='Nazwa')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=140, verbose_name='Nazwa')
    description = models.TextField(verbose_name='Opis')
    added = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='media/', null=False, verbose_name='Zdjęcie produktu')
    ingredients = models.ImageField(upload_to='media/', null=False, verbose_name='Skład')
    categories = models.IntegerField(choices=CATEGORIES, verbose_name='Kategorie')
    shops = models.ManyToManyField(Shop, related_name='products', verbose_name='Sklepy')
    manufacturer = models.ForeignKey(Manufacturer, default=1, related_name='manufacturer', verbose_name='Producent')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name
