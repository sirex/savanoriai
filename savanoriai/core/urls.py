from django.conf.urls import url

from allauth.account import views as allauth
from savanoriai.core import views
from savanoriai.core.forms import OrgSignupForm, VolunteerSignupForm

signup_org = allauth.SignupView.as_view(form_class=OrgSignupForm)
signup_volunteer = allauth.SignupView.as_view(form_class=VolunteerSignupForm)

urlpatterns = [
    url(r'^$', allauth.login, name='index'),
    url(r'^accounts/signup/org/$', signup_org, name='signup_org'),
    url(r'^accounts/signup/volunteer/$', signup_volunteer, name='signup_volunteer'),
    url(r'^accounts/profile/$', views.volunteer_profile, name='volunteer_profile'),
]
