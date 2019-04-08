#!/bin/bash -e


main() {
    setup
    migrate
    #createsuperuser
}


setup() {
    local scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
    [[ -n "$APPHOME" ]] || APPHOME=$(dirname $scriptsdir)

    is_init_file="$CONFIGHOME/db_is_initialized"
    if [[ -e $is_init_file ]]; then
        echo 'database already initialized'
        exit 0
    fi
}


migrate() {
    # create schema and load initial data
    python $APPHOME/manage.py migrate
    local rc=$?
    if (( rc > 0 )); then
        echo "failed to create database schema, migrate returned with ${rc}"
        exit 1
    else
        echo 'Initial database migration complete'
        touch $is_init_file
    fi
}


createsuperuser() {
    [[ $DEFAULT_USER ]] || DEFAULT_USER="admin"
    [[ $DEFAULT_EMAIL ]] || DEFAULT_EMAIL="admin@local"
    [[ $DEFAULT_PASS ]] || DEFAULT_PASS="adminadmin"

    local rc=0
    echo "from django.contrib.auth.models import User; "\
         "User.objects.create_superuser('$DEFAULT_USER', "\
         "'$DEFAULT_EMAIL', '$DEFAULT_PASS')" |\
         $APPHOME/manage.py shell || rc=$?
    if ((rc>0)); then
        echo "manage.py createsuperuser failed with ${rc}"
        exit 1
    else
        echo 'DB superuser created'
    fi
}




main $@
