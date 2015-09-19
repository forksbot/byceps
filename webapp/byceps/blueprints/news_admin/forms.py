# -*- coding: utf-8 -*-

"""
byceps.blueprints.news_admin.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2015 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from wtforms import StringField

from ...util.l10n import LocalizedForm


class ItemCreateForm(LocalizedForm):
    slug = StringField('Slug')
