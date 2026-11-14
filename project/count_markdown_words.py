import re, sys, json
nb = json.load(open(sys.argv[1], encoding="utf-8"))
total = 0
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "markdown":
        continue
    text = "".join(c["source"])
    lines = [l for l in text.splitlines() if not re.fullmatch(r"\s*\|?[\s:\-|]+\|?\s*", l)]
    words = [t for t in re.split(r"\s+", "\n".join(lines)) if re.search(r"[A-Za-z0-9]", t)]
    total += len(words)
    if len(words) >= 100:
        print(f"cell {i}: {len(words)} words")
print(f"TOTAL {total:,} words")
