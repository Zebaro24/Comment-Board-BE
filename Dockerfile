FROM python:3.13-slim AS build

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi --no-root

COPY . /app

FROM python:3.13-slim

WORKDIR /app

COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /app /app

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "Comment_Board_BE.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]