# Common commands to habdle the project.
# ------------------------------------------------------------------------------
check:
	poetry run isort . --profile black
	poetry run black .
	poetry run mypy .
