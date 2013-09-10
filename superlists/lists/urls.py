from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(.+)/$','lists.views.view_list',name='view_list'),
    url(r'^(.+)/new_item$', 'lists.views.add_item', name='add_item'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
)
