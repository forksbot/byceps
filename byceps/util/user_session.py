"""
byceps.util.user_session
~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from enum import Enum
from typing import Optional, Set

from flask import session

from ..services.authentication.exceptions import AuthenticationFailed
from ..services.authentication.session.models.current_user import CurrentUser
from ..services.authentication.session import service as session_service
from ..services.user import service as user_service
from ..services.user.transfer.models import User
from ..typing import PartyID, UserID

from .authorization import get_permissions_for_user


KEY_LOCALE = 'locale'
KEY_USER_ID = 'user_id'
KEY_USER_AUTH_TOKEN = 'user_auth_token'


def start(user_id: UserID, auth_token: str, *, permanent: bool = False) -> None:
    """Initialize the user's session by putting the relevant data
    into the session cookie.
    """
    session[KEY_USER_ID] = str(user_id)
    session[KEY_USER_AUTH_TOKEN] = str(auth_token)
    session.permanent = permanent


def end() -> None:
    """End the user's session by deleting the session cookie."""
    session.pop(KEY_USER_ID, None)
    session.pop(KEY_USER_AUTH_TOKEN, None)
    session.permanent = False


def get_current_user(
    required_permissions: Set[Enum],
    locale: Optional[str],
    *,
    party_id: Optional[PartyID] = None,
) -> CurrentUser:
    user = get_user(party_id=party_id)

    if user is None:
        return session_service.get_anonymous_current_user(locale)

    permissions = get_permissions_for_user(user.id)

    if not required_permissions.issubset(permissions):
        return session_service.get_anonymous_current_user(locale)

    return session_service.get_authenticated_current_user(
        user, permissions, locale
    )


def get_user(*, party_id: Optional[PartyID] = None) -> Optional[User]:
    """Return the current user if authenticated, `None` if not."""
    user_id = session.get(KEY_USER_ID)
    auth_token = session.get(KEY_USER_AUTH_TOKEN)

    return _load_user(user_id, auth_token, party_id=party_id)


def _load_user(
    user_id: Optional[str],
    auth_token: Optional[str],
    *,
    party_id: Optional[PartyID] = None,
) -> Optional[User]:
    """Load the user with that ID.

    Return `None` if:
    - the ID is unknown.
    - the account is not enabled.
    - the auth token is invalid.
    """
    if user_id is None:
        return None

    user = user_service.find_active_user(
        user_id, include_avatar=True, include_orga_flag_for_party_id=party_id
    )

    if user is None:
        return None

    # Validate auth token.
    if (auth_token is None) or not _is_auth_token_valid(user.id, auth_token):
        # Bad auth token, not logging in.
        return None

    return user


def _is_auth_token_valid(user_id: UserID, auth_token: str) -> bool:
    try:
        session_service.authenticate_session(user_id, auth_token)
    except AuthenticationFailed:
        return False
    else:
        return True


def get_locale() -> Optional[str]:
    """Return the locale set in the session, if any."""
    return session.get(KEY_LOCALE)


def set_locale(locale: str) -> None:
    """Set locale for the session."""
    session[KEY_LOCALE] = locale
