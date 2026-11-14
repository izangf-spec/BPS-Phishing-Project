# Local notes for this course project

- The selected main file is `project/data/dataset_url.csv`; its observed columns are listed in `reports/dataset_profile.txt`.
- The main CSV has 29 columns and does not contain an `is_https` field. The publisher's schema documentation mentions `is_https` in the CompPhish-aligned feature representation; if using `project/data/vn_compphish.csv`, follow the publisher's warning to exclude it from modelling.
- The main source CSV is retained unchanged. Scripts generate diagnostic reports only.
- Two host-level collision groups are reported because URL user-info before `@` is removed from the canonical host key. These are not automatically treated as duplicate records.
- `collected_at` uses day/month/year strings for many records; scripts parse that format as well as ISO dates.
