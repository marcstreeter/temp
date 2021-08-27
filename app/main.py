from utils.server import serve
from routes import (
    artist,
    category,
    country,
    movie,
    show,
    system,
)

serve.include_router(artist.router)
serve.include_router(category.router)
serve.include_router(country.router)
serve.include_router(movie.router)
serve.include_router(show.router)
serve.include_router(system.router)
