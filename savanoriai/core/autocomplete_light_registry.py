import autocomplete_light.shortcuts as al

from savanoriai.core.models import City


class CityAutocomplete(al.AutocompleteModelBase):
    model = City
    search_fields = ['^name']
    attrs = {
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 16,
        'class': 'modern-style',
    }

al.register(CityAutocomplete)
