#!/bin/bash
#
# Author: Sakthi Santhosh
# Created on: 16/10/2023
cp ./nginx/$1.conf /etc/nginx/sites-available/default

if [ "$1" == "maintenance" ]; then
  cp ./nginx/maintenance/index.html /var/www/html/
fi
