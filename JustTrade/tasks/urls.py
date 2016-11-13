from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'show/$', views.show_tasks, name='show_tasks'),
    url(r'trade/(?P<pk>[0-9]*)/$', views.task_detail_view, name='trade'),
    url(r'trade/(?P<pk>[0-9]*)/switch/$', views.task_switch_api, name='switch'),
    url(r'trade/(?P<pk>[0-9]*)/updateinfo/$', views.task_log_api, name='task_log'),
    url(r'trade/(?P<pk>[0-9]*)/backtest/$', views.backtest_view, name='back_test')

]