create-env-file:
	echo "Create .env file (update if necessary)"
	cp .env.example .env

install-local: create-env-file
	echo "Installing precommits"
	pip install -r requirements/dev.txt
	pre-commit install
	pre-commit install --hook-type commit-msg

	echo "Create docker images"
	docker compose build

test-local:
	docker compose -f docker-compose.dev.yml run --rm api bash scripts/test_coverage.sh
	sed -i 's\<source>/app</source>\<source>{{ cookiecutter.project_slug }}</source>\g' coverage/coverage.xml

test:
	docker compose -f docker-compose.pipeline.yml up --build -d
	docker compose -f docker-compose.pipeline.yml exec -ti django_test bash scripts/test_coverage.sh
	docker cp {{ cookiecutter.project_slug }}_test:/home/backend/coverage ./coverage
	docker compose -f docker-compose.pipeline.yml down -t 1 --volumes --rmi local

clean:
	docker compose -f docker-compose.pipeline.yml down -t 1 
	docker compose -f docker-compose.dev.yml down -t 1 
	docker compose -f docker-compose.yml down -t 1 

rmvolumes:
	docker compose -f docker-compose.pipeline.yml down -t 1 --volumes --rmi local
	docker compose -f docker-compose.dev.yml down -t 1 --volumes --rmi local
	docker compose -f docker-compose.yml down -t 1 --volumes --rmi local

build:
	docker compose -f docker-compose.dev.yml build

run:
	docker compose -f docker-compose.dev.yml up -d

logs:
	docker compose -f docker-compose.dev.yml logs -f --tail 100

rerun: clean run logs

restart:
	docker compose -f docker-compose.dev.yml restart -t 1 api 

exec:
	docker compose -f docker-compose.dev.yml exec -ti api bash

shell:
	docker exec -ti {{ cookiecutter.project_slug }}_api python manage.py shell_plus

debug-web:
	docker exec -ti {{ cookiecutter.project_slug }}_api madbg connect

migrations:
	docker exec -ti {{ cookiecutter.project_slug }}_api python manage.py makemigrations
