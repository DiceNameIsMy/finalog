from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import uuid


@dataclass
class Operation:
    id: uuid.UUID
    account_id: uuid.UUID
    amount: Decimal
    created_at: datetime
