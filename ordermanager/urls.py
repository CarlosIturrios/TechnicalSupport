from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    
    # Auth Urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/ordermanager/login/'}, name='logout'),

    # App views    
   	url(r'^$', views.principal, name='principal'),
   	url(r'^$', views.createOrder, name='createOrder'),
   	url(r'^$', views.dashboard, name='dashboard'),
   	url(r'^$', views.orderPending, name='orderPending'),
   	url(r'^$', views.orderSupport, name='orderSupport'),
   	url(r'^$', views.poll, name='poll'),
]