# Django Template

## Get started

Get env vars and edit them.
`cp .env.example .env && nano .env`

For local development, you can fire the postgres database easily 
`docker compose -f docker-compose.dev.yml up -d`

Don't forget to update the .env accordingly (127.0.0.1 on local, "postgres" (container_name) on server)
```bash
PGHOST=127.0.0.1

# database access credentials
ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
PGPORT=5432

# SUPERUSER
DJANGO_SU_NAME=Admin
DJANGO_SU_EMAIL=admin@gmail.com    
DJANGO_SU_PASSWORD=admin123456
```

Run migrations
`cd /app && python manage.py migrate && python manage.py runserver`

Got to `127.0.0.1:8000` to see your awesome django website
You can connect on admin with the superuser provided 

Enjoy building your website ! 




## Github Workflow 

Don't forget to add your secrets in github actions /settings/secrets/actions

## Nginx conf 

Don't forget to update nginx.conf and nginx.dev.conf with your domain.
A DNS "A" Record should be pointing to your ip address too.

## Certbot 

Use certbot to get a certificate first :

Update the docker-compose.yml with nginx.dev.conf first

```yaml
  nginx:
    image: nginx:alpine
    restart: always
    container_name: nginx
    volumes:
      - static_volume:/app/static
      - ./nginx.dev.conf:/etc/nginx/conf.d/default.conf # Here we use nginx.dev.conf
      - certbot_www:/var/www/certbot
      - certbot_conf:/etc/nginx/ssl/:ro
    depends_on:
      - django
    ports:
      - 80:80
      - 443:443
    networks:
      - backend
```
Then run a dry run to test the connection. Failed attemps can be due to firewall/ports or permission issues (unlikely). You must run this on your server

`docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org` 

Then to get your certficate an pem files : 
`docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d example.org` 

You can even automate the renewal process by adding a cron job every once in a while : `0 1 * * * docker compose run --rm certbot renew` (Everyday at 1am)
