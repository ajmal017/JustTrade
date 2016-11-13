from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'show/$', views.show_tasks, name='show_tasks'),
    url(r'trade/(?P<pk>[0-9]*)/$', views.task_detail_view, name='trade'),
    url(r'trade/(?P<pk>[0-9]*)/quotes/$', views.task_quotes_api, name='quotes'),
    url(r'trade/(?P<pk>[0-9]*)/switch/$', views.task_switch_api, name='switch'),
    url(r'trade/(?P<pk>[0-9]*)/updateinfo/$', views.task_log_api, name='task_log'),
    url(r'trade/(?P<pk>[0-9]*)/backtest/$', views.backtest_view, name='back_test'),
    url(r'trade/(?P<pk>[0-9]*)/backtestapi/$', views.backtest_api, name='back_test_api'),
    url(r'trade/(?P<pk>[0-9]*)/ibm/$', views.IBM_trade_view, name='IBM_trade_view')

]