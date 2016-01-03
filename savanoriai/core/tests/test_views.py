import re
import pytest

from django.core import mail

from django_webtest import DjangoTestApp, WebTestMixin

from savanoriai.core import factories
from savanoriai.core.models import Volunteer


@pytest.fixture
def app(request, db):
    mixin = WebTestMixin()
    mixin._patch_settings()
    request.addfinalizer(mixin._unpatch_settings)
    return DjangoTestApp(extra_environ=mixin.extra_environ)


def errors(resp):
    if 'form' in resp.context:
        return resp.context['form'].errors


def test_index(app):
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
    form['place'].force_value([place.pk])
    form['shift'] = [shifts[0].pk]
    form['agreement'] = True
    resp = form.submit()
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[savanoriai.maistobankas.lt] Prašome patvirtinti savo el. pašto adresą'

    # Check if user was created
    volunteer = Volunteer.objects.get(user__email='test@example.com')
    assert volunteer.user.first_name == 'First'
    assert volunteer.user.last_name == 'Last'
    assert volunteer.place.wikipedia_title == 'Senamiestis'
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
    assert resp.request.path == '/accounts/profile/'
