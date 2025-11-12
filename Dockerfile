# build stage
FROM python:3.12 AS builder
ENV PYTHONUNBUFFERED=1


# install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# set up a python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install all the python packages needed
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip pipenv && \
    pipenv requirements > requirements.txt && \
    pip install -r requirements.txt

# runtime stage
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1

# install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# duplicate the virtual environment from the builder
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY src .

RUN chmod +x /app/entry_main.sh

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./entry_main.sh"]
