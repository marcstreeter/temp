import logging
from typing import Optional

from fastapi import APIRouter

from models.show import ShowData
from schemas.base import BaseSerializer
from services import show as svc

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/show",
    tags=["show"],
    dependencies=[],
)


class Serializer(BaseSerializer):
    data: list[ShowData]


@router.get("/", response_model=Serializer)
async def listing(
    artist_id: Optional[int] = None,
    country_id: Optional[int] = None,
    rating_id: Optional[int] = None,
):
    logger.debug("serving show listing")
    data = await svc.listing(artist=artist_id, country=country_id, rating=rating_id)
    return Serializer(data=data)
