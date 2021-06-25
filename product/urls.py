# from django.conf.urls.static import static
from django.urls import path
from .views import *



app_name='product'
urlpatterns = [
    path('', home, name='home'),
    path('shop/', product_in_category, name='product_all'),
    path('shop/<slug:category_slug>/', product_in_category, name="product_in_category"),
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'),
    path('reply_write', reply_write, name='reply_write')
] 

