from django.conf.urls import patterns, url
from django.views.generic import ListView
from mandeburka_test.contact.models import Request

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'mandeburka_test.views.home', name='home'),
    url(r'^$', 'mandeburka_test.contact.views.index', name='index'),
    url(r'^requests$', ListView.as_view(
        queryset=Request.objects.all()[:10],
        context_object_name='requests',
        template_name='contact/requests.html'
        ), name='requests'),
    url(r'^edit', 'mandeburka_test.contact.views.edit', name='edit'),
    url(r'ajax-upload$',
        'mandeburka_test.contact.views.import_uploader',
        name="my_ajax_upload"),
)
