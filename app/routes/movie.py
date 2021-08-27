import logging
from typing import Optional

from fastapi import APIRouter

from models.movie import MovieData
from models.artist import ArtistData
from schemas.base import BaseSerializer
from services import movie as svc

router = APIRouter(
    prefix="/movie",
    tags=["movie"],
    dependencies=[],
)

logger = logging.getLogger(__name__)


class Serializer(BaseSerializer):
    data: list[MovieData]


class SerializerActor(BaseSerializer):
    data: list[ArtistData]


@router.get("/", response_model=Serializer)
async def listing(
    artist_id: Optional[int] = None,
    country_id: Optional[int] = None,
    rating_id: Optional[int] = None,
):
    logger.debug("serving movie listing")
    data = await svc.listing(artist=artist_id, country=country_id, rating=rating_id)
    return Serializer(data=data)


@router.get("/{movie_id}", response_model=Serializer)
async def detail(movie_id: int):
    data = await svc.detail(movie_id)
    return Serializer(data=[data])


# @router.get("/{movie}/actor", response_model=SerializerActor)
# async def detail(movie_id: int):
#     data = await svc.actors(movie_id=movie_id)
#     return SerializerActor(data=data)
