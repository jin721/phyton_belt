from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^reg_user$', views.reg_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add),
    url(r'^travels/add_trip$', views.add_trip),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^travels/destination/join/(?P<id>\d+)$', views.join_trip)
]
