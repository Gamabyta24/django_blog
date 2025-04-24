build:
	./build.sh

render-start:
	python create_superuser.py
	gunicorn django_blog.wsgi

install:
	uv sync

.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py migrate

start:
	python manage.py runserver
