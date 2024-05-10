# Django Template

## Using Makefile

For convenience all needed commands to run the project are structured into a Makefile
You need to install it first

Linux : sudo apt install make

MacOS: brew install make

Windows : https://stackoverflow.com/a/32127632


You also need docker to be installed on your host machine. Here are some instructions :

Linux : https://docs.kawa-infra.fr/docker/

Windows : https://docs.docker.com/desktop/wsl/

MacOS : https://docs.docker.com/desktop/install/mac-install/

### Get started with Makefile

- Git clone this project into your local computer.

- First create a virtual env for your project. `python3 -m venv .venv` will create a virtual env named .venv in your project directory.

- Install the development dependencies with `make install-local`. This will create the appropriate .env file desgined to work locally, install pre-commits and pip install the packages

- To run the project : `make run` Your application will be available in 127.0.0.1:8000

- To see logs of the project : `make logs`, you may want to see only api logs with `docker compose logs -f --tail 100 api`

- To enter the container run : `make exec`

- To run tests you can run `make test-local`

- You can have a django shell available (sometimes usefull for debug) with `make shell`

- To stop the containers you can run `make clean`

- A lot of time you will want to restart the application (when you change a .env variable or for debugging purpose) you can run `make rerun` which will do `make clean, make run and make logs` all at once

- To create a new migration file run `make migrations` then `make rerun`. Migrations are applied when the container is started.

Congrats ! Your project is correctly configured !

## Get started (without Makefile)

Get env vars and edit them.
`cp .env.example .env && nano .env`

For local development, you can fire the postgres database easily 
`docker compose -f docker-compose.dev.yml up -d`

Don't forget to update the .env accordingly (127.0.0.1 on local, "postgres" (container_name) on server)
```bash

# database access credentials
DJANGO_DB_PASSWORD=password
DJANGO_DB_PORT=5432
DJANGO_DB_USER=postgres
DJANGO_DB_NAME=mydatabase
DJANGO_DB_HOST=db

# SUPERUSER
DJANGO_SU_NAME=Admin
DJANGO_SU_EMAIL=admin@gmail.com    
DJANGO_SU_PASSWORD=admin123456
```

Run migrations
`cd /{{ cookiercutter.project_slug }} && python manage.py migrate && python manage.py runserver` 

Got to `127.0.0.1:8000` to see your awesome django website
You can connect on admin with the superuser provided 

Enjoy building your website ! 


## Github Workflow 

Don't forget to add your secrets in github actions /settings/secrets/actions

## Nginx conf 

Don't forget to update nginx.conf and nginx.dev.conf with your domain.
A DNS "A" Record should be pointing to your ip address too.

## Certbot 

Use certbot to get a certificate :

- Update the nginx.conf with this simple configuration first

```bash
server {
    listen 80;
    server_name example.org;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

}
```

- Restart the nginx service to apply configuration : `docker compose restart nginx`

- Then launch a dry run to test the connection on your VPS. Failed attemps can be due to firewall/ports or permission issues (unlikely). Replace the last parameter with the one you put on the nginx.conf file

`docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org` 

- Then to get your certficate and pem files : 

`docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d example.org` 

- You can put the nginx.conf back and restart restart nginx again : `docker compose restart nginx`

- You can even automate the renewal process by adding a cron job every once in a while : `0 1 * * * docker compose run --rm certbot renew` (Everyday at 1am)
