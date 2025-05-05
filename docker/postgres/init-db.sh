#!/bin/bash
set -e

# Creating multiple databases
for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
    echo "Creating database: $db"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOSQL
        CREATE DATABASE $db;
EOSQL
    echo "Initializing scheduled_jobs table in database: $db"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$db" -f /docker-entrypoint-initdb.d/scheduled_jobs.sql
done