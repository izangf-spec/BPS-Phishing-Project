# Planned enrichment: Tranco top-sites ranking

**Status: planned, not downloaded or joined in this project version.** The brief identifies this second source transparently; no ranking values are claimed as already joined.

## Source and reproducibility

- Source: https://tranco-list.eu/
- Archive one specific list snapshot and record the list ID, retrieval timestamp, downloaded filename, file checksum and applicable licence/terms.
- Keep the snapshot separate from the original PhishVN CSV; never overwrite raw source files.

## Join specification

1. Parse each URL as data only; do not visit it.
2. Extract the registrable domain with a public-suffix-aware library (rather than taking the last two labels, which fails for suffixes such as `co.uk`).
3. Normalise case and trailing dots; retain the original URL and derived join key.
4. Join left from PhishVN to the archived Tranco snapshot on registrable domain. Keep `tranco_list_id`, `tranco_snapshot_date`, and `tranco_rank`.
5. Before accepting the join, test that the selected snapshot has one rank per domain, count matched and unmatched rows, inspect collisions and record the match rate by label/source/tier.
6. Do not treat a missing match as malicious or a high rank as proof of safety. Compare ranks only within the same snapshot.
7. Because Tranco-derived benign records already exist in PhishVN, identify overlapping records and do not describe the join as independent validation. Do not use the enrichment to alter labels.

## Evaluation safeguards

- Keep all feature engineering fitted on training data where applicable.
- Preserve the publisher's group-aware train/validation/test split; do not randomly split rows after enrichment.
- Report results with and without the enrichment and check whether source membership becomes a shortcut feature.
- Add the snapshot, transformation code and results to the manifest before considering this join complete.
