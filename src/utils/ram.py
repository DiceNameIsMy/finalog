from datetime import datetime
import uuid

import utils


def make_id() -> uuid.UUID:
    return uuid.uuid4()


def get_created_at_date() -> datetime:
    return utils.dt.tz_aware_current_dt()
