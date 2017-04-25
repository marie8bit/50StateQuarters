from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.coin_collector, name='coin_collector'),
    url(r'^coin/(?P<coin_pk>\d+)$', views.coindetail, name='coindetail'),
    url(r'^statecoin50/fixtures/map.html', views.map_coins, name= 'map_coins')
]
