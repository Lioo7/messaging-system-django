FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc graphviz libgraphviz-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Run collectstatic during container build
RUN python manage.py collectstatic --noinput

# Entrypoint script to create superuser
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Specify the entry point script to run on container start
ENTRYPOINT ["/code/entrypoint.sh"]
