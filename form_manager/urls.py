from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #
    url(r'^(?P<slug>[-\w]+)$', 
        'form_manager.views.form', 
        name="form_manager_form"),

    url(r'^$', 'form_manager.views.index', name="form_manager_index"),
)
