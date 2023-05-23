# Mizzle

A data logger for a WXT530 weather station.

## Database setup

Use psql to to create a database:

    psql -U postgres -h <hostname>
    CREATE DATABASE mizzle;
    \c mizzle
    \q

    psql -U postgres -h <hostname> -d mizzle < schema.sql

Export the postgres connection string

    export POSTGRES_URL='postgresql://postgres:<password>@<hostname>/mizzle'

## Load data from text files

```bash
find 2023 -type f -exec cat {} + | grep 'XDR' > ./mizzle.py
```
