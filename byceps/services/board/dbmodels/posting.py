"""
byceps.services.board.dbmodels.posting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from datetime import datetime

from ....database import BaseQuery, db, generate_uuid
from ....typing import UserID
from ....util.instances import ReprBuilder

from ...user.dbmodels.user import User

from ..transfer.models import TopicID

from .topic import Topic


class PostingQuery(BaseQuery):

    def for_topic(self, topic_id: TopicID) -> BaseQuery:
        return self.filter_by(topic_id=topic_id)

    def without_hidden(self) -> BaseQuery:
        """Only return postings every user may see."""
        return self.filter(Posting.hidden == False)

    def earliest_to_latest(self) -> BaseQuery:
        return self.order_by(Posting.created_at.asc())

    def latest_to_earliest(self) -> BaseQuery:
        return self.order_by(Posting.created_at.desc())


class Posting(db.Model):
    """A posting."""

    __tablename__ = 'board_postings'
    query_class = PostingQuery

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    topic_id = db.Column(db.Uuid, db.ForeignKey('board_topics.id'), index=True, nullable=False)
    topic = db.relationship(Topic, backref='postings')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    creator_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.UnicodeText, nullable=False)
    last_edited_at = db.Column(db.DateTime)
    last_edited_by_id = db.Column(db.Uuid, db.ForeignKey('users.id'))
    last_edited_by = db.relationship(User, foreign_keys=[last_edited_by_id])
    edit_count = db.Column(db.Integer, default=0, nullable=False)
    hidden = db.Column(db.Boolean, default=False, nullable=False)
    hidden_at = db.Column(db.DateTime)
    hidden_by_id = db.Column(db.Uuid, db.ForeignKey('users.id'))
    hidden_by = db.relationship(User, foreign_keys=[hidden_by_id])

    def __init__(self, topic: Topic, creator_id: UserID, body: str) -> None:
        self.topic = topic
        self.creator_id = creator_id
        self.body = body

    def is_initial_topic_posting(self, topic: Topic) -> bool:
        return self == topic.initial_posting

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        builder = ReprBuilder(self) \
            .add_with_lookup('id') \
            .add('topic', self.topic.title)

        if self.hidden:
            builder.add_custom(f'hidden by {self.hidden_by.screen_name}')

        return builder.build()


class InitialTopicPostingAssociation(db.Model):
    __tablename__ = 'board_initial_topic_postings'

    topic_id = db.Column(db.Uuid, db.ForeignKey('board_topics.id'), primary_key=True)
    topic = db.relationship(Topic, backref=db.backref('initial_topic_posting_association', uselist=False))
    posting_id = db.Column(db.Uuid, db.ForeignKey('board_postings.id'), unique=True, nullable=False)
    posting = db.relationship(Posting)

    def __init__(self, topic: Topic, posting: Posting) -> None:
        self.topic = topic
        self.posting = posting
