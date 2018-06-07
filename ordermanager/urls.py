from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    
    # Auth Urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/ordermanager/login/'}, name='logout'),

    # App views    
   	url(r'^$', views.principal, name='principal'),
   	url(r'^createOrder/(?P<int>[0-9]+)/$', views.createOrder, name='createOrder'),
   	url(r'^dashboard/$', views.dashboard, name='dashboard'),
   	url(r'^orderPending/$', views.orderPending, name='orderPending'),
   	url(r'^orderSupport/$', views.orderSupport, name='orderSupport'),
   	url(r'^poll/$', views.poll, name='poll'),
    url(r'^comment/$', views.comment, name='comment'),
]