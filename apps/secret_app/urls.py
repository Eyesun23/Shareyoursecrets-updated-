from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^popular$', views.popular),
    url(r'^recent$', views.recent),
    url(r'^users/register$', views.register),
    url(r'^user/comments$', views.comment),
    url(r'^like/(?P<comment_id>\d+)', views.like),
    url(r'^unlike/(?P<comment_id>\d+)', views.like),
    url(r'^delete/(?P<comment_id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]
