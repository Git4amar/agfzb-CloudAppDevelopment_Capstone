#!/bin/bash

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations djangoapp
python manage.py migrate
#python manage.py collectstatic
# write code to export superuser crdentials as ENV variables in the container
./set_superuser.sh

echo "$@"
exec "$@"