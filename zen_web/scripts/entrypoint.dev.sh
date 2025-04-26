#! /bin/sh

if [ "$DATABASE_ENGINE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_DB_HOST $POSTGRES_DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

# The “$@” symbol indicates that every argument we pass into the container will be appended to the executable.
exec "$@"
