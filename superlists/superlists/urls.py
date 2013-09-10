from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/(.+)/$','lists.views.view_list',
            name='view_list'
    ),
    url(r'^lists/(.+)/new_item$', 'lists.views.add_item', name='add_item'),
    url(r'^lists/new$', 'lists.views.new_list', name='new_list'),
)
