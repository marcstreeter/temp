# API Example
example netflix api service 

# Endpoints
| VERB | URL                                        | DESCRIPTION            |
| ---- | ---                                        | -----------            |
| get  | /system/status                             |                        |
| get  | /docs                                      | openapi schema         |
| get  | /movie                                     |                        |
| get  | /movie/{movie_id}                          |                        |
| get  | /movie/?[artist_id/country_id/rating_id]   |                        |
| get  | /show?[artist_id/country_id/rating_id]     |                        |
| get  | /show                                      |                        |
| get  | /category                                  |                        |
| get  | /artist                                    |                        |
| get  | /country                                   |                        |


# Development Setup
Before making changes please initialize environment

```commandline
pip install -r requirements/development.txt
pre-commit install
```

Starting up with

```commandline
cp .env.example .env
# populate the KAGGLE USER and TOKEN
docker compose up
```
