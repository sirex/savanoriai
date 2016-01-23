from django.http import Http404
from django.core.urlresolvers import reverse

from allauth.account.adapter import DefaultAccountAdapter

from savanoriai.core.models import Volunteer, Organisation


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        assert request.user.is_authenticated()

        try:
            request.user.organisation
        except Organisation.DoesNotExist:
            pass
        else:
            return reverse('organisation_profile')

        try:
            request.user.volunteer
        except Volunteer.DoesNotExist:
            raise Http404()
        else:
            return reverse('volunteer_profile')
