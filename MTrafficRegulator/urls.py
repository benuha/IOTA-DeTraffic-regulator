from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path(r'get_traffic_status', views.get_traffic_status, name='get_traffic_status')
]
