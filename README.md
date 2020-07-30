How to install & use:

    - Build and run:
        docker-compose up -d
        docker-compose logs -f web

    - Run migrations and destroy container
        docker-compose run --rm web python manage.py makemigrations
        docker-compose run --rm web python manage.py migrate

    - Start a bash inside the container:
        docker-compose run --rm web bash

    - Create paxul platform object:
        python manage.py shell_plus
        Platform.objects.create(name="paxful")

    - Create superuser
        admin = User.objects.create_superuser(username="admin", password="admin123")

    - Create a user using httpie:
        http post http://0.0.0.0:8000/users/ username=testuser password=testuser email=testuser@gmail.com

    - Run tests:
        make tests or docker-compose run --rm web pytest

    - Documentation:
        http://localhost:8000/docs/
