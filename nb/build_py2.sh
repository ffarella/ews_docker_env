#!/bin/bash
#
tag=$(date --iso-8601 |  sed  's/-//g')
LOGFILE=../nb_py2_$tag.log
echo "$(date): Starting build" > $LOGFILE
docker build --rm --force-rm --tag ewsconsulting/nb_py2:latest --file Dockerfile_py2 . | tee -a $LOGFILE
echo "$(date): Finished" >> $LOGFILE 2>&1