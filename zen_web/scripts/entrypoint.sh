#! /bin/sh

if [ "$DATABASE_ENGINE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_DB_HOST $POSTGRES_DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

if [ "$RUN_MIGRATIONS" = 1 ]
then
    echo "Running migrations..."
    python manage.py migrate
fi

if [ "$RUN_COLLECTSTATIC" = 1 ]
then
    echo "Running collectstatic..."
    python manage.py collectstatic --noinput
fi
# The “$@” symbol indicates that every argument we pass into the container will be appended to the executable.
exec "$@"
