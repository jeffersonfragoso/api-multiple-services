#!/bin/sh

set -e

until nc -z ${RABBITMQ_HOST} 5672 > /dev/null 2>&1; do
    echo "RabbitMQ is unavailable - sleeping"
    sleep 1
done

exec "$@"