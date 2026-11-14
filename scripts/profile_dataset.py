#!/usr/bin/env python3
"""
Reproducible first-pass profile for the PhishVN CSV.
Run from the project root: python scripts/profile_dataset.py
Outputs a report to reports/dataset_profile.txt.
This script does not open or visit any URL contained in the dataset.
"""
from pathlib import Path
import csv
from collections import Counter
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "project" / "data" / "dataset_url.csv"
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)
REPORT_PATH = REPORT_DIR / "dataset_profile.txt"

rows = 0
header = []
null_counts = Counter()
label_counts = Counter()
tier_counts = Counter()
source_counts = Counter()
date_values = []
duplicate_urls = 0
seen_urls = set()
url_col = None

def is_missing(value):
    return value is None or value.strip().lower() in {"", "na", "n/a", "null", "none", "nan"}

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames or []
    for row in reader:
        rows += 1
        for key in header:
            if is_missing(row.get(key, "")):
                null_counts[key] += 1
        if "label" in row:
            label_counts[row["label"].strip()] += 1
        if "tier" in row:
            tier_counts[row["tier"].strip()] += 1
        if "source" in row:
            source_counts[row["source"].strip()] += 1
        if row.get("collected_at", "").strip():
            date_values.append(row["collected_at"].strip())
        # Use the literal URL column if present; do not normalise silently.
        for candidate in ("url", "URL", "url_original", "url_norm"):
            if candidate in row and row[candidate].strip():
                url_col = candidate
                break
        if url_col:
            raw = (row.get(url_col) or "").strip()
            if raw:
                if raw in seen_urls:
                    duplicate_urls += 1
                else:
                    seen_urls.add(raw)

def parse_date(s):
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None

parsed_dates = [parse_date(x) for x in date_values]
valid_dates = [x for x in parsed_dates if x is not None]
file_size = CSV_PATH.stat().st_size

lines = [
    "PhishVN — first-pass dataset profile",
    "===================================",
    f"File: {CSV_PATH.relative_to(ROOT)}",
    f"File size: {file_size:,} bytes ({file_size / (1024**2):.2f} MiB)",
    f"Rows: {rows:,}",
    f"Columns: {len(header)}",
    "Columns: " + ", ".join(header),
    "",
    "Label counts:",
]
lines += [f"  {k or '[blank]'}: {v:,}" for k, v in label_counts.most_common()]
lines += ["", "Tier counts:"]
lines += [f"  {k or '[blank]'}: {v:,}" for k, v in tier_counts.most_common()]
lines += ["", "Source counts:"]
lines += [f"  {k or '[blank]'}: {v:,}" for k, v in source_counts.most_common()]
lines += ["", "Missing values by column (top 20):"]
lines += [f"  {k}: {v:,} ({v / rows:.1%})" for k, v in null_counts.most_common(20)] if rows else []
lines += ["", f"Exact duplicate count in selected URL column ({url_col or 'not found'}): {duplicate_urls:,}"]
if valid_dates:
    lines += [f"Valid collected_at dates: {len(valid_dates):,}"]
    lines += [f"Min collected_at: {min(valid_dates).isoformat()}"]
    lines += [f"Max collected_at: {max(valid_dates).isoformat()}"]
else:
    lines += ["No parseable collected_at dates found."]
lines += [
    "",
    "Notes:",
    "- Missing values treat blank, NA, N/A, null, none and nan as missing.",
    "- Duplicate count is exact-string duplicates only, not URL-normalised duplicates.",
    "- Date min/max use parseable collected_at values only.",
    "- Review this report before making claims; inspect schema/docs and verify column semantics.",
]
REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Saved report: {REPORT_PATH}")
print(f"Rows={rows:,}; columns={len(header)}; size={file_size:,} bytes ({file_size/(1024**2):.2f} MiB)")
