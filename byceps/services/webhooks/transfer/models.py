"""
byceps.services.webhooks.transfer.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional
from uuid import UUID


WebhookID = NewType('WebhookID', UUID)


EventSelectors = Dict[str, Optional[Dict[str, List[str]]]]


@dataclass(frozen=True)
class OutgoingWebhook:
    id: WebhookID
    event_selectors: EventSelectors
    format: str
    text_prefix: Optional[str]
    extra_fields: Optional[Dict[str, Any]]
    url: str
    description: str
    enabled: bool
