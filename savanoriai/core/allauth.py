from django.http import Http404
from django.core.urlresolvers import reverse

from allauth.utils import get_current_site
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
            return reverse('volunteers_list')

        try:
            request.user.volunteer
        except Volunteer.DoesNotExist:
            raise Http404()
        else:
            return reverse('volunteer_profile')

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        user = emailconfirmation.email_address.user
        ctx = {
            "user": user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            if Organisation.objects.filter(user=user).exists():
                email_template = 'account/email/organisation_email_confirmation_signup'
            else:
                email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)
