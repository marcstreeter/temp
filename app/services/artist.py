from models.artist import (
    Artist,
    ArtistData,
)


async def listing():
    return await ArtistData.from_queryset(Artist.all())


async def detail(item_id: int):
    return await ArtistData.from_queryset_single(Artist.get(id=item_id))
