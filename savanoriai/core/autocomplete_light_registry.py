from django.utils.translation import ugettext_lazy as _

import autocomplete_light.shortcuts as al

from savanoriai.core.models import Place


class CityAutocomplete(al.AutocompleteModelBase):
    model = Place
    search_fields = ['^wikipedia_title']
    limit_choices = 8
    split_words = False
    order_by = '-population'
    attrs = {
        'data-autocomplete-minimum-characters': 1,
        'placeholder': _('Įveskite kelias vietovės raides'),
    }

al.register(CityAutocomplete)
