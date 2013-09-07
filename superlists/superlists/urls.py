from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
)
