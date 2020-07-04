#!/bin/sh

set -e

until PGPASSWORD=$DATABASE_PASSWORD psql -h $DATABASE_HOST -U $DATABASE_USER -c '\q' > /dev/null 2>&1; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done

until nc -z ${RABBITMQ_HOST} 5672 > /dev/null 2>&1; do
    echo "RabbitMQ is unavailable - sleeping"
    sleep 1
done

echo "Executing the flask db upgrade"
python3 /code/src/manage.py db upgrade -d /code/src/api/migrations

exec "$@"