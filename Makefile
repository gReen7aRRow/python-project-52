install:
    poetry install
task_manager:
    poetry run task_manager
lint:
    poetry run flake8 task_manager
    poetry run flake8 tests
