#!/usr/bin/env python3
"""Step 3b: Prepare classification batches and write final classified output.

This script does two things:
1. Reads candidates + website text and outputs them in batches for classification
2. After classification data is provided, writes the final classified CSV

Usage:
  python3 classify_candidates.py dump    # Dump all candidates for classification
  python3 classify_candidates.py write   # Write final CSV from classifications.jsonl
"""

import csv
import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
INPUT_FILE = os.path.join(DATA_DIR, "yc_candidates_with_text.csv")
CLASSIFICATIONS_FILE = os.path.join(DATA_DIR, "classifications.jsonl")
OUTPUT_FILE = os.path.join(DATA_DIR, "yc_agent_infra_classified.csv")


def dump_for_classification():
    """Print all candidates in a format suitable for batch classification."""
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    batch_size = 25
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        print(f"\n{'='*80}")
        print(f"BATCH {i // batch_size + 1} (companies {i+1}-{min(i+batch_size, len(rows))})")
        print(f"{'='*80}")
        for j, row in enumerate(batch):
            name = row.get("name", "?")
            batch_name = row.get("batch", "?")
            url = row.get("website", "?")
            one_liner = row.get("one_liner", "")
            text = row.get("extracted_text", "")[:800]
            status = row.get("fetch_status", "?")
            print(f"\n--- {i+j+1}. {name} [{batch_name}] ---")
            print(f"URL: {url}")
            print(f"YC: {one_liner}")
            if text and status in ("OK", "OK_RETRY"):
                print(f"Site: {text[:500]}")
            elif status == "EMPTY_RESPONSE":
                print("Site: [JS-rendered, no text extracted]")
            else:
                print(f"Site: [{status}]")


def write_classified():
    """Read classifications from JSONL and merge with candidate data."""
    # Read original candidates
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = {row["name"]: row for row in reader}

    # Read classifications
    classifications = {}
    with open(CLASSIFICATIONS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                classifications[data["name"]] = data

    print(f"Read {len(rows)} candidates, {len(classifications)} classifications")

    # Merge
    out_fields = [
        "name", "batch", "website", "one_liner", "current_description",
        "classification", "layer", "notes", "relevance_score"
    ]

    results = []
    for name, row in rows.items():
        cl = classifications.get(name, {})
        results.append({
            "name": name,
            "batch": row.get("batch", ""),
            "website": row.get("website", ""),
            "one_liner": row.get("one_liner", ""),
            "current_description": cl.get("current_description", ""),
            "classification": cl.get("classification", "UNCLASSIFIED"),
            "layer": cl.get("layer", ""),
            "notes": cl.get("notes", ""),
            "relevance_score": row.get("relevance_score", ""),
        })

    # Sort: AGENT-INFRA-DIRECT first, then ADJACENT, then AS-PRODUCT, then rest
    order = {"AGENT-INFRA-DIRECT": 0, "AGENT-INFRA-ADJACENT": 1, "AGENT-AS-PRODUCT": 2, "NOT-RELEVANT": 3, "UNCLASSIFIED": 4}
    results.sort(key=lambda r: (order.get(r["classification"], 5), -int(r.get("relevance_score", 0) or 0)))

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(results)

    # Summary
    counts = {}
    for r in results:
        cl = r["classification"]
        counts[cl] = counts.get(cl, 0) + 1

    print(f"\nClassification breakdown:")
    for cl, count in sorted(counts.items(), key=lambda x: order.get(x[0], 5)):
        print(f"  {cl}: {count}")
    print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 classify_candidates.py [dump|write]")
        sys.exit(1)

    if sys.argv[1] == "dump":
        dump_for_classification()
    elif sys.argv[1] == "write":
        write_classified()
    else:
        print(f"Unknown command: {sys.argv[1]}")
