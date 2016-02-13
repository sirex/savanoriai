import re

from django.core import mail

from savanoriai.core import factories
from savanoriai.core.models import Volunteer, Organisation, VolunteerCampaign
from savanoriai.core.tests.utils import errors


def test_volunteer(app):
    place = factories.PlaceFactory()
    shifts = factories.ShiftFactory.create_batch(len(factories.shifts))

    # Open login form
    resp = app.get('/')

    # Click on 'Savanoriams'
    resp = resp.click('Savanoriams')

    # Fill and submit registration form
    form = resp.forms['signup_form']
    form['first_name'] = 'First'
    form['last_name'] = 'Last'
    form['email'] = 'test@example.com'
    form['password1'] = 'secret'
    form['password2'] = 'secret'
    form['places'].force_value([place.pk])
    form['shift'] = [shifts[0].pk]
    form['agreement'] = True
    resp = form.submit()
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[savanoriai.maistobankas.lt] Prašome patvirtinti savo el. pašto adresą'
    assert 'savanorio profilį' in mail.outbox[0].body
    assert 'organizacijos profilį' not in mail.outbox[0].body

    # Check if user was created
    volunteer = Volunteer.objects.get(user__email='test@example.com')
    assert volunteer.user.first_name == 'First'
    assert volunteer.user.last_name == 'Last'
    assert [x.wikipedia_title for x in volunteer.places.all()] == ['Senamiestis']
    assert [shift.title for shift in volunteer.shift.all()] == ['Pirmadienis (14:45-18:00)']

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/accounts/confirm-email/'

    # Confirg email
    confirmation_url = re.search(r'/accounts/confirm-email/[^/]+/', mail.outbox[0].body).group(0)
    resp = app.get(confirmation_url)
    resp = resp.form.submit()
    resp = resp.follow()
    assert resp.request.path == '/accounts/login/'

    # Login
    form = resp.forms['login']
    form['login'] = 'test@example.com'
    form['password'] = 'secret'
    resp = form.submit()
    assert resp.status_int == 302, errors(resp)

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/volunteer/profile/'


def test_volunteer_profile(app):
    volunteer = factories.VolunteerFactory()
    naujamiestis = factories.PlaceFactory(wikipedia_title='Naujamiestis')

    resp = app.get('/volunteer/profile/', user=volunteer.user.username)
    assert resp.status_int == 200

    # Fill and submit profile form
    form = resp.forms['volunteer_profile_form']
    form['first_name'] = 'New first'
    form['last_name'] = 'New last'
    form['places'].force_value([naujamiestis.pk])
    resp = form.submit('action', value='update_profile')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/volunteer/profile/'

    # Check if for was saved
    volunteer = Volunteer.objects.get(pk=volunteer.pk)
    assert volunteer.user.first_name == 'New first'
    assert volunteer.user.last_name == 'New last'
    assert [x.wikipedia_title for x in volunteer.places.all()] == ['Naujamiestis']


def test_volunteer_change_email(app):
    volunteer = factories.VolunteerFactory()

    resp = app.get('/volunteer/profile/', user=volunteer.user.username)
    assert resp.status_int == 200

    # Change unconfirmed email
    form = resp.forms['volunteer_profile_form']
    form['email'] = 'new@example.com'
    resp = form.submit('action', value='update_profile')
    assert resp.status_int == 200
    assert errors(resp) == {'email': [
        'Patikrinkite savo el. paštą ir patvirtinkite šį el. pašto adresą, tada galėsite jį naudoti.',
    ]}
    assert len(mail.outbox) == 1

    # Confirm unconfirmed email
    confirmation_url = re.search(r'/accounts/confirm-email/[^/]+/', mail.outbox[0].body).group(0)
    resp = app.get(confirmation_url)
    resp = resp.form.submit()
    resp = resp.follow()
    assert resp.request.path == '/volunteer/profile/'

    # Change to confirmed email
    form = resp.forms['volunteer_profile_form']
    form['email'] = 'new@example.com'
    resp = form.submit('action', value='update_profile')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 1

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/volunteer/profile/'

    # Check if for was saved
    volunteer = Volunteer.objects.get(pk=volunteer.pk)
    assert volunteer.user.email == 'new@example.com'


def test_volunteer_change_password(app):
    volunteer = factories.VolunteerFactory()
    volunteer.user.set_password('senas')
    volunteer.user.save()

    resp = app.get('/volunteer/profile/', user=volunteer.user.username)
    assert resp.status_int == 200

    # Change unconfirmed email
    form = resp.forms['change_password_form']
    form['oldpassword'] = 'senas'
    form['password1'] = 'naujas'
    form['password2'] = 'naujas'
    resp = form.submit('action', value='change_password')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/volunteer/profile/'

    # Check if for was saved
    volunteer = Volunteer.objects.get(pk=volunteer.pk)
    assert volunteer.user.check_password('naujas')


def test_organisation(app):
    factories.CampaignFactory()
    place = factories.PlaceFactory()

    # Open login form
    resp = app.get('/')

    # Click on 'Savanoriams'
    resp = resp.click('Organizacijoms')

    # Fill and submit registration form
    form = resp.forms['signup_form']
    form['first_name'] = 'First'
    form['email'] = 'test@example.com'
    form['phone'] = '1111111111'
    form['password1'] = 'secret'
    form['password2'] = 'secret'
    form['places'].force_value([place.pk])
    form['agreement'] = True
    resp = form.submit()
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[savanoriai.maistobankas.lt] Prašome patvirtinti savo el. pašto adresą'
    assert 'organizacijos profilį' in mail.outbox[0].body
    assert 'savanorio profilį' not in mail.outbox[0].body

    # Check if user was created
    volunteer = Organisation.objects.get(user__email='test@example.com')
    assert volunteer.user.first_name == 'First'
    assert volunteer.user.last_name == ''
    assert volunteer.phone == '1111111111'
    assert [x.wikipedia_title for x in volunteer.places.all()] == ['Senamiestis']

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/accounts/confirm-email/'

    # Confirg email
    confirmation_url = re.search(r'/accounts/confirm-email/[^/]+/', mail.outbox[0].body).group(0)
    resp = app.get(confirmation_url)
    resp = resp.form.submit()
    resp = resp.follow()
    assert resp.request.path == '/accounts/login/'

    # Login
    form = resp.forms['login']
    form['login'] = 'test@example.com'
    form['password'] = 'secret'
    resp = form.submit()
    assert resp.status_int == 302, errors(resp)

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/volunteers/'


def test_organisation_profile(app):
    org = factories.OrganisationFactory()
    naujamiestis = factories.PlaceFactory(wikipedia_title='Naujamiestis')

    resp = app.get('/organisation/profile/', user=org.user.username)
    assert resp.status_int == 200

    # Fill and submit profile form
    form = resp.forms['organisation_profile_form']
    form['first_name'] = 'New name'
    form['places'].force_value([naujamiestis.pk])
    resp = form.submit('action', value='update_profile')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/organisation/profile/'

    # Check if for was saved
    org = Organisation.objects.get(pk=org.pk)
    assert org.user.first_name == 'New name'
    assert [x.wikipedia_title for x in org.places.all()] == ['Naujamiestis']


def test_organisation_change_email(app):
    factories.CampaignFactory()
    organisation = factories.OrganisationFactory()

    resp = app.get('/organisation/profile/', user=organisation.user.username)
    assert resp.status_int == 200

    # Change unconfirmed email
    form = resp.forms['organisation_profile_form']
    form['email'] = 'new@example.com'
    resp = form.submit('action', value='update_profile')
    assert resp.status_int == 200
    assert errors(resp) == {'email': [
        'Patikrinkite savo el. paštą ir patvirtinkite šį el. pašto adresą, tada galėsite jį naudoti.',
    ]}
    assert len(mail.outbox) == 1

    # Confirm unconfirmed email
    confirmation_url = re.search(r'/accounts/confirm-email/[^/]+/', mail.outbox[0].body).group(0)
    resp = app.get(confirmation_url)
    resp = resp.form.submit()
    resp = resp.follow()
    assert resp.request.path == '/volunteers/'

    # Change to confirmed email
    resp = app.get('/organisation/profile/', user=organisation.user.username)
    form = resp.forms['organisation_profile_form']
    form['email'] = 'new@example.com'
    resp = form.submit('action', value='update_profile')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 1

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/organisation/profile/'

    # Check if for was saved
    organisation = Organisation.objects.get(pk=organisation.pk)
    assert organisation.user.email == 'new@example.com'


def test_organisation_change_password(app):
    organisation = factories.OrganisationFactory()
    organisation.user.set_password('senas')
    organisation.user.save()

    resp = app.get('/organisation/profile/', user=organisation.user.username)
    assert resp.status_int == 200

    # Change unconfirmed email
    form = resp.forms['change_password_form']
    form['oldpassword'] = 'senas'
    form['password1'] = 'naujas'
    form['password2'] = 'naujas'
    resp = form.submit('action', value='change_password')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    # Check redirect
    resp = resp.follow()
    assert resp.request.path == '/organisation/profile/'

    # Check if for was saved
    organisation = Organisation.objects.get(pk=organisation.pk)
    assert organisation.user.check_password('naujas')


def test_toggle_choice(app):
    campaign = factories.CampaignFactory()
    organisation = factories.OrganisationFactory()
    other_organisation = factories.OrganisationFactory(user__username='org2')
    volunteer = factories.VolunteerFactory()
    user = organisation.user.username

    def volunteer_campaigns():
        return [x.organisation for x in VolunteerCampaign.objects.filter(campaign=campaign, volunteer=volunteer)]

    assert volunteer_campaigns() == []

    resp = app.post('/volunteers/toggle-choice/', {'volunteer_id': volunteer.pk}, user=user)
    assert resp.status_int == 200
    assert resp.json == {'label': 'Pakviesta', 'state': 'invited'}
    assert volunteer_campaigns() == [organisation]
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[savanoriai.maistobankas.lt] Kvietimas prisijungti prie akcijos'
    assert re.search(r'/volunteer/confirm-invite/([^/]+)/', mail.outbox[0].body) is not None

    resp = app.post('/volunteers/toggle-choice/', {'volunteer_id': volunteer.pk}, user=user)
    assert resp.status_int == 200
    assert resp.json == {'label': 'Pakviesta', 'state': 'invited'}
    assert volunteer_campaigns() == [organisation]
    assert len(mail.outbox) == 1

    user = other_organisation.user.username
    resp = app.post('/volunteers/toggle-choice/', {'volunteer_id': volunteer.pk}, user=user)
    assert resp.status_int == 200
    assert resp.json == {'label': 'Užimta', 'state': 'taken'}
    assert volunteer_campaigns() == [organisation]
    assert len(mail.outbox) == 1

    vc = VolunteerCampaign.objects.get(campaign=campaign, volunteer=volunteer, organisation=organisation)
    vc.accepted = True
    vc.save()
    user = organisation.user.username
    resp = app.post('/volunteers/toggle-choice/', {'volunteer_id': volunteer.pk}, user=user)
    assert resp.status_int == 200
    assert resp.json == {'label': 'Patvirtinta', 'state': 'accepted'}
    assert volunteer_campaigns() == [organisation]
    assert len(mail.outbox) == 1

    user = other_organisation.user.username
    resp = app.post('/volunteers/toggle-choice/', {'volunteer_id': volunteer.pk}, user=user)
    assert resp.status_int == 200
    assert resp.json == {'label': 'Užimta', 'state': 'taken'}
    assert volunteer_campaigns() == [organisation]
    assert len(mail.outbox) == 1

    vc.accepted = False
    vc.save()
    user = organisation.user.username
    resp = app.post('/volunteers/toggle-choice/', {'volunteer_id': volunteer.pk}, user=user)
    assert resp.status_int == 200
    assert resp.json == {'label': 'Atmesta', 'state': 'rejected'}
    assert volunteer_campaigns() == [organisation]
    assert len(mail.outbox) == 1
