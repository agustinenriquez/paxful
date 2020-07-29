How to install & use:

    - Build and run:
        docker-compose up -d
        docker-compose logs -f web

    - Run migrations and destroy container
        docker-compose run --rm web python manage.py makemigrations
        docker-compose run --rm web python manage.py migrate

    - Start a bash inside the container:
        docker-compose run --rm web bash

    - Create a user:
        http post http://0.0.0.0:8000/users/ username=testuser password=testuser email=testuser@gmail.com
