from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from allauth.account.forms import SignupForm

from savanoriai.core.models import Volunteer

User = get_user_model()


class OrgSignupForm(SignupForm):
    name = forms.CharField(label=_("Pavadinimas"), min_length=3, max_length=255)


class VolunteerSignupForm(SignupForm):
    first_name = User._meta.get_field('first_name').formfield()
    last_name = User._meta.get_field('first_name').formfield()
    city = Volunteer._meta.get_field('city').formfield()
    district = Volunteer._meta.get_field('district').formfield()
    phone = Volunteer._meta.get_field('phone').formfield()
    shift = Volunteer._meta.get_field('shift').formfield()
    experience = Volunteer._meta.get_field('experience').formfield()
