#!/usr/bin/env python3.7

"""Deploy certificate to Halon"""

import base64
import json
from datetime import datetime, timezone

import requests

# read configuration
with open("halon-deploy-cert.json") as input_file:
    config = json.load(input_file)

timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S%z")
halon_url = f"https://{config['hostname']}/api/1.0.0"

# read cert & key
with open(config["certfile"]) as cert_file:
    pki_certdata = cert_file.read()
with open(config["keyfile"]) as key_file:
    pki_keydata = key_file.read()

# construct new PKI parameters
pki_key = f"pki__{config['pki_key']}"
pki_params = [
    f"{config['certname']} (certbot {timestamp})",
    "x509+privatekey",
    base64.b64encode((pki_certdata + pki_keydata).encode()).decode(),
]

# create session for Halon
session = requests.Session()
session.auth = (config["username"], config["password"])
if "cacert" in config:
    session.verify = config["cacert"]

# fetch configuration from Halon
response = session.get(f"{halon_url}/config/revisions/HEAD")
response.raise_for_status()

# digest current configuration
last_halon_config = response.json()
last_halon_revision = last_halon_config["id"]

# prepare new configuration
next_halon_config = {}
next_halon_revision = last_halon_revision + 1
next_halon_config["message"] = f"certbot {timestamp}"
next_halon_config["config"] = []

# update new configuration
for c in last_halon_config["config"]:
    paramset = c.copy()
    if paramset["name"] == pki_key:
        paramset["params"] = pki_params
    next_halon_config["config"].append(paramset)

# deploy configuration
if config.get("deploy", False):
    response = session.post(
        f"{halon_url}/config/revisions/{next_halon_revision}", json=next_halon_config
    )
    response.raise_for_status()
else:
    print(json.dumps(next_halon_config, indent=4))
