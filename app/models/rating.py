from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models.base import BulkCreate


class Rating(BulkCreate):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=16, unique=True)


RatingData = pydantic_model_creator(Rating, name="Rating", include=("id", "name"))
