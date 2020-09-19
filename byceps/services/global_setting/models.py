"""
byceps.services.global_setting.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ...database import db
from ...util.instances import ReprBuilder


class Setting(db.Model):
    """A global setting."""

    __tablename__ = 'global_settings'

    name = db.Column(db.UnicodeText, primary_key=True)
    value = db.Column(db.UnicodeText)

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add_with_lookup('name') \
            .add_with_lookup('value') \
            .build()