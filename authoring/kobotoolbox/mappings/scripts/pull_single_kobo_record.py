#!/usr/bin/env python3
"""
Pull raw KoboToolbox JSON and extract a target metadata record.

Default example:
- Form: gaia_metadata_authoring_form_v2
- Record ID: 136

Outputs:
- records/raw/record_<id>_raw.json
- records/raw/record_<id>_keys.txt

Environment variables:
- KOBO_API_TOKEN
- KOBO_SERVER_URL optional, defaults to https://kf.kobotoolbox.org
"""

import argparse
import json
import os
from getpass import getpass
from pathlib import Path

import requests


def find_repo_root(start_path: Path | None = None) -> Path:
    """Find the Git repository root by walking upward until .git is found."""
    start_path = Path(start_path or Path.cwd()).resolve()

    for path in [start_path, *start_path.parents]:
        if (path / ".git").exists():
            return path

    raise RuntimeError("Could not find repository root. Run this script from inside the Git repo.")


def get_json(url: str, headers: dict, timeout: int = 60) -> dict:
    """GET a URL and return parsed JSON."""
    response = requests.get(url, headers=headers, timeout=timeout)
    print(f"GET {response.url} -> {response.status_code}")
    response.raise_for_status()
    return response.json()


def fetch_paginated_results(start_url: str, headers: dict) -> list[dict]:
    """Fetch all paginated results from a Kobo v2 API endpoint."""
    results = []
    next_url = start_url

    while next_url:
        payload = get_json(next_url, headers=headers)
        results.extend(payload.get("results", []))
        next_url = payload.get("next")

    return results


def get_record_id(record: dict) -> str | None:
    """Return the legacy/control ID from a Kobo record."""
    candidate_keys = [
        "control_group/id",
        "id",
        "ID",
        "dataset_id",
        "record_id",
    ]

    for key in candidate_keys:
        value = record.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pull raw KoboToolbox JSON and extract one metadata record."
    )

    parser.add_argument(
        "--form-name",
        default="gaia_metadata_authoring_form_v2",
        help="Kobo form name to search for.",
    )

    parser.add_argument(
        "--record-id",
        default="136",
        help="Record ID to extract from control_group/id.",
    )

    parser.add_argument(
        "--server-url",
        default=os.getenv("KOBO_SERVER_URL", "https://kf.kobotoolbox.org"),
        help="KoboToolbox server URL.",
    )

    args = parser.parse_args()

    repo_root = find_repo_root()
    kobo_dir = repo_root / "authoring" / "kobotoolbox"

    raw_dir = kobo_dir / "records" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    target_record_file = raw_dir / f"record_{args.record_id}_raw.json"
    target_record_keys_file = raw_dir / f"record_{args.record_id}_keys.txt"

    api_token = (os.getenv("KOBO_API_TOKEN") or getpass("Paste Kobo API token: ")).strip()

    if not api_token:
        raise ValueError("No Kobo API token provided.")

    headers = {
        "Authorization": f"Token {api_token}",
        "Accept": "application/json",
    }

    print("Repository root:")
    print(repo_root)

    print("\nRaw record output:")
    print(target_record_file)

    print("\nFetching Kobo forms/assets...")
    assets_url = f"{args.server_url.rstrip('/')}/api/v2/assets/"
    assets = fetch_paginated_results(assets_url, headers=headers)

    target_asset = None
    target_form_name = args.form_name.strip().lower()

    for asset in assets:
        asset_name = asset.get("name", "").strip().lower()
        if asset_name == target_form_name:
            target_asset = asset
            break

    if target_asset is None:
        available_names = sorted([a.get("name", "") for a in assets if a.get("name")])
        print("\nAvailable form names:")
        for name in available_names:
            print("-", name)
        raise ValueError(f"Could not find a form named '{args.form_name}'")

    print(f"\nFound form: {target_asset.get('name')}")
    print(f"UID: {target_asset.get('uid')}")
    print(f"Data endpoint: {target_asset.get('data')}")

    data_url = target_asset.get("data")
    if not data_url:
        raise ValueError("The target Kobo form does not have a data endpoint.")

    print("\nFetching submissions...")
    submissions = fetch_paginated_results(data_url, headers=headers)
    print(f"Total submissions retrieved: {len(submissions)}")

    target_record = None

    for record in submissions:
        if get_record_id(record) == str(args.record_id):
            target_record = record
            break

    if target_record is None:
        found_ids = [get_record_id(record) for record in submissions]
        found_ids = [x for x in found_ids if x is not None]

        print("\nIDs found:")
        print(found_ids[:50])

        raise ValueError(f"No raw JSON record found for ID {args.record_id}")

    with open(target_record_file, "w", encoding="utf-8") as f:
        json.dump(target_record, f, indent=2, ensure_ascii=False)

    record_keys = sorted(target_record.keys())

    with open(target_record_keys_file, "w", encoding="utf-8") as f:
        for key in record_keys:
            f.write(key + "\n")

    print(f"\nSaved raw JSON record for ID {args.record_id} to:")
    print(target_record_file.resolve())

    print("\nSaved record key list to:")
    print(target_record_keys_file.resolve())

    print("\nQuick check:")
    print("Record ID:", get_record_id(target_record))
    print("Title:", target_record.get("dublin_core_group/title"))
    print("DOI:", target_record.get("dublin_core_group/doi"))

    description = str(target_record.get("dublin_core_group/description", ""))
    print("Description preview:", description[:300])

    print("\nNext step:")
    print(
        "Run 03_kobo_to_jsonld.py with --wrap-key datasets "
        "to generate the JSON-LD output."
    )


if __name__ == "__main__":
    main()
