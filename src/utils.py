from datetime import datetime, timezone


def tz_aware_dt(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc)


def tz_aware_current_dt() -> datetime:
    return tz_aware_dt(datetime.utcnow())
