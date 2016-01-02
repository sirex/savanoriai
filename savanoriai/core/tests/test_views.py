import pytest

from django_webtest import DjangoTestApp, WebTestMixin

from django.contrib.auth import get_user_model


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
    User = get_user_model()

    resp = app.get('/')
    resp = resp.click('Savanoriams')
    form = resp.forms['signup_form']
    form['email'] = 'test@example.com'
    form['password1'] = 'secret'
    form['password2'] = 'secret'
    resp = form.submit()
    assert resp.status_int == 302, errors(resp)
    assert User.objects.filter(email='test@example.com').exists()
    resp = resp.follow()
    assert resp.request.path == ''
