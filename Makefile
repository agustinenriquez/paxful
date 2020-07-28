runserver:
	python manage.py runserver
migrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
shell_plus:
	python manage.py shell_plus
flake:
	flake8 .
tests:
	pytest
testusers:
	pytest rest/tests/user_tests.py
clean-python:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -r -f {} \;
djangosettings:
	export DJANGO_SETTINGS_MODULE=paxful.settings
showurls:
	python manage.py show_urls
celery:
	celery -A paxful worker -l info
