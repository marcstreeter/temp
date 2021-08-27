# API Example
example netflix api service 

# Endpoints
| VERB | URL                                        | DESCRIPTION            |
| ---- | ---                                        | -----------            |
| post | /system/initialize                         | populates server*      |
| get  | /system/status                             |                        |
| get  | /docs                                      | openapi schema         |
| get  | /movie                                     |                        |
| get  | /movie/{movie_id}                          |                        |
| get  | /movie/?[artist_id/country_id/rating_id]   |                        |
| get  | /show                                      |                        |
| get  | /category                                  |                        |
| get  | /artist                                    |                        |
| get  | /country                                   |                        |
*_NOTE_: present implementation takes ~30s to populate*

# Development Setup
Before making changes please initialize environment

```commandline
pip install -r requirements/development.txt
pre-commit install
```

# First Run
The database needs to be populated first. Run:

```commandline
docker compose up -d
curl -X "POST" "http://localhost:8081/initialize"
```