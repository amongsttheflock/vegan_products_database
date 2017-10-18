from django.contrib import admin
from .models import Shop, Product, Manufacturer


class ProductInlineAdmin(admin.TabularInline):
    model = Product.shops.through


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'shop_products')
    inlines = (ProductInlineAdmin,)

    def shop_products(self, obj):
        return ",  ".join([str(product.name) for product in obj.products.all()])


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'description', 'product_shops', 'photo', 'ingredients', 'user', 'added',)
    inlines = (ProductInlineAdmin,)

    def manufacturer(self, obj):
        return obj.manufacturer.name

    def product_shops(self, obj):
        return ",  ".join([str(shop.name) for shop in obj.shops.all()])


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)


admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
