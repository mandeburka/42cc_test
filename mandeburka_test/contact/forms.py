from django import forms
from mandeburka_test.contact.models import UserProfile
from django.forms.widgets import FileInput


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'date_of_birth',
            'photo',
            'email',
            'jabber',
            'skype',
            'other_contacts',
            'bio'
        )
        widgets = {
            'photo': FileInput,
        }
