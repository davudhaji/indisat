FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code

RUN apt-get update && apt-get install -y \
  locales \
  locales-all \
  build-essential \
  libpq-dev \
  libjpeg-dev \
  binutils \
  libproj-dev \
  gdal-bin \
  libxml2-dev \
  libxslt1-dev \
  zlib1g-dev \
  libffi-dev \
  wkhtmltopdf \
  libssl-dev

COPY mime.types /etc/mime.types

RUN mkdir ${APP_ROOT}
COPY . ${APP_ROOT}
WORKDIR ${APP_ROOT}

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN python manage.py collectstatic --noinput