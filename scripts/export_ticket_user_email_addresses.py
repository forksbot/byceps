#!/usr/bin/env python

"""Export the email addresses of ticket users for a party as CSV.

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from typing import Iterator

import click

from byceps.services.ticketing import ticket_service
from byceps.services.user import service as user_service
from byceps.typing import PartyID
from byceps.util.system import get_config_filename_from_env_or_exit

from _util import app_context
from _validators import validate_party


@click.command()
@click.argument('party', callback=validate_party)
def execute(party):
    email_addresses = list(_get_email_addresses(party.id))

    # Sort to produce stable output.
    email_addresses.sort()

    for email_address in email_addresses:
        print(email_address)


def _get_email_addresses(party_id: PartyID) -> Iterator[str]:
    user_ids = ticket_service.get_ticket_users_for_party(party_id)

    user_ids_and_email_addresses = user_service.get_email_addresses(user_ids)
    for _, email_address in user_ids_and_email_addresses:
        if email_address:
            yield email_address


if __name__ == '__main__':
    config_filename = get_config_filename_from_env_or_exit()
    with app_context(config_filename):
        execute()
