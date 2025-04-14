## Fake Migrations

When we manually apply certain database schema change operations, we can use this powerful fake migration to get
our database and Django migration system back in sync. Only apply fake migrations when the database schema is the same
as the existing Django model definition.

```shell
# make a migration
python manage.py makemigrations [<app_name>] 

# Fake a migration
python manage.py migrate [<app_name>] [<migration_name>] --fake 
```

## Reverse Migrations

Migrations can be reversed with migrate by passing the number of the previous migration.

```shell
# Reverse a migration 0003
python manage.py migrate [<app_name>] 0002

# If you want to reverse all migrations applied for an app, use the name zero
python manage.py migrate <app_name> zero
```
