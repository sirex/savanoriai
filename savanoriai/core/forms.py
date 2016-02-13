from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from autocomplete_light import shortcuts as al
from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from allauth.account.utils import filter_users_by_email

from savanoriai.core.models import Volunteer, Organisation, Shift

User = get_user_model()


agreement_text = _(
    "Sutinku, kad mano asmeniniai duomenys būtų naudojami savanorystės „Maisto banke“ tikslais."
)


def validate_profile_email(form, value):
    value = get_adapter().clean_email(value)
    if value and value != form.instance.user.email:
        users = filter_users_by_email(value)
        on_diff_account = [u for u in users if u.pk != form.instance.user.pk]
        if on_diff_account:
            raise forms.ValidationError(_("A user is already registered with this e-mail address."))
        email_address = EmailAddress.objects.add_email(form.request, form.instance.user, value, confirm=True)
        if not email_address.verified:
            raise forms.ValidationError(_(
                "Patikrinkite savo el. paštą ir patvirtinkite šį el. pašto adresą, tada galėsite jį naudoti."
            ))
    return value


class OrganisationBaseForm(forms.Form):
    first_name = User._meta.get_field('first_name').formfield()

    required_css_class = 'field-required'

    class Meta:
        model = Organisation
        autocomplete_fields = ('places',)
        fields = [
            'first_name',
            'email',
            'phone',
            'places',
        ]
        help_texts = {
            'places': _("Mikrorajonai, gyvenvietės arba miestai, kuriuose darysite „Maisto banko“ akcijas."),
        }
        labels = {
            'first_name': _("Pavadinimas"),
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            organisation = kwargs['instance']
            user = organisation.user
            kwargs['initial'] = {
                'first_name': user.first_name,
                'email': user.email,
                'phone': organisation.phone,
                'places': organisation.places.all(),
            }

        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['first_name'].label = _("Pavadinimas")

    def update_profile(self, request, user, organisation):
        cldata = self.cleaned_data

        changed_email = self.instance and cldata['email'] and user.email != cldata['email']

        user.first_name = cldata['first_name']
        user.email = cldata['email']
        user.save()

        organisation.user = user
        organisation.phone = cldata['phone']
        organisation.save()
        organisation.places = cldata['places']

        if changed_email:
            email_address = EmailAddress.objects.add_email(request, user, cldata['email'], confirm=True)
            email_address.set_as_primary()


class OrganisationProfileForm(OrganisationBaseForm, al.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'type': 'email'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_email(self):
        value = self.cleaned_data["email"]
        return validate_profile_email(self, value)


class OrganisationAdminForm(OrganisationBaseForm, al.ModelForm):
    email = forms.EmailField(label=_("El. pašto adresas"), widget=forms.TextInput(attrs={'type': 'email'}))


class OrgSignupForm(SignupForm, OrganisationBaseForm, al.ModelForm):
    agreement = forms.BooleanField(initial=False, label=agreement_text)

    class Meta(OrganisationBaseForm.Meta):
        fields = [
            'first_name',
            'email',
            'password1',
            'password2',
            'phone',
            'places',
            'agreement',
        ]

    def custom_signup(self, request, user):
        organisation = Organisation()
        self.update_profile(request, user, organisation)


class VolunteerBaseForm(forms.Form):
    first_name = User._meta.get_field('first_name').formfield()
    last_name = User._meta.get_field('last_name').formfield()

    required_css_class = 'field-required'

    class Meta:
        model = Volunteer
        autocomplete_fields = ('places',)
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'places',
            'shift',
            'experience',
        ]
        help_texts = {
            'places': _("Mikrorajonai, gyvenvietės arba miestai, kuriuose norėtumėte savanoriauti."),
            'experience': _("Nurodykite, kiek kartų jau esate savanoriavę."),
        }
        widgets = {
            'shift': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            volunteer = kwargs['instance']
            user = volunteer.user
            kwargs['initial'] = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': volunteer.phone,
                'places': volunteer.places.all(),
                'shift': volunteer.shift.all(),
                'experience': volunteer.experience,
            }

        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def update_profile(self, request, user, volunteer):
        cldata = self.cleaned_data

        changed_email = self.instance and cldata['email'] and user.email != cldata['email']

        user.first_name = cldata['first_name']
        user.last_name = cldata['last_name']
        user.email = cldata['email']
        user.save()

        volunteer.user = user
        volunteer.phone = cldata['phone']
        volunteer.experience = cldata['experience']
        volunteer.save()
        volunteer.places = cldata['places']
        volunteer.shift = cldata['shift']

        if changed_email:
            email_address = EmailAddress.objects.add_email(request, user, cldata['email'], confirm=True)
            email_address.set_as_primary()


class VolunteerAdminForm(VolunteerBaseForm, al.ModelForm):
    email = forms.EmailField(label=_("El. pašto adresas"), widget=forms.TextInput(attrs={'type': 'email'}))


class VolunteerProfileForm(VolunteerBaseForm, al.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'type': 'email'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_email(self):
        value = self.cleaned_data["email"]
        return validate_profile_email(self, value)


class VolunteerSignupForm(SignupForm, VolunteerBaseForm, al.ModelForm):
    agreement = forms.BooleanField(initial=False, label=agreement_text)

    class Meta(VolunteerBaseForm.Meta):
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone',
            'places',
            'shift',
            'experience',
        ]

    def custom_signup(self, request, user):
        volunteer = Volunteer()
        self.update_profile(request, user, volunteer)


class VolunteerFilterForm(forms.Form):
    STATE_CHOICES = (
        ('all', _("Visi")),
        ('accepted', _("Priimti")),
        ('available', _("Laisvi")),
        ('invited', _("Pakviesti")),
    )

    places = al.ModelMultipleChoiceField('PlaceAutocomplete', label=_("Vietos"), required=False)
    shifts = forms.ModelMultipleChoiceField(
        label=_("Pamainos"),
        widget=forms.CheckboxSelectMultiple(),
        queryset=Shift.objects.filter(visible=True).order_by('title'),
        required=False,
    )
    state = forms.ChoiceField(choices=STATE_CHOICES, initial='all', required=False, label=_("Būsena"))
