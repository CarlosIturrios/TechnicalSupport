from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    
    # Auth Urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/ordermanager/login/'}, name='logout'),

    # App views    
   	url(r'^$', views.principal, name='principal'),
   	url(r'^create-Order/(?P<int>[0-9]+)/$', views.createOrder, name='createOrder'),
   	url(r'^request-dashboard/$', views.dashboard, name='dashboard'),
    url(r'^department-dashboard/$', views.department_dashboard, name='department_dashboard'),
    url(r'^request-type-dashboard/$', views.request_type_dashboard, name='request_type_dashboard'),
   	url(r'^order-Pending/$', views.orderPending, name='orderPending'),
   	url(r'^order-Support/(?P<pk>[0-9]+)/$', views.orderSupport, name='orderSupport'),
   	url(r'^poll/(?P<pk>[0-9]+)/$', views.poll, name='poll'),
    url(r'^comment/$', views.comment, name='comment'), 
    url(r'^order-Cancel/(?P<pk>[0-9]+)/$', views.orderCancel, name='orderCancel'),
    url(r'^order-Pause/(?P<pk>[0-9]+)/$', views.orderPause, name='orderPause'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^Create-Maintenance/$', views.CreateMaintenance, name='CreateMaintenance'),
    url(r'^Order-Observations/$', views.OrderObservations, name='OrderObservations'),
    url(r'^order-Show/(?P<pk>[0-9]+)/$', views.orderShow, name='orderShow'),
]