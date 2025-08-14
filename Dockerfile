# Dockerfile
FROM python:3.11-slim

# system packages needed for building Python wheels and pillow
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential gcc libjpeg62-turbo-dev zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements first for layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# copy project files into image
COPY . /app

# ensure staticfiles dir exists
RUN mkdir -p /app/staticfiles

# Collect static files at build time (this will generate hashed/compressed files)
# NOTE: this can fail if STATICFILES_STORAGE is Manifest type and refs are missing
ENV DJANGO_SETTINGS_MODULE=mitsu.settings
RUN python manage.py collectstatic --noinput

# runtime env
ENV PYTHONUNBUFFERED=1

# expose the port that gunicorn will bind to (internal)
EXPOSE 8798

# NO ENTRYPOINT/CMD here — command will be provided in docker-compose
