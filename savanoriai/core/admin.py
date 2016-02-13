from django.contrib import admin
from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress

from savanoriai.core.models import Campaign, Shift, Volunteer, Organisation
from savanoriai.core.forms import OrganisationAdminForm

User = get_user_model()

admin.site.register(Campaign)
admin.site.register(Shift)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    pass


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    form = OrganisationAdminForm

    def save_model(self, request, obj, form, change):
        cldata = form.cleaned_data
        user = obj.user if change else User()

        user.first_name = cldata['first_name']
        user.email = cldata['email']
        user.save()

        email_address, created = EmailAddress.objects.get_or_create(user=user, email=cldata['email'])
        email_address.verified = True
        email_address.set_as_primary()

        obj.user = user
        obj.phone = cldata['phone']
        obj.save()

        obj.places = cldata['places']
