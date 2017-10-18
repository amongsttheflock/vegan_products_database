from .models import Shop, Manufacturer, Product, CATEGORIES


def my_cp(request):
    shops = Shop.objects.all()
    manufacturers = Manufacturer.objects.all()
    categories = CATEGORIES
    ctx = {
        'shops': shops,
        'manufacturers': manufacturers,
        'categories': categories
    }
    return ctx
