# Multistaged build to prevent reinstall the packages everytime
# it's more ecological #greenIT #NICE !
FROM python:3.12-slim-bullseye AS base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN apt-get update && \
    apt-get install -y nano vim build-essential  && \
    apt-get clean

FROM base as pip-installed

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


FROM pip-installed AS code

# run as rootless
RUN adduser --disabled-password --gecos '' backend
USER backend
COPY --chown=backend:backend {{ cookiecutter.project_slug }} ./home/backend/app
WORKDIR /home/backend/app
EXPOSE 8000

CMD ["bash", "./scripts/gunicorn.sh"]
