"""DJangoEx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from member import views

urlpatterns = [
    path( "register", views.register, name="register" ),
    path( "checkid", views.checkid, name="checkid"),
    path( "checkemail", views.checkemail, name="checkemail"),
    path( "login", views.login, name="login" ),
    path( "profile", views.profile, name="profile" ),
    path( "logout", views.logout, name="logout" ),
    path( "delete", views.delete, name="delete" ),
    path( "modify", views.modify, name="modify" ),
    path( "modifypro", views.modifypro, name="modifypro" ),
    path( "orderdetail", views.order_detail, name="orderdetail" ),
    path( "orderitem", views.orderitem, name="orderitem" ),
    path( "review_write", views.review_write, name="review_write"),
    path( "review_write_pro", views.review_write_pro, name="review_write_pro"),
    path( "review_modify", views.review_modify, name="review_modify"),
    path( "review_modify_pro", views.review_modify_pro, name="review_modify_pro"),
    path('^activate/(?P<uid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]

















