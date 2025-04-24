build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py migrate

start:
	python manage.py runserver