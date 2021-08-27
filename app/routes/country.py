from fastapi import APIRouter

from models.country import CountryData
from schemas.base import BaseSerializer
from services import country as svc

router = APIRouter(
    prefix="/country",
    tags=["country"],
    dependencies=[],
)


class Serializer(BaseSerializer):
    data: list[CountryData]


@router.get("/", response_model=Serializer)
async def listing():
    data = await svc.listing()
    return Serializer(data=data)
