from django.conf import settings


def django_settings_processor(request):
    return {'settings': settings}
