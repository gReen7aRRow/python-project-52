install:
    poetry install

task_manager:
    poetry run task_manager

lint:
    poetry run flake8 task_manager

test:
    poetry run pytest

test-coverage:
    poetry run coverage run -m pytest
    poetry run coverage xml

run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate
