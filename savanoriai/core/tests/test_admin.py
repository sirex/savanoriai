from django.core import mail

from savanoriai.core import factories
from savanoriai.core.models import Organisation, Volunteer
from savanoriai.core.tests.utils import errors


def test_organisation(app):
    place = factories.PlaceFactory()
    admin = factories.AdminUserFactory()

    # Create new organisation
    resp = app.get('/admin/core/organisation/add/', user=admin.username)
    assert resp.status_int == 200

    form = resp.forms['organisation_form']
    form['first_name'] = 'First'
    form['email'] = 'test@example.com'
    form['phone'] = '1111111111'
    form['places'].force_value([place.pk])
    resp = form.submit('_continue')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    obj = Organisation.objects.get(user__email='test@example.com')
    assert obj.user.first_name == 'First'
    assert obj.phone == '1111111111'
    assert [x.wikipedia_title for x in obj.places.all()] == [place.wikipedia_title]

    # Update existing organisation
    resp = app.get('/admin/core/organisation/%d/change/' % obj.pk, user=admin.username)
    assert resp.status_int == 200

    form = resp.forms['organisation_form']
    form['first_name'] = 'Name'
    form['email'] = 'name@example.com'
    form['phone'] = '2222222222'
    form['places'].force_value([place.pk])
    resp = form.submit('_continue')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    obj = Organisation.objects.get(pk=obj.pk)
    assert obj.user.first_name == 'Name'
    assert obj.phone == '2222222222'
    assert [x.wikipedia_title for x in obj.places.all()] == [place.wikipedia_title]


def test_volunteer(app):
    admin = factories.AdminUserFactory()
    place = factories.PlaceFactory()
    shifts = factories.ShiftFactory.create_batch(len(factories.shifts))

    # Create new volunteer
    resp = app.get('/admin/core/volunteer/add/', user=admin.username)
    assert resp.status_int == 200

    form = resp.forms['volunteer_form']
    form['first_name'] = 'First'
    form['last_name'] = 'Last'
    form['email'] = 'test@example.com'
    form['phone'] = '1111111111'
    form['experience'] = '1'
    form['places'].force_value([place.pk])
    form['shift'] = [shifts[0].pk]
    resp = form.submit('_continue')
    # resp.showbrowser()
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    obj = Volunteer.objects.get(user__email='test@example.com')
    assert obj.user.first_name == 'First'
    assert obj.phone == '1111111111'
    assert [x.wikipedia_title for x in obj.places.all()] == [place.wikipedia_title]

    # Update existing volunteer
    resp = app.get('/admin/core/volunteer/%d/change/' % obj.pk, user=admin.username)
    assert resp.status_int == 200

    form = resp.forms['volunteer_form']
    form['first_name'] = 'Name'
    form['last_name'] = 'Last'
    form['email'] = 'name@example.com'
    form['phone'] = '2222222222'
    form['places'].force_value([place.pk])
    form['shift'] = [shifts[0].pk]
    resp = form.submit('_continue')
    assert resp.status_int == 302, errors(resp)
    assert len(mail.outbox) == 0

    obj = Volunteer.objects.get(pk=obj.pk)
    assert obj.user.first_name == 'Name'
    assert obj.phone == '2222222222'
    assert [x.wikipedia_title for x in obj.places.all()] == [place.wikipedia_title]
