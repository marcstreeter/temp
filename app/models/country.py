from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models.base import BulkCreate


class Country(BulkCreate):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64, unique=True)


CountryData = pydantic_model_creator(Country, name="Country", include=("id", "name"))
