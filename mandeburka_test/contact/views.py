# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


def index(request):
    user = get_object_or_404(User, username='admin')
    return render(request, 'contact/index.html', {'contact_user': user})


@login_required
def edit(request):
    return render(request, 'contact/edit.html')
