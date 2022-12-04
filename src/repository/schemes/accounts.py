from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import uuid

from repository import enums


@dataclass
class Account:
    id: uuid.UUID
    name: str
    currency: enums.Currency
    base_balance: Decimal
    user_id: uuid.UUID

    created_at: datetime
