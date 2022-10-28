install:
    poetry install
task_manager:
    poetry run task_manager
lint:
    poetry run flake8
test:
    poetry run pytest users/tests.py statuses/tests.py tasks/tests.py labels/tests.py
test-coverage:
    poetry run coverage run -m pytest
    poetry run coverage xml
run:
	poetry run python3 manage.py runserver
migrate:
	poetry run python3 manage.py migrate
