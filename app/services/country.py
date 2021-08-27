from models.country import (
    Country,
    CountryData,
)


async def listing():
    return await CountryData.from_queryset(Country.all())
