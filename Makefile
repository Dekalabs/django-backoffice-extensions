# Common commands to handle the project.
# ------------------------------------------------------------------------------
check:
	poetry run isort backoffice_extensions --profile black
	poetry run black backoffice_extensions
	poetry run mypy backoffice_extensions
