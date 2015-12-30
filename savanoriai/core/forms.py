from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from autocomplete_light import shortcuts as al
from allauth.account.forms import SignupForm

from savanoriai.core.models import Volunteer

User = get_user_model()


class OrgSignupForm(SignupForm):
    name = forms.CharField(label=_("Pavadinimas"), min_length=3, max_length=255)


class VolunteerSignupForm(SignupForm, al.ModelForm):
    first_name = User._meta.get_field('first_name').formfield()
    last_name = User._meta.get_field('first_name').formfield()

    class Meta:
        model = Volunteer
        autocomplete_fields = ('city',)
        fields = [
            'first_name',
            'last_name',
            'city',
            'district',
            'phone',
            'shift',
            'experience',
        ]
