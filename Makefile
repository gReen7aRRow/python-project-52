install:
    poetry install
lint:
    poetry run flake8
test:
    poetry run coverage run --source '.' manage.py test
coverage:
    poetry run coverage xml
run:
	poetry run python3 manage.py runserver
migrate:
    poetry run python3 manage.py migrate
