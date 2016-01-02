import autocomplete_light.shortcuts as al

from savanoriai.core.models import Place


class CityAutocomplete(al.AutocompleteModelBase):
    model = Place
    search_fields = ['^wikipedia_title']
    order_by = '-population'
    attrs = {
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 16,
        'class': 'modern-style',
    }

al.register(CityAutocomplete)
