"""
byceps.services.text_diff.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from difflib import HtmlDiff
from typing import Optional


def create_html_diff(from_text: str, to_text: str, from_description: str,
                     to_description: str, *, numlines: int=3) -> Optional[str]:
    """Calculate the difference between the two texts and render it as HTML.

    If the texts to compare are equal, `None` is returned.
    """
    from_text = _fallback_if_none(from_text)
    to_text = _fallback_if_none(to_text)

    if from_text == to_text:
        return None

    from_lines = from_text.split('\n')
    to_lines = to_text.split('\n')

    return HtmlDiff().make_table(from_lines, to_lines,
                                 from_description, to_description,
                                 context=True, numlines=numlines)


def _fallback_if_none(value: Optional[str], *, fallback: str='') -> str:
    return value if (value is not None) else fallback