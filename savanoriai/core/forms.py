from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from autocomplete_light import shortcuts as al
from allauth.account.forms import SignupForm

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


class VolunteerSignupForm(SignupForm, al.ModelForm):
    first_name = User._meta.get_field('first_name').formfield()
    last_name = User._meta.get_field('last_name').formfield()
    agreement = forms.BooleanField(initial=False, label=agreement_text)

    class Meta:
        model = Volunteer
        autocomplete_fields = ('place',)
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
            'agreement',
        ]
        help_texts = {
            'place': _("Mikrorajonas, gyvenvietė arba miestas, kuriame norite savanoriauti."),
            'experience': _("Nurodykite, kiek kartų jau esate savanoriavę."),
        }
        widgets = {
            'shift': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def custom_signup(self, request, user):
        cldata = self.cleaned_data

        print(cldata)

        user.first_name = cldata['first_name']
        user.last_name = cldata['last_name']
        user.save()

        volunteer = Volunteer.objects.create(
            user=user,
            place=cldata['place'],
            phone=cldata['phone'],
            experience=cldata['experience'],
        )

        for shift in cldata['shift']:
            volunteer.shift.add(shift)
