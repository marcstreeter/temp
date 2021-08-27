from typing import (
    Union,
    Tuple,
    Iterator,
)
from pathlib import Path
from uuid import uuid4

import kaggle
import pandas as pd

from utils import (
    config,
    date,
)
from models.rating import Rating
from models.show import Show
from models.movie import Movie
from models.artist import Artist
from models.category import Category
from models.country import Country

ROW_BATCH_SIZE = 10 ** 6
DATASET = config.KAGGLE_DATASET
DATASET_PATH = config.KAGGLE_DATASET_PATH
ProductionType = Tuple[
    list[Show],
    list[Movie],
    dict[str, list[Artist]],
    dict[str, list[Artist]],
    dict[str, list[Category]],
    dict[str, list[Country]],
    dict[str, Rating],
]


async def initialize():
    is_populated = await _is_populated()
    if is_populated:
        return
    data_path = _get_data()
    await _parse_movies(data_path)


async def _is_populated() -> bool:
    """quick test to see if any table exists"""
    try:
        await Movie.get(id=1)
        return True
    except:  # noqa E722
        return False


def _get_data(dataset: str = DATASET, path: str = DATASET_PATH) -> Path:
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, path=path, unzip=True)
    return Path(path)


def _get_production_batch(chunk: pd.DataFrame, uuid: str) -> ProductionType:
    show_batch = []
    movie_batch = []
    actor_map_batch = {}
    director_map_batch = {}
    category_map_batch = {}
    country_map_batch = {}
    rating_map_batch = {}
    for (
        _,
        show_id,
        show_type,
        title,
        director,
        cast,
        country,
        date_added,
        release_year,
        rating,
        duration,
        listed_in,
        description,
    ) in chunk.itertuples():
        common = dict(
            netflix_id=show_id,
            title=title,
            date_added=date.parse_date(date_added),
            release_year=date.parse_year(release_year),
            rating=None,
            description=description,
        )
        show_id: str
        if show_type == "TV Show":
            show_batch.append(Show(**common, batch=uuid, seasons=_parse_seasons(duration)))
        else:
            movie_batch.append(Movie(**common, batch=uuid, runtime=_parse_runtime(duration)))
        actor_map_batch[show_id] = [Artist(name=name) for name in _split_strip(cast)]
        director_map_batch[show_id] = [Artist(name=name) for name in _split_strip(director)]
        category_map_batch[show_id] = [Category(name=name) for name in _split_strip(listed_in)]
        country_map_batch[show_id] = [Country(name=name) for name in _split_strip(country)]
        rating_map_batch[show_id] = Rating(name=rating)
    return (
        show_batch,
        movie_batch,
        actor_map_batch,
        director_map_batch,
        category_map_batch,
        country_map_batch,
        rating_map_batch,
    )


async def _parse_chunk(chunk: pd.DataFrame):
    chunk_uuid = str(uuid4())
    (
        show_batch,
        movie_batch,
        actor_map_batch,
        director_map_batch,
        category_map_batch,
        country_map_batch,
        rating_map_batch,
    ) = _get_production_batch(chunk, chunk_uuid)
    artist_batch = []
    for batch in actor_map_batch.values():
        artist_batch += batch
    for batch in director_map_batch.values():
        artist_batch += batch
    category_batch = []
    for batch in category_map_batch.values():
        category_batch += batch
    country_batch = []
    for batch in country_map_batch.values():
        country_batch += batch
    await Artist.bulk_create(artist_batch)
    await Category.bulk_create(category_batch)
    await Country.bulk_create(country_batch)
    await Rating.bulk_create(list(rating_map_batch.values()))
    await Show.bulk_create(show_batch)
    await Movie.bulk_create(movie_batch)
    movies = await Movie.filter(batch=chunk_uuid)
    shows = await Show.filter(batch=chunk_uuid)
    await _update_rating(movies, production_rating_map=rating_map_batch)
    await _update_rating(shows, production_rating_map=rating_map_batch)
    await _add_actors(movies, actor_map=actor_map_batch)
    await _add_actors(shows, actor_map=actor_map_batch)
    await _add_directors(movies, director_map=director_map_batch)
    await _add_directors(shows, director_map=director_map_batch)
    await _add_countries(movies, country_map=country_map_batch)
    await _add_countries(shows, country_map=country_map_batch)
    await _add_categories(movies, category_map=category_map_batch)
    await _add_categories(shows, category_map=category_map_batch)


async def _add_directors(
    production: Union[list[Movie], list[Show]], director_map: dict[str, list[Artist]]
):
    production_map = {item.netflix_id: item for item in production}
    for netflix_id, production in production_map.items():
        names = [director.name for director in director_map.get(netflix_id, [])]
        directors = await Artist.filter(name__in=names)
        if directors:
            await production.director.add(*directors)


async def _add_actors(
    production: Union[list[Movie], list[Show]], actor_map: dict[str, list[Artist]]
):
    production_map = {item.netflix_id: item for item in production}
    for netflix_id, production in production_map.items():
        names = [actor.name for actor in actor_map.get(netflix_id, [])]
        actors = await Artist.filter(name__in=names)
        if actors:
            await production.cast.add(*actors)


async def _add_countries(
    production: Union[list[Movie], list[Show]], country_map: dict[str, list[Country]]
):
    production_map = {item.netflix_id: item for item in production}
    for netflix_id, production in production_map.items():
        names = [actor.name for actor in country_map.get(netflix_id, [])]
        countries = await Country.filter(name__in=names)
        if countries:
            await production.country.add(*countries)


async def _add_categories(
    production: Union[list[Movie], list[Show]], category_map: dict[str, list[Category]]
):
    production_map = {item.netflix_id: item for item in production}
    for netflix_id, production in production_map.items():
        names = [category.name for category in category_map.get(netflix_id, [])]
        categories = await Category.filter(name__in=names)
        if categories:
            await production.category.add(*categories)


async def _update_rating(
    production: Union[list[Movie], list[Show]], production_rating_map: dict[str, Rating]
):
    production_map = {item.netflix_id: item for item in production}
    ratings = await Rating.all()
    rating_name_map = {rating.name: rating for rating in ratings}
    for netflix_id, production in production_map.items():
        rating_name = production_rating_map[netflix_id].name
        rating = rating_name_map[rating_name]
        production.rating = rating
        await production.save()


def _split_strip(item: str) -> Iterator[str]:
    return filter(None, list(set(name.strip() or None for name in item.split(","))))


async def _parse_csv(csv: Path):
    with pd.read_csv(csv, chunksize=ROW_BATCH_SIZE) as reader:
        for chunk in reader:
            chunk.fillna("", inplace=True)
            await _parse_chunk(chunk)


async def _parse_movies(file_path: Path):
    for csv in file_path.glob("*.csv"):
        await _parse_csv(csv)


def _parse_seasons(duration: str) -> int:
    return int(duration.replace(" Seasons", "").replace(" Season", "").strip())


def _parse_runtime(duration: str) -> int:
    return int(duration.replace(" min", "").strip())
