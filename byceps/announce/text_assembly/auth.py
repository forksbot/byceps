"""
byceps.announce.text_assembly.auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Announce auth events.

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from ...events.auth import UserLoggedIn
from ...services.site import service as site_service

from ._helpers import get_screen_name_or_fallback


def assemble_text_for_user_logged_in(event: UserLoggedIn) -> str:
    screen_name = get_screen_name_or_fallback(event.initiator_screen_name)

    site = None
    if event.site_id:
        site = site_service.find_site(event.site_id)

    if site:
        return f'{screen_name} hat sich auf Site "{site.title}" eingeloggt.'
    else:
        return f'{screen_name} hat sich eingeloggt.'
