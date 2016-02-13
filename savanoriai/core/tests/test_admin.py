from django.core import mail

from savanoriai.core import factories
from savanoriai.core.models import Organisation
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
