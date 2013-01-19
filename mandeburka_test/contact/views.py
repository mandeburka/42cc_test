# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


def index(request):
    user = get_object_or_404(User, username='admin')
    return render(request, 'contact/index.html', {'user': user})
