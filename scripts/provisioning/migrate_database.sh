#!/bin/bash
set -e

if
    test -z "$APP_PATH" ||
    test -z "$VIRTUAL_ENV_PATH"
then
    >&2 echo "APP_PATH and VIRTUAL_ENV_PATH env variable must be defined"
    exit 1
fi

cd "$APP_PATH"
source "$VIRTUAL_ENV_PATH"/bin/activate

# Ensure that MySQL is running in strict mode
mysql --user="root" --host="$ADE_BDD_SVR" "$ADE_BDD_NAM" --password="$MYSQL_ROOT_PASSWORD" --execute='set global SQL_MODE="STRICT_ALL_TABLES";'

# the migrations assume the database is in utf8
mysql --user="$ADE_BDD_USR" --host="$ADE_BDD_SVR" "$ADE_BDD_NAM" --password="$ADE_BDD_PWD" --execute='ALTER DATABASE `'"$ADE_BDD_NAM"'` CHARACTER SET utf8 COLLATE utf8_unicode_ci'

python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'vanves')" | python manage.py shell
