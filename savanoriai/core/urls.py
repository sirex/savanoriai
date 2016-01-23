from django.conf.urls import url

from allauth.account import views as allauth
from savanoriai.core import views
from savanoriai.core.forms import OrgSignupForm, VolunteerSignupForm

signup_organisation = allauth.SignupView.as_view(
    template_name="organisations/signup.html",
    form_class=OrgSignupForm,
)

signup_volunteer = allauth.SignupView.as_view(
    template_name="volunteers/signup.html",
    form_class=VolunteerSignupForm,
)

urlpatterns = [
    url(r'^$', allauth.login, name='index'),
    url(r'^organisation/signup/$', signup_organisation, name='signup_organisation'),
    url(r'^organisation/profile/$', views.organisation_profile, name='organisation_profile'),
    url(r'^volunteer/signup/$', signup_volunteer, name='signup_volunteer'),
    url(r'^volunteer/profile/$', views.volunteer_profile, name='volunteer_profile'),
]
