from django import forms
from mandeburka_test.contact.models import UserProfile
from django.forms.widgets import HiddenInput
from django.forms.fields import CharField
from mandeburka_test.contact.widgets import ContactDateInput


class UserProfileForm(forms.ModelForm):
    photo = CharField(widget=HiddenInput, required=False)

    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'jabber',
            'skype',
            'other_contacts',
            'bio',
            'photo'
        )
        widgets = {'date_of_birth': ContactDateInput}
