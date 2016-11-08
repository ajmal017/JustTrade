from django.conf.urls import url,include
from django.contrib import admin

from tasks import urls as task_urls
import views

urlpatterns = [
    url(r'^$', views.landing_view),
    url(r'^index/$', views.index_view),

    url(r'^admin/', admin.site.urls),
    url(r'^task/', include(task_urls)),

]
