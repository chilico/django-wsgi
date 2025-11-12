# django-wsgi

## Overview

This is a Django repo for bootstrapping projects running the WSGI server.

It may act as a template to get a dockerised async Django backend setup quickly.

## Architecture

- Docker
- Gunicorn (WSGI)
- Django
- Django Rest Framework
- Pytest
- Loguru

## Setup

### Prerequisites

1. Install Docker Desktop
2. Install pipenv globally:

```bash
brew install pipx
pipx install pipenv
pipx ensurepath
```

### Environment

Copy required env vars:

```sh
cp .env.example .env
```

Set your variables accordingly:

1. `DJANGO_PROJECT_NAME`
   Set your Django project name by replace this value (default `project`).

IMPORTANT: Do not change this value after first spinning up Docker; a new project will be created with `django-admin startproject ${DJANGO_PROJECT_NAME}` if the named project directory and its settings file do not exist. Alternatively, hardcode your preferred name and remove all instances of the var (recommended for more established projects).

2. `DEBUG`
   Set `DEBUG=1` for development (default `1`). This is both for Django dev and to direct uvicorn to reload file changes.

3. `WORKERS`
   Sets the number of worker instances for gunicorn to use when not in dev (default `1`).

### Build & run containers

```sh
docker compose build
docker compose up
```

Use `ctrl+c` in the terminal running the containers to shutdown and exit.

### Testing

This setup uses `pytest` rather that Django's built in test framework. I find it has a cleaner syntax and parametrisation is a big win.

A separate test database volume and docker compose file are used to run tests. This makes clear separation of test and development databases, and mirrors how tests ought to be run in production. To run tests, use the `docker-compose.test.yml`:

```sh
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

Or use the helper script (see next).

### Helpers

There are executable scripts found in the root level `bin`.

- `collectstatic`: refreshes Django's static files
- `makemigrations`: makes Django migrations, excepts args (see script for usage)
- `migrate`: runs migrations
- `test`: runs tests

Run these from root like a command, e.g.:

```sh
bin/test
```

Feel free to add to and/or pair back this setup to your heart's content.

Made by @chilico
