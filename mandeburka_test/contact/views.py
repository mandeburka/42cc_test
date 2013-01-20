from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from mandeburka_test.contact.forms import UserProfileForm


def index(request):
    user = get_object_or_404(User, username='admin')
    return render(request, 'contact/index.html', {'contact_user': user})


@login_required
def edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'contact/edit.html', {'form': form})
