import pytest

from webtest import TestApp
from django.core.wsgi import get_wsgi_application


@pytest.fixture
def app():
    return TestApp(get_wsgi_application())


def test_index(app):
    resp = app.get('/')
    assert resp.status_int == 200
