from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'mandeburka_test.views.home', name='home'),
    url(r'^$', 'mandeburka_test.contact.views.index', name='index')
)
