from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import uuid


@dataclass
class Account:
    id: uuid.UUID
    name: str
    created_at: datetime
