#!/bin/bash

set -eo pipefail

if [[ "$WAIT_FOR_DB" == "yes" ]]
then
  while !</dev/tcp/$DATABASE_HOST/3306; do echo "Waiting for DB..." && sleep 1; done;
fi

if [[ "$ENVIRONMENT" == "PRODUCTION" ]]
then
  exec gunicorn main:serve -k uvicorn.workers.UvicornWorker --lifespan on --port 8000 --host 0.0.0.0
else
  exec uvicorn main:serve --reload --lifespan on --log-level debug --use-colors --port 8000 --host 0.0.0.0
fi
