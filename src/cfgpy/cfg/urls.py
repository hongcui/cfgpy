from django.views.generic import DetailView, ListView, FormView
from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from models import DatasetXml

admin.autodiscover()

urlpatterns = patterns('cfg.views',
    # Examples:
    url(r'^$',
        ListView.as_view(
                         queryset=DatasetXml.objects.order_by('-name'),
                         context_object_name = 'dataset_list',
                         template_name='cfg/index.html')),
    url(r'^(?P<dataset_id>\w+)/$', 'species'),
    url(r'^(\w+)/compute/$', 'compute'),
    url(r'^(\w+)/compute/split/$', 'split_species')
)
