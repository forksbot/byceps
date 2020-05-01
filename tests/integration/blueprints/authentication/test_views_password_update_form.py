"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from tests.helpers import http_client, login_user


def test_when_logged_in_form_is_available(party_app, site, user):
    login_user(user.id)

    response = send_request(party_app, user_id=user.id)

    assert response.status_code == 200


def test_when_not_logged_in_form_is_unavailable(party_app, site):
    response = send_request(party_app)

    assert response.status_code == 404


# helpers


def send_request(app, user_id=None):
    url = '/authentication/password/update'
    with http_client(app, user_id=user_id) as client:
        return client.get(url)