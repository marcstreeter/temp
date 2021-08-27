from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models.base import BulkCreate


class Category(BulkCreate):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=36, unique=True)


CategoryData = pydantic_model_creator(Category, name="Category", include=("id", "name"))
