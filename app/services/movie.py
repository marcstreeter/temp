from typing import Optional

from models.movie import (
    Movie,
    MovieData,
)

# from models.artist import (
#     Artist,
#     ArtistData,
# )


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
    return await MovieData.from_queryset(Movie.filter(**options))


async def detail(movie_id: int):
    return await MovieData.from_queryset_single(Movie.get(id=movie_id))


# async def actor(movie_id: int):
#     return await Movie.get()
