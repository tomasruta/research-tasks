#!/usr/bin/env python3
"""Step 1: Fetch all YC companies from target batches via the yc-oss API."""

import httpx
import csv
import json
import os
import time

API_BASE = "https://yc-oss.github.io/api/batches"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "yc_companies_raw.csv")

# Try multiple slug formats per desired batch
BATCH_SLUGS = [
    "w26", "winter-2026",
    "f25", "fall-2025",
    "x25", "spring-2025",
    "s25", "summer-2025",
    "w25", "winter-2025",
    "f24", "fall-2024",
    "s24", "summer-2024",
    "w24", "winter-2024",
]

FIELDS = [
    "name", "slug", "one_liner", "long_description", "website",
    "batch", "industry", "subindustry", "tags", "team_size",
    "status", "stage"
]


def fetch_batch(client, slug):
    """Fetch companies for a given batch slug. Returns list of dicts or None."""
    url = f"{API_BASE}/{slug}.json"
    try:
        resp = client.get(url)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            return None
        else:
            print(f"  Warning: {slug} returned HTTP {resp.status_code}")
            return None
    except Exception as e:
        print(f"  Error fetching {slug}: {e}")
        return None


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    all_companies = {}  # keyed by slug for deduplication
    batch_counts = {}

    client = httpx.Client(timeout=15.0, follow_redirects=True)

    for slug in BATCH_SLUGS:
        print(f"Trying batch slug: {slug}...", end=" ")
        companies = fetch_batch(client, slug)
        if companies is None:
            print("not found (404)")
            continue

        print(f"found {len(companies)} companies")
        for co in companies:
            co_slug = co.get("slug", "")
            if co_slug and co_slug not in all_companies:
                all_companies[co_slug] = co
                batch_name = co.get("batch", slug)
                batch_counts[batch_name] = batch_counts.get(batch_name, 0) + 1

    client.close()

    # Write CSV
    print(f"\nTotal unique companies: {len(all_companies)}")
    print("Batch breakdown:")
    for batch, count in sorted(batch_counts.items()):
        print(f"  {batch}: {count}")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for co in all_companies.values():
            # Convert tags list to semicolon-separated string
            row = {}
            for field in FIELDS:
                val = co.get(field, "")
                if isinstance(val, list):
                    val = "; ".join(str(v) for v in val)
                elif val is None:
                    val = ""
                row[field] = val
            writer.writerow(row)

    print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
