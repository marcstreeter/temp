from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models.base import BulkCreate


class Artist(BulkCreate):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, unique=True)


ArtistData = pydantic_model_creator(Artist, name="Artist", include=("id", "name"))
