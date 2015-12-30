from django.contrib import admin

from savanoriai.core.models import City, District, Volunteer


class DistrictInline(admin.TabularInline):
    model = District


class CityAdmin(admin.ModelAdmin):
    inlines = [DistrictInline]

admin.site.register(City, CityAdmin)


admin.site.register(Volunteer)
