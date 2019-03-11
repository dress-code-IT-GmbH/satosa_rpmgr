#!/bin/bash


scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APPHOME=$(dirname $scriptsdir)

python manage.py dumpdata > $APPHOME/database/database.json