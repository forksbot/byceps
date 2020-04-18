"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import pytest

from byceps.services.news import (
    channel_service as news_channel_service,
    service as news_service,
)

from tests.helpers import create_brand, create_user

from ...conftest import database_recreated


@pytest.fixture(scope='module')
def app(party_app, db):
    with party_app.app_context():
        with database_recreated(db):
            yield party_app


@pytest.fixture
def editor(make_user):
    yield from make_user('NewsEditor')


@pytest.fixture(scope='module')
def brand(app):
    return create_brand()


@pytest.fixture(scope='module')
def channel(brand):
    channel_id = f'{brand.id}-test'
    url_prefix = 'https://example.com/news/'

    channel = news_channel_service.create_channel(brand.id, channel_id, url_prefix)

    yield channel

    news_channel_service.delete_channel(channel_id)


def test_image_url_with_image(app, channel, editor):
    item = create_item(
        channel.id,
        'with-image',
        editor.id,
        image_url_path='breaking.png',
    )

    assert item.image_url_path == '/data/global/news_channels/acmecon-test/breaking.png'

    tear_down_news_item(item)


def test_image_url_without_image(app, channel, editor):
    item = create_item(channel.id, 'without-image', editor.id)

    assert item.image_url_path is None

    tear_down_news_item(item)


# helpers


def create_item(channel_id, slug, editor_id, *, image_url_path=None):
    title = 'the title'
    body = 'the body'

    item = news_service.create_item(
        channel_id, slug, editor_id, title, body, image_url_path=image_url_path
    )

    # Return aggregated version of item.
    return news_service.find_aggregated_item_by_slug(channel_id, slug)


def tear_down_news_item(item):
    news_service.delete_item(item.id)
