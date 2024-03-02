# Scripts

```bash

# Run RabbitMQ
docker-compose up

# Run Celery Worker
./venv/bin/celery -A DRF worker -l DEBUG -c 1 -Q celery -n main

# Run Celery Beat
 ./venv/bin/celery -A DRF beat -l DEBUG

```