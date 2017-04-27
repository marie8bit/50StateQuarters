from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^user/(?P<user_pk>\d+)$', views.coin_collector, name='coin_collector'),
    url(r'^coin/(?P<coin_pk>\d+)$', views.coindetail, name='coindetail'),

]
