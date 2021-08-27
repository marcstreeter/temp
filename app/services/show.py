from typing import Optional

from models.show import (
    Show,
    ShowData,
)


async def listing(
    artist: Optional[int] = None,
    country: Optional[int] = None,
    rating: Optional[int] = None,
):
    options = {}
    if artist:
        options["cast__id"] = artist
    if country:
        options["country__id"] = country
    if rating:
        options["rating__id"] = rating
    return await ShowData.from_queryset(Show.filter(**options))
