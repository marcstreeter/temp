from fastapi import APIRouter

from schemas.base import BaseSerializer

router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[],
)


@router.get("/status")
def status():
    return BaseSerializer(message="running")
