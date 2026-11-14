#!/usr/bin/env python3
"""Reproducible data-quality checks for the PhishVN URL table.
Run from project root: py scripts/quality_checks.py
The script never opens or visits URLs and never modifies source data.
"""
import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "project" / "data" / "dataset_url.csv"
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)
REPORT_FILE = REPORT_DIR / "quality_checks.txt"


def is_missing(value):
    return value is None or value.strip().lower() in {"", "na", "n/a", "null", "none", "nan"}


def parse_date(value):
    value = (value or "").strip()
    if not value:
        return None
    for fmt in (
        "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def canonical_host_key(value):
    """Host-level key: strips URL user-info, fragment and default port.

    This is for collision review only. It is NOT proof that rows are duplicates.
    """
    value = (value or "").strip()
    if not value:
        return ""
    try:
        parts = urlsplit(value)
        scheme = parts.scheme.lower()
        host = (parts.hostname or "").lower()
        if not host:
            return value
        try:
            port = parts.port
        except ValueError:
            return value
        netloc = host
        if port is not None and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
            netloc += f":{port}"
        return urlunsplit((scheme, netloc, parts.path or "/", parts.query, ""))
    except Exception:
        return value


rows = 0
header = []
missing = Counter()
labels = Counter()
tiers = Counter()
sources = Counter()
exact_seen = set()
exact_repeats = 0
host_groups = defaultdict(list)
dates = []
with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames or []
    for line_no, row in enumerate(reader, start=2):
        rows += 1
        for col in header:
            if is_missing(row.get(col, "")):
                missing[col] += 1
        labels[(row.get("label") or "").strip()] += 1
        tiers[(row.get("tier") or "").strip()] += 1
        sources[(row.get("source") or "").strip()] += 1
        date_value = row.get("collected_at", "")
        parsed = parse_date(date_value)
        if parsed:
            dates.append(parsed)
        raw_url = (row.get("url") or "").strip()
        if raw_url:
            if raw_url in exact_seen:
                exact_repeats += 1
            exact_seen.add(raw_url)
            key = canonical_host_key(raw_url)
            if key:
                host_groups[key].append((line_no, raw_url, row.get("label", ""), row.get("tier", ""), row.get("source", "")))

host_repeat_occurrences = sum(len(v)-1 for v in host_groups.values() if len(v)>1)
collision_groups = [(k,v) for k,v in host_groups.items() if len(v)>1]
file_size = CSV_FILE.stat().st_size
lines = [
    "PhishVN — quality checks", "========================",
    f"File: {CSV_FILE.relative_to(ROOT)}",
    f"File size: {file_size:,} bytes ({file_size / (1024**2):.2f} MiB)",
    f"Rows: {rows:,}", f"Columns: {len(header)}",
    "", "Label counts:",
]
lines += [f"  {k or '[blank]'}: {v:,}" for k,v in labels.most_common()]
lines += ["", "Tier counts:"]
lines += [f"  {k or '[blank]'}: {v:,}" for k,v in tiers.most_common()]
lines += ["", "Source counts:"]
lines += [f"  {k or '[blank]'}: {v:,}" for k,v in sources.most_common()]
lines += ["", "Missing values by column:"]
lines += [f"  {k}: {v:,} ({v / rows:.1%})" for k,v in missing.most_common()] if rows else []
lines += ["", f"Exact duplicate URL occurrences: {exact_repeats:,}",
          f"Parseable collected_at values: {len(dates):,}"]
if dates:
    lines += [f"Minimum parsed collected_at: {min(dates).date().isoformat()}", f"Maximum parsed collected_at: {max(dates).date().isoformat()}"]
lines += [f"Host-level collision groups after conservative canonicalisation: {len(collision_groups):,}",
          f"Repeated occurrences across those host-level groups: {host_repeat_occurrences:,}",
          "", "Interpretation notes:",
          "- Missing values treat blank, NA, N/A, null, none and nan as missing.",
          "- Date parsing supports ISO formats and day/month/year values in the source.",
          "- Host-level canonicalisation strips URL user-info before @, fragments and default ports; this can group different URL strings by host.",
          "- A host-level collision is not proof of a duplicate record. Review context and keep the raw source unchanged.",
          "- No URL was opened or visited; this script only parses URL strings."]
for key, group in collision_groups:
    lines += ["", f"Collision key: {key}"]
    for line_no, url, label, tier, source in group:
        lines += [f"  line {line_no}: {url} | label={label} | tier={tier} | source={source}"]
REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Report saved to: {REPORT_FILE}")
print(f"Rows={rows:,}; columns={len(header)}; size={file_size:,} bytes ({file_size/(1024**2):.2f} MiB)")
print(f"Exact duplicate URL occurrences: {exact_repeats:,}")
print(f"Host-level collision groups: {len(collision_groups):,}; repeated occurrences: {host_repeat_occurrences:,}")
if dates:
    print(f"Parseable collected_at dates: {len(dates):,}; range: {min(dates).date()} to {max(dates).date()}")
