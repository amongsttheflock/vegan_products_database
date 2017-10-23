from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from vegandb_app.views import SearchView, ResultsView, signup, ShowProductView, UserDetailView, UserDashView, AddProductView, ModifyProductView, AddShopView, AddManufacturerView, DeleteProductView, UserMessagesView, UserMessagesReceivedView, UserMessagesSentView, MessageView, CreateMessageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SearchView.as_view(), name='home'),
    url(r'^results/$', ResultsView.as_view(), name='results'),
    url(r'^add_product/$', AddProductView.as_view(), name='add_product'),
    url(r'^add_shop/(?P<product_id>(\d)+)$', AddShopView.as_view(), name='add_shop'),
    url(r'^add_manufacturer/(?P<product_id>(\d)+)$', AddManufacturerView.as_view(), name='add_manufacturer'),
    url(r'^modify_product/(?P<pk>(\d)+)$', ModifyProductView.as_view(), name='modify_product'),
    url(r'^delete_product/(?P<pk>(\d)+)$', DeleteProductView.as_view(), name='delete_product'),
    url(r'^product_details/(?P<product_id>(\d)+)$', ShowProductView.as_view(), name='product_details'),
    url(r'^user_dash/$', UserDashView.as_view(), name='user_dash'),
    url(r'^user/(?P<user_id>(\d)+)$', UserDetailView.as_view(), name='user_view'),
    url(r'^user_messages/$', UserMessagesView.as_view(), name='user_messages'),
    url(r'^user_messages_rec/$', UserMessagesReceivedView.as_view(), name='user_messages_rec'),
    url(r'^user_messages_sent/$', UserMessagesSentView.as_view(), name='user_messages_sent'),
    url(r'^create_message/$', CreateMessageView.as_view(), name='create_message'),
    url(r'^message_details/(?P<pk>(\d)+)$', MessageView.as_view(), name='message_details'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^signup/$', signup, name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
