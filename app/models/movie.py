from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models.production import Production
from models.artist import Artist
from models.country import Country
from models.category import Category


class Movie(Production):
    cast: fields.ManyToManyRelation[Artist] = fields.ManyToManyField(
        "app.Artist",
        related_name="movie_actors",
        through="movie_actor",
    )
    director: fields.ManyToManyRelation[Artist] = fields.ManyToManyField(
        "app.Artist",
        related_name="movie_directors",
        through="movie_director",
    )
    country: fields.ManyToManyRelation[Country] = fields.ManyToManyField(
        "app.Country",
        related_name="movie_countries",
        through="movie_country",
    )
    category: fields.ManyToManyRelation[Category] = fields.ManyToManyField(
        "app.Category",
        related_name="movie_categories",
        through="movie_category",
    )
    runtime = fields.SmallIntField(description="length of movie in minutes")


MovieData = pydantic_model_creator(
    Movie, name="Movie", include=("id", "netflix_id", "title", "runtime")
)
