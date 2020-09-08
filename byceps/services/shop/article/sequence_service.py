"""
byceps.services.shop.article.sequence_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from typing import List, Optional

from ....database import db

from ..sequence.models import NumberSequence as DbNumberSequence
from ..sequence.transfer.models import Purpose
from ..shop.transfer.models import ShopID

from .transfer.models import (
    ArticleNumber,
    ArticleNumberSequence,
    ArticleNumberSequenceID,
)


def create_article_number_sequence(
    shop_id: ShopID, prefix: str, *, value: Optional[int] = None
) -> ArticleNumberSequenceID:
    """Create an article number sequence."""
    sequence = DbNumberSequence(shop_id, Purpose.article, prefix, value=value)

    db.session.add(sequence)
    db.session.commit()

    return sequence.id


def delete_article_number_sequence(
    sequence_id: ArticleNumberSequenceID,
) -> None:
    """Delete the article number sequence."""
    db.session.query(DbNumberSequence) \
        .filter_by(id=sequence_id) \
        .delete()

    db.session.commit()


def find_article_number_sequence(
    sequence_id: ArticleNumberSequenceID,
) -> Optional[ArticleNumberSequence]:
    """Return the article number sequence, or `None` if the sequence ID
    is unknown or if the sequence's purpose is not article numbers.
    """
    sequence = DbNumberSequence.query \
        .filter_by(id=sequence_id) \
        .filter_by(_purpose=Purpose.article.name) \
        .one_or_none()

    if sequence is None:
        return None

    return _db_entity_to_article_number_sequence(sequence)


def find_article_number_sequences_for_shop(
    shop_id: ShopID,
) -> List[ArticleNumberSequence]:
    """Return the article number sequences defined for that shop."""
    sequences = DbNumberSequence.query \
        .filter_by(shop_id=shop_id) \
        .filter_by(_purpose=Purpose.article.name) \
        .all()

    return [
        _db_entity_to_article_number_sequence(sequence)
        for sequence in sequences
    ]


class ArticleNumberGenerationFailed(Exception):
    """Indicate that generating a prefixed, sequential article number
    has failed.
    """

    def __init__(self, message: str) -> None:
        self.message = message


def generate_article_number(
    sequence_id: ArticleNumberSequenceID,
) -> ArticleNumber:
    """Generate and reserve the next article number from this sequence."""
    sequence = DbNumberSequence.query \
        .filter_by(id=sequence_id) \
        .filter_by(_purpose=Purpose.article.name) \
        .with_for_update() \
        .one_or_none()

    if sequence is None:
        raise ArticleNumberGenerationFailed(
            f'No article number sequence found for ID "{sequence_id}".'
        )

    sequence.value = DbNumberSequence.value + 1
    db.session.commit()

    return ArticleNumber(f'{sequence.prefix}{sequence.value:05d}')


def _db_entity_to_article_number_sequence(
    sequence: DbNumberSequence,
) -> ArticleNumberSequence:
    return ArticleNumberSequence(
        sequence.id,
        sequence.shop_id,
        sequence.prefix,
        sequence.value,
    )
