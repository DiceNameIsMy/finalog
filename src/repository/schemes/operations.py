from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import uuid


@dataclass
class Operation:
    id: uuid.UUID
    amount: Decimal
    account_id: uuid.UUID
    category_id: uuid.UUID
    created_at: datetime
