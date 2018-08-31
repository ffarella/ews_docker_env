#!/bin/bash
#
tag=$(date --iso-8601 |  sed  's/-//g')
LOGFILE=../nb_py3_$tag.log
echo "$(date): Starting build" > $LOGFILE
docker build --rm --force-rm --tag ewsconsulting/nb_py3:latest --file Dockerfile_py3 . | tee -a $LOGFILE
echo "$(date): Finished" >> $LOGFILE 2>&1