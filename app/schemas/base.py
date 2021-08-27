from pydantic import BaseModel


class BaseSerializer(BaseModel):
    data: list = []
    message: str = ""
    success: bool = True
