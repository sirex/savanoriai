from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from autocomplete_light import shortcuts as al
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from allauth.account.utils import filter_users_by_email

from savanoriai.core.models import Volunteer, Organisation

User = get_user_model()


agreement_text = _(
    "Sutinku, kad mano asmeniniai duomenys būtų naudojami savanorystės „Maisto banke“ tikslais."
)


class OrgSignupForm(SignupForm, al.ModelForm):
    first_name = User._meta.get_field('first_name').formfield()
    agreement = forms.BooleanField(initial=False, label=agreement_text)

    class Meta:
        model = Organisation
        autocomplete_fields = ('places',)
        fields = [
            'first_name',
            'email',
            'password1',
            'password2',
            'phone',
            'places',
            'agreement',
        ]
        help_texts = {
            'places': _("Mikrorajonai, gyvenvietės arba miestai, kuriuose darysite „Maisto banko“ akcijas."),
        }
        labels = {
            'first_name': _("Pavadinimas"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True


class VolunteerBaseForm(forms.Form):
    first_name = User._meta.get_field('first_name').formfield()
    last_name = User._meta.get_field('last_name').formfield()

    class Meta:
        model = Volunteer
        autocomplete_fields = ('place',)
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'place',
            'shift',
            'experience',
        ]
        help_texts = {
            'place': _("Mikrorajonas, gyvenvietė arba miestas, kuriame norite savanoriauti."),
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
                'place': volunteer.place,
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
        volunteer.place = cldata['place']
        volunteer.phone = cldata['phone']
        volunteer.experience = cldata['experience']
        volunteer.save()
        volunteer.shift = cldata['shift']

        if changed_email:
            email_address = EmailAddress.objects.add_email(request, user, cldata['email'], confirm=True)
            email_address.set_as_primary()


class VolunteerProfileForm(VolunteerBaseForm, al.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'type': 'email'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = get_adapter().clean_email(value)
        if value and value != self.instance.user.email:
            users = filter_users_by_email(value)
            on_diff_account = [u for u in users if u.pk != self.instance.user.pk]
            if on_diff_account:
                raise forms.ValidationError(_("A user is already registered with this e-mail address."))
            email_address = EmailAddress.objects.add_email(self.request, self.instance.useruser, value, confirm=True)
            if not email_address.verified:
                raise forms.ValidationError(_(
                    "Patikrinkite savo el. paštą ir patvirtinkite šį el. pašto adresą, tada galėsite jį naudoti."
                ))
        return value


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
            'place',
            'shift',
            'experience',
        ]

    def custom_signup(self, request, user):
        volunteer = Volunteer()
        self.update_profile(request, user, volunteer)
