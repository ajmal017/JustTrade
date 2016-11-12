from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'show/$', views.show_tasks, name='show_tasks'),
    url(r'trade/(?P<pk>[0-9]*)/$', views.trade, name='trade'),
    url(r'trade/(?P<pk>[0-9]*)/updateinfo/$',views.present_trading,name = 'update_info'),
]