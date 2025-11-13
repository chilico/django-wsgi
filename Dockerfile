# BUILD STAGE - install dependencies
FROM python:3.12 AS builder
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# set up python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install python packages
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip pipenv && \
    pipenv requirements > requirements.txt && \
    pip install -r requirements.txt

# RUNTIME STAGE - slim production image
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1

# install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# duplicate virtual environment from builder
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# copy source & make entry executable
WORKDIR /app
COPY src .
RUN chmod +x /app/entry_main.sh

# go
EXPOSE 8080
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./entry_main.sh"]
