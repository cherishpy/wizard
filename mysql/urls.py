from django.conf.urls import url
from . import views

urlpatterns = [
  
    url(r'^cluster_list/$', views.cluster_list, name='cluster_list'),
    url(r'^cluster_add/$', views.cluster_add, name='cluster_add'),
    #url(r'^cluster_modify/$', views.cluster_modify, name='cluster_modify'),
    url(r'^cluster_edit/(?P<cluster_name>[a-zA-Z][0-9a-zA-Z\_]*)/$', views.cluster_edit, name='cluster_edit'),
    url(r'^cluster_dele/(?P<cluster_name>[a-zA-Z][0-9a-zA-Z\_]*)/$', views.cluster_dele, name='cluster_dele'),

    url(r'^mysql_list/$', views.mysql_list, name='mysql_list'),
    url(r'^mysqlDetail/(?P<clusterName>.+)/$', views.mysqlDetail, name='mysqlDetail'),
    #url(r'^node_edit/(\d+)/$', views.node_edit, name='node_edit'),
    url(r'^node_info/(\d+)/$', views.node_info, name='node_info'),
    url(r'^node_dele/(\d+)/$', views.node_dele, name='node_dele'),
    url(r'^auto_add_slave/(?P<clusterName>.+)/$', views.auto_add_slave, name='auto_add_slave'),
]

