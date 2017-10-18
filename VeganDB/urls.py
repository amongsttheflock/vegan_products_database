from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from vegandb_app.views import SearchView, ResultsView, signup, ShowProductView, UserDetailView, UserDashView, AddProductView, ModifyProductView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SearchView.as_view(), name='home'),
    url(r'^results/$', ResultsView.as_view(), name='results'),
    url(r'^add_product/$', AddProductView.as_view(), name='add_product'),
    url(r'^modify_product/(?P<pk>(\d)+)$', ModifyProductView.as_view(), name='add_product'),
    url(r'^product_details/(?P<product_id>(\d)+)', ShowProductView.as_view(), name='product_details'),
    url(r'^user_dash/', UserDashView.as_view(), name='user_dash'),
    url(r'^user/(?P<user_id>(\d)+)', UserDetailView.as_view(), name='user_view'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^signup/$', signup, name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
