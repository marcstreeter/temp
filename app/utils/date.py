from typing import (
    Optional,
    Union,
)

import datetime as dt


def parse_date(date: str) -> Optional[dt.date]:
    stripped = date.strip()
    if not stripped:
        return None
    return dt.datetime.strptime(stripped, "%B %d, %Y")


def parse_year(date: Union[str, float]) -> int:
    return int(date)
