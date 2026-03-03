#!/usr/bin/env python3
"""Step 3a: Bulk fetch candidate websites and extract text content."""

import httpx
import csv
import os
import re
import time
from html import unescape

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
INPUT_FILE = os.path.join(DATA_DIR, "yc_candidates.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "yc_candidates_with_text.csv")
TEXT_DIR = os.path.join(DATA_DIR, "website_texts")
CHECKPOINT_EVERY = 25
DELAY_SECONDS = 0.5
MAX_TEXT_IN_CSV = 2000
MAX_TEXT_IN_FILE = 5000


def extract_text_from_html(html):
    """Extract visible text from HTML without external dependencies."""
    # Remove script and style blocks
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    # Remove SVG blocks
    text = re.sub(r'<svg[^>]*>.*?</svg>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    # Replace block-level tags with newlines
    text = re.sub(r'<(?:p|div|br|h[1-6]|li|tr|td|th|section|article|header|footer|nav|main)[^>]*>', '\n', text, flags=re.IGNORECASE)
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode HTML entities
    text = unescape(text)
    # Collapse whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def fetch_website(client, url):
    """Fetch a website and return (status, extracted_text)."""
    if not url or url.strip() == "":
        return "NO_URL", ""

    # Ensure URL has scheme
    if not url.startswith("http"):
        url = "https://" + url

    try:
        resp = client.get(url)
        if resp.status_code == 200:
            text = extract_text_from_html(resp.text)
            if len(text.strip()) < 50:
                return "EMPTY_RESPONSE", text
            return "OK", text[:MAX_TEXT_IN_FILE]
        elif resp.status_code in (403, 401):
            return f"BLOCKED_{resp.status_code}", ""
        elif resp.status_code >= 500:
            # Retry once for server errors
            time.sleep(1)
            resp2 = client.get(url)
            if resp2.status_code == 200:
                text = extract_text_from_html(resp2.text)
                return "OK_RETRY", text[:MAX_TEXT_IN_FILE]
            return f"SERVER_ERROR_{resp.status_code}", ""
        else:
            return f"HTTP_{resp.status_code}", ""
    except httpx.TimeoutException:
        return "TIMEOUT", ""
    except httpx.ConnectError:
        # Retry once
        try:
            time.sleep(1)
            resp = client.get(url)
            text = extract_text_from_html(resp.text)
            return "OK_RETRY", text[:MAX_TEXT_IN_FILE]
        except Exception:
            return "CONNECTION_ERROR", ""
    except Exception as e:
        return f"ERROR_{type(e).__name__}", ""


def main():
    os.makedirs(TEXT_DIR, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        candidates = list(reader)
        fieldnames = reader.fieldnames

    print(f"Read {len(candidates)} candidates from {INPUT_FILE}")

    # Prepare output fieldnames
    out_fields = list(fieldnames) + ["fetch_status", "extracted_text"]

    client = httpx.Client(
        timeout=httpx.Timeout(10.0, connect=5.0),
        follow_redirects=True,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )

    results = []
    status_counts = {}
    skipped = 0

    for i, row in enumerate(candidates):
        slug = row.get("slug", f"company_{i}")
        txt_path = os.path.join(TEXT_DIR, f"{slug}.txt")

        # Resume support: skip if already fetched
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                existing_text = f.read()
            row["fetch_status"] = "CACHED"
            row["extracted_text"] = existing_text[:MAX_TEXT_IN_CSV]
            results.append(row)
            skipped += 1
            continue

        url = row.get("website", "")
        status, text = fetch_website(client, url)

        # Track status
        status_counts[status] = status_counts.get(status, 0) + 1

        # Save full text to file
        if text:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

        row["fetch_status"] = status
        row["extracted_text"] = text[:MAX_TEXT_IN_CSV]
        results.append(row)

        # Progress
        if (i + 1) % 10 == 0:
            print(f"  Fetched {i + 1}/{len(candidates)} ({status}): {row.get('name', '?')}")

        # Checkpoint
        if (i + 1) % CHECKPOINT_EVERY == 0:
            _write_csv(OUTPUT_FILE, out_fields, results)
            print(f"  Checkpoint saved at {i + 1}")

        time.sleep(DELAY_SECONDS)

    client.close()

    # Final write
    _write_csv(OUTPUT_FILE, out_fields, results)

    print(f"\nDone! Fetched {len(candidates) - skipped} sites ({skipped} cached)")
    print("Status breakdown:")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"  {status}: {count}")
    print(f"\nWritten to {OUTPUT_FILE}")


def _write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
