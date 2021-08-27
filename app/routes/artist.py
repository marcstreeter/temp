from fastapi import APIRouter

from models.artist import ArtistData
from schemas.base import BaseSerializer
from services import artist as svc

router = APIRouter(
    prefix="/artist",
    tags=["artist"],
    dependencies=[],
)


class Serializer(BaseSerializer):
    data: list[ArtistData]


@router.get("/", response_model=Serializer)
async def listing():
    data = await svc.listing()
    return Serializer(data=data)


@router.get("/{artist}")
async def detail(artist: int):
    data = await svc.detail(artist)
    return Serializer(data=[data])
