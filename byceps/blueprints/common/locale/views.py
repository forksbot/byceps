"""
byceps.blueprints.common.locale.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from flask import redirect, request

from ....util.framework.blueprint import create_blueprint
from ....util import user_session


blueprint = create_blueprint('locale', __name__)


@blueprint.route('/set')
def set_locale():
    """Set the locale."""
    locale = request.args.get('locale')
    user_session.set_locale(locale)
    return redirect('/')
