build:
	./build.sh

render-start:
	gunicorn django_blog.wsgi

install:
	uv sync

.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py migrate

start:
	python manage.py runserver
ruff:
    uv run ruff check .

ruff-fix:
    uv run ruff check . --fix
