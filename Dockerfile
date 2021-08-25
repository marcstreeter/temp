FROM python:3.9.5-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/usr/src/scripts:${PATH}"
ARG environment=development
ENV PYTHONPATH=/usr/src/app

WORKDIR /usr/src

COPY scripts ./scripts
COPY app ./app
COPY requirements ./requirements

RUN chmod +x ./scripts/*
RUN pip install --no-cache-dir -r requirements/${environment}.txt

WORKDIR /usr/src/app

CMD [ "entrypoint.sh" ]