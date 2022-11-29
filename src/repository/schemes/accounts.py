from dataclasses import dataclass
from datetime import datetime
import uuid

from repository import enums


@dataclass
class Account:
    id: uuid.UUID
    name: str
    currency: enums.Currency
    user_id: uuid.UUID

    created_at: datetime
