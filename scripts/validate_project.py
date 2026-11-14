#!/usr/bin/env python3
"""Lightweight project-package validation. Run from the project root."""
import csv, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, condition, detail):
    checks.append((name, bool(condition), detail))

required=[
    'README.md','DATASET_SOURCE.txt','.gitignore','project/data/dataset_url.csv',
    'project/data/splits/url_train.csv','project/data/splits/url_val.csv','project/data/splits/url_test.csv',
    'data_docs/docs/schema.md','data_docs/docs/datasheet.md','data_docs/docs/data_sources.md',
    'data_docs/LICENSE','data_docs/CITATION.cff','project/project-brief.md',
    'scripts/profile_dataset.py','scripts/quality_checks.py','scripts/inspect_duplicates.py',
    'reports/dataset_profile.txt','reports/quality_checks.txt','reports/duplicate_inspection.txt','data_docs/PROJECT_DATA_NOTES.md','data_docs/docs/tranco_join_plan.md'
]
for rel in required: check(f'File exists: {rel}', (ROOT/rel).is_file(), rel)
with (ROOT/'project/data/dataset_url.csv').open('r',encoding='utf-8-sig',newline='') as f:
    reader=csv.reader(f); header=next(reader); rows=sum(1 for _ in reader)
check('Main dataset rows', rows==53116, f'{rows:,} rows')
check('Main dataset columns', len(header)==29, f'{len(header)} columns')
check('Dataset size', (ROOT/'project/data/dataset_url.csv').stat().st_size==11263539, f"{(ROOT/'project/data/dataset_url.csv').stat().st_size:,} bytes")
brief=(ROOT/'project/project-brief.md').read_text(encoding='utf-8')
check('Brief includes dataset card', 'Dataset-card field' in brief, 'dataset card heading/table')
check('Brief includes architecture diagram', '```mermaid' in brief and 'flowchart' in brief, 'Mermaid flowchart present')
check('Brief includes hypotheses', all(x in brief for x in ['H1 —','H2 —','H3 —']), '3 hypotheses found')
check('Brief includes KPIs', '### KPIs' in brief, 'KPI section present')
check('Brief includes Harvard references', '## References (Harvard style)' in brief and 'Nguyen Vu, T. (2026)' in brief and 'Vu, T.N. (2026a)' not in brief and 'Vu, 2026b' not in brief, 'References section present')
check('Second source and join method identified', 'Second-source join plan' in brief and 'tranco_join_plan.md' in (ROOT/'README.md').read_text(encoding='utf-8'), 'Tranco domain join is explicitly planned, not falsely claimed as complete')
check('KPI formulas and trade-offs', 'TP/(TP+FP)' in brief and 'false-positive' in brief.lower(), 'Classifier formulas and operational trade-off present')
check('AI assistance disclosed', 'AI-use acknowledgement' in brief and 'Generative AI assisted' in (ROOT/'README.md').read_text(encoding='utf-8'), 'Disclosure present in brief and README')
check('Hypotheses prioritised', 'priority by decision value' in brief.lower(), 'Priorities stated')
check('Architecture alternatives and risks', 'simpler than hosting a custom web app' in brief and 'Key risks' in brief, 'Alternative and main risks described')
# Main prose word count excludes dataset card and reference list; architecture code is not prose.
body=re.sub(r'## 1\. Dataset selection and dataset card.*?\*\*Eligibility decision\.\*\*.*?\n\n## 2\. Business problem','## 2. Business problem',brief,flags=re.S)
body=re.sub(r'```mermaid.*?```','',body,flags=re.S)
body=re.sub(r'## References \(Harvard style\).*','',body,flags=re.S)
word_count=len(re.findall(r"\b[\w'-]+\b",body))
check('Brief prose word count',800<=word_count<=1500,f'{word_count} words excluding dataset card, diagram code and references')
report_lines=['PROJECT VALIDATION','==================']
for name,ok,detail in checks:
    report_lines.append(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}")
failed=sum(not ok for _,ok,_ in checks)
report_lines.append(f"\nResult: {len(checks)-failed}/{len(checks)} checks passed")
report_path=ROOT/'reports'/'project_validation.txt'
report_path.parent.mkdir(exist_ok=True)
report_path.write_text('\n'.join(report_lines)+'\n',encoding='utf-8')
print('\n'.join(report_lines))
print(f'Validation report saved to: {report_path}')
sys.exit(1 if failed else 0)
