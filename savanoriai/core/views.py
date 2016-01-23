from django.shortcuts import render, redirect
from django.http import Http404
from django.core.urlresolvers import reverse

from allauth.account.forms import ChangePasswordForm
from allauth.account.decorators import verified_email_required

from savanoriai.core.models import Volunteer, Organisation
from savanoriai.core.forms import VolunteerProfileForm, OrganisationProfileForm


def index(request):
    return render(request, 'base.html', {})


@verified_email_required()
def organisation_profile(request):
    try:
        organisation = request.user.organisation
    except Organisation.DoesNotExist:
        raise Http404()

    action = request.POST.get('action') if request.method == 'POST' else None

    if action == 'update_profile':
        profile_form = OrganisationProfileForm(request, request.POST, instance=organisation)
        if profile_form.is_valid():
            profile_form.update_profile(request, request.user, organisation)
            return redirect(reverse('organisation_profile'))
    else:
        profile_form = OrganisationProfileForm(request, instance=organisation)

    if action == 'change_password':
        password_form = ChangePasswordForm(organisation.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            return redirect(reverse('organisation_profile'))
    else:
        password_form = ChangePasswordForm(organisation.user)

    return render(request, 'organisations/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


@verified_email_required()
def volunteer_profile(request):
    try:
        volunteer = request.user.volunteer
    except Volunteer.DoesNotExist:
        raise Http404()

    action = request.POST.get('action') if request.method == 'POST' else None

    if action == 'update_profile':
        profile_form = VolunteerProfileForm(request, request.POST, instance=volunteer)
        if profile_form.is_valid():
            profile_form.update_profile(request, request.user, volunteer)
            return redirect(reverse('volunteer_profile'))
    else:
        profile_form = VolunteerProfileForm(request, instance=volunteer)

    if action == 'change_password':
        password_form = ChangePasswordForm(volunteer.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            return redirect(reverse('volunteer_profile'))
    else:
        password_form = ChangePasswordForm(volunteer.user)

    return render(request, 'volunteers/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
