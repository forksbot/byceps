# -*- coding: utf-8 -*-

"""
byceps.blueprints.board.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2014 Jochen Kupperschmidt
"""

from flask import g, request

from ...database import db
from ...util.framework import create_blueprint, flash_success
from ...util.templating import templated
from ...util.views import redirect_to

from ..authorization.decorators import permission_required
from ..authorization.registry import permission_registry

from .authorization import BoardPostingPermission, BoardTopicPermission
from .formatting import render_html
from .forms import PostingCreateForm, TopicCreateForm
from .models import Category, Posting, Topic


blueprint = create_blueprint('board', __name__)


permission_registry.register_enum(BoardTopicPermission)
permission_registry.register_enum(BoardPostingPermission)


blueprint.add_app_template_filter(render_html, 'bbcode')


@blueprint.route('/categories')
@templated
def category_index():
    """List categories."""
    categories = Category.query.for_current_brand().all()
    return {'categories': categories}


@blueprint.route('/categories/<id>')
@templated
def category_view(id):
    """List latest topics in the category."""
    category = Category.query.get_or_404(id)
    return {'category': category}


@blueprint.route('/topics/<id>')
@templated
def topic_view(id):
    """List postings for the topic."""
    topic = Topic.query.get_or_404(id)
    return {'topic': topic}


@blueprint.route('/categories/<category_id>/create')
@permission_required(BoardTopicPermission.create)
@templated
def topic_create_form(category_id, errorneous_form=None):
    """Show a form to create a topic in the category."""
    category = Category.query.get_or_404(category_id)
    form = errorneous_form if errorneous_form else TopicCreateForm()
    return {
        'category': category,
        'form': form,
    }


@blueprint.route('/categories/<category_id>/create', methods=['POST'])
@permission_required(BoardTopicPermission.create)
def topic_create(category_id):
    """Create a topic in the category."""
    form = TopicCreateForm(request.form)

    category = Category.query.get_or_404(category_id)
    author = g.current_user
    title = form.title.data.strip()
    body = form.body.data.strip()

    topic = Topic(category, author, title)
    posting = Posting(topic, author, body)

    db.session.add(topic)
    db.session.add(posting)
    db.session.commit()

    flash_success('Das Thema wurde hinzugefügt.')
    return redirect_to('.topic_view', id=topic.id)


@blueprint.route('/topics/<topic_id>/create')
@permission_required(BoardPostingPermission.create)
@templated
def posting_create_form(topic_id, errorneous_form=None):
    """Show a form to create a posting to the topic."""
    topic = Topic.query.get_or_404(topic_id)
    form = errorneous_form if errorneous_form else PostingCreateForm()
    return {
        'topic': topic,
        'form': form,
    }


@blueprint.route('/topics/<topic_id>/create', methods=['POST'])
@permission_required(BoardPostingPermission.create)
def posting_create(topic_id):
    """Create a posting to the topic."""
    form = PostingCreateForm(request.form)

    topic = Topic.query.get_or_404(topic_id)
    author = g.current_user
    body = form.body.data.strip()

    posting = Posting(topic, author, body)
    db.session.add(posting)
    db.session.commit()

    flash_success('Deine Antwort wurde hinzugefügt.')
    return redirect_to('.topic_view', id=topic.id)
