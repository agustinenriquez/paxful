runserver:
	docker-compose up -d
migrations:
	docker-compose run --rm web python manage.py makemigrations
migrate:
	docker-compose run --rm web python manage.py migrate
shell_plus:
	docker-compose run --rm web python manage.py shell_plus
flake:
	docker-compose run --rm web flake8 .
tests:
	docker-compose run --rm web pytest
clean-python:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -r -f {} \;
showurls:
	docker-compose run --rm web  python manage.py show_urls
