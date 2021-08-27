from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models.artist import Artist
from models.production import Production
from models.country import Country
from models.category import Category


class Show(Production):
    cast: fields.ManyToManyRelation[Artist] = fields.ManyToManyField(
        "app.Artist", related_name="show_actors", through="show_actor"
    )
    director: fields.ManyToManyRelation[Artist] = fields.ManyToManyField(
        "app.Artist",
        related_name="show_directors",
        through="show_director",
    )
    country: fields.ManyToManyRelation[Country] = fields.ManyToManyField(
        "app.Country", related_name="show_countries", through="show_country"
    )
    category: fields.ManyToManyRelation[Category] = fields.ManyToManyField(
        "app.Category", related_name="show_categories", through="show_category"
    )
    seasons = fields.SmallIntField()


ShowData = pydantic_model_creator(
    Show, name="Show", include=("id", "netflix_id", "title", "seasons")
)
