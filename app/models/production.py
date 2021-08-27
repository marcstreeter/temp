from tortoise import fields

from models.rating import Rating
from models.base import BulkCreate


class Production(BulkCreate):
    id = fields.IntField(pk=True)
    netflix_id = fields.CharField(max_length=40, unique=True)
    title = fields.CharField(max_length=256)
    date_added = fields.DateField(null=True)
    release_year = fields.SmallIntField()
    rating: fields.ForeignKeyNullableRelation[Rating] = fields.ForeignKeyField(
        "app.Rating",
        on_delete=fields.SET_NULL,
        null=True,
    )
    description = fields.TextField(null=True)
    batch = fields.CharField(max_length=36, description="key used to differentiate batches")

    class Meta:
        abstract = True
