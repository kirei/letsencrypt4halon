#!/bin/bash

CERTBOT="certbot -q"

EMAIL=
MX_HOSTNAME=

SPG_HOSTNAME=
SPG_USERNAME=
SPG_PASSWORD=

. `dirname $0`/`basename $0 .sh`.conf

CERT=/etc/letsencrypt/live/${MX_HOSTNAME}/fullchain.pem
KEY=/etc/letsencrypt/live/${MX_HOSTNAME}/privkey.pem

FLAGFILE=/etc/letsencrypt/live/${MX_HOSTNAME}/deployed
TIMESTAMP=`date --rfc-3339=seconds`
COMMENT="${MX_HOSTNAME} (certbot ${TIMESTAMP})"


if [ ! -d /etc/letsencrypt/accounts ]; then
	$CERTBOT register --agree-tos --email $EMAIL
	touch $CERTFILE
fi
if [ ! -f $CERT ]; then
	$CERTBOT certonly -d $MX_HOSTNAME --standalone
else
	$CERTBOT renew --reuse-key --cert-name $MX_HOSTNAME --standalone
fi

if [ ! -f $CERT -o ! -f $KEY ]; then
	echo "Missing certificate/key"
	exit 1
fi

if [ ! -f $FLAGFILE -o $CERT -nt $FLAGFILE ]; then
	echo "Cert updated, deployment needed."
fi

