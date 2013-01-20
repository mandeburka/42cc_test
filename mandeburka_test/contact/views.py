from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from mandeburka_test.contact.forms import UserProfileForm
import json
from django.http import HttpResponse
from django.middleware.csrf import get_token
from ajaxuploader.views import AjaxFileUploader


def index(request):
    user = get_object_or_404(User, username='admin')
    return render(request, 'contact/index.html', {'contact_user': user})


@login_required
def edit(request):
    response_data = {}
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES,
            instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            saved = True
        else:
            response_data['errors'] = form.errors
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    if request.is_ajax():
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
    return render(request, 'contact/edit.html', {'form': form})


def start(request):
    csrf_token = get_token(request)
    return render(
        request,
        'import.html',
        {'csrf_token': csrf_token})


import_uploader = AjaxFileUploader()
