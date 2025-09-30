#!/bin/sh
set -e

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
until nc -z db 5432; do
  sleep 2
done

echo "Postgres is up - initializing DB"
python app/init_db.py

echo "Starting app"
exec python app/main.py
