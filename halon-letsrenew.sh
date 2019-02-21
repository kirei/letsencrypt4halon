#!/bin/bash

CERTBOT="certbot -q"

EMAIL=
HOSTNAME=

. `dirname $0`/`basename $0 .sh`.conf

CERT=/etc/letsencrypt/live/${HOSTNAME}/fullchain.pem
KEY=/etc/letsencrypt/live/${HOSTNAME}/privkey.pem
FLAGFILE=/etc/letsencrypt/live/${HOSTNAME}/deployed


if [ ! -d /etc/letsencrypt/accounts ]; then
	$CERTBOT register --agree-tos --email $EMAIL
	touch $CERTFILE
fi
if [ ! -f $CERT ]; then
	$CERTBOT certonly -d $HOSTNAME --standalone
else
	$CERTBOT renew --reuse-key --cert-name $HOSTNAME --standalone
fi

if [ ! -f $CERT -o ! -f $KEY ]; then
	echo "Missing certificate/key"
	exit 1
fi

if [ ! -f $FLAGFILE -o $CERT -nt $FLAGFILE ]; then
	(cd /etc/letsencrypt; ./halon-deploy-cert.py)
	touch $FLAGFILE
fi
