# Mizzle

A data logger for a WXT530 weather station.

## Database setup

Use psql to to create a database:

    psql -U postgres -h <hostname>
    CREATE DATABASE mizzle;
    \c mizzle

Export the postgres connection string

    export POSTGRES_URL='postgresql://postgres:<password>@<hostname>/mizzle'