from django.http import Http404
from django.conf import settings
from django.utils.translation import ugettext

from allauth.account.utils import perform_login
from allauth.account.signals import user_logged_in

from savanoriai.core.models import Campaign


def get_active_campaign_or_404():
    campaign = Campaign.objects.filter(is_active=True).order_by('start_date').first()
    if campaign is None:
        raise Http404('No active campaign found.')
    else:
        return campaign


def log_user_in(request, user):
    if not request.user.is_authenticated():
        logged_in = False

        def check_logged_in(sender, **kwargs):
            nonlocal logged_in
            if kwargs.get('user') == user:
                logged_in = True

        user_logged_in.connect(check_logged_in)
        response = perform_login(request, user, email_verification=settings.ACCOUNT_EMAIL_VERIFICATION)
        user_logged_in.disconnect(check_logged_in)

        if logged_in is False:
            return response


def get_volunteer_status(volunteer_campaign, organisation):
    if volunteer_campaign is None:
        return 'free', ugettext('Laisva')
    if volunteer_campaign.organisation != organisation:
        return 'taken', ugettext('Užimta')
    if volunteer_campaign.accepted is None:
        return 'invited', ugettext('Pakviesta')
    if volunteer_campaign.accepted is True:
        return 'accepted', ugettext('Patvirtinta')
    if volunteer_campaign.accepted is False:
        return 'rejected', ugettext('Atmesta')
