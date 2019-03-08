#!/usr/bin/env python3

import json
import requests
import base64
from datetime import datetime, timezone



# read configuration
with open('halon-save-config.json') as input_file:
    config = json.load(input_file)

halon_url = f"https://{config['hostname']}/api/1.0.0"

# create session for Halon
session = requests.Session()
session.auth = (config['username'], config['password'])
if 'cacert' in config:
    session.verify = config['cacert']

# fetch configuration from Halon
response = session.get(f"{halon_url}/config/revisions/HEAD")
response.raise_for_status()

# digest current configuration
last_halon_config = response.json()
last_halon_revision = last_halon_config['id']

# archive configurations
archive_path = config.get('archive_path', '.')
with open(f"{archive_path}/halon-config-{last_halon_revision}.json", "wt") as f:
    f.write(json.dumps(last_halon_config, indent=4))
