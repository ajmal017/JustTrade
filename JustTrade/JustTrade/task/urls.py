from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$/tasks',views.show_tasks,name = 'show_tasks'),
]