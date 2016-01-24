from django.contrib import admin

from savanoriai.core.models import Campaign, Shift, Volunteer, Organisation

admin.site.register(Campaign)
admin.site.register(Shift)
admin.site.register(Volunteer)
admin.site.register(Organisation)
