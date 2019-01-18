#!/bin/bash
#Ment to be run as root after buildout is done. Will obtain cert and install on nginx debian

cd /etc/nginx
ln -s /home/voteit/srv/ssu_buildout/etc/nginx.conf ./sites-available/ssu.conf
cd sites-enabled
ln -s ../sites-available/ssu.conf

service nginx stop
certbot certonly --standalone -d ssu.voteit.se
service nginx start
