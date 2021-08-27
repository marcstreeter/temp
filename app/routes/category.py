from fastapi import APIRouter

from models.category import CategoryData
from schemas.base import BaseSerializer
from services import category as svc

router = APIRouter(
    prefix="/category",
    tags=["category"],
    dependencies=[],
)


class Serializer(BaseSerializer):
    data: list[CategoryData]


@router.get("/", response_model=Serializer)
async def listing():
    data = await svc.listing()
    return Serializer(data=data)
