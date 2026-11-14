#!/usr/bin/env python3
"""Inspect host-level URL collisions without visiting any URL or modifying data."""
import csv
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "project" / "data" / "dataset_url.csv"
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)
REPORT_FILE = REPORT_DIR / "duplicate_inspection.txt"

def canonical_host_key(value):
    value = (value or "").strip()
    if not value:
        return ""
    try:
        p = urlsplit(value)
        scheme = p.scheme.lower()
        host = (p.hostname or "").lower()
        if not host:
            return value
        try:
            port = p.port
        except ValueError:
            return value
        netloc = host
        if port is not None and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
            netloc += f":{port}"
        return urlunsplit((scheme, netloc, p.path or "/", p.query, ""))
    except Exception:
        return value

groups = defaultdict(list)
with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    for line_no, row in enumerate(csv.DictReader(f), start=2):
        url = (row.get("url") or "").strip()
        key = canonical_host_key(url)
        if key:
            groups[key].append({"line": line_no, "url": url, "label": row.get("label", ""), "tier": row.get("tier", ""), "source": row.get("source", ""), "id": row.get("id", "")})

collisions = [(key, records) for key, records in groups.items() if len(records) > 1]
lines = ["PhishVN — host-level URL collision inspection", "=============================================", "", "This is a review list, not a deduplication instruction.", "The canonical key strips URL user-info before @, fragments and default ports.", "URLs were not opened or visited."]
repeats = 0
for key, records in collisions:
    repeats += len(records)-1
    lines += ["", f"Collision key: {key}"]
    for r in records:
        lines += [f"  CSV line {r['line']}: {r['url']} | label={r['label']} | tier={r['tier']} | source={r['source']} | id={r['id']}"]
lines += ["", f"Collision groups: {len(collisions)}", f"Repeated occurrences beyond first row per group: {repeats}", "", "Decision: retain all source rows unless a later documented analysis step establishes a justified deduplication rule."]
REPORT_FILE.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Report saved to: {REPORT_FILE}")
print("\n".join(lines))
