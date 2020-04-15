#!/usr/bin/env python3.7

"""Fetch configuration from HALON and save as JSON"""

import argparse
import base64
import json
from datetime import datetime, timezone

import requests


def main() -> None:
    """Main functions"""

    parser = argparse.ArgumentParser(description="Save HALON config")
    parser.add_argument(
        "--config",
        metavar="filename",
        required=False,
        help="Config file",
        default="halon-save-config.json",
    )
    parser.add_argument(
        "--output", metavar="filename", required=False, help="Output file"
    )
    args = parser.parse_args()

    # read configuration
    with open(args.config) as input_file:
        config = json.load(input_file)

    halon_url = f"https://{config['hostname']}/api/1.0.0"

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

    # archive configurations
    archive_path = config.get("archive_path", ".")
    output_filename = (
        args.output or f"{archive_path}/halon-config-{last_halon_revision}.json"
    )
    with open(output_filename, "wt") as f:
        f.write(json.dumps(last_halon_config, indent=4))


if __name__ == "__main__":
    main()
