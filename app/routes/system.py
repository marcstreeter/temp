from fastapi import APIRouter

from schemas.base import BaseSerializer
from services import system as svc

router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[],
)


@router.post("/initialize", response_model=BaseSerializer)
async def initialize():
    await svc.initialize()
    return BaseSerializer(message="initialized")


@router.get("/status")
def status():
    return BaseSerializer(message="running")
