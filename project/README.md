# Deliverable 2: phishing URL model (PhishVN, `project/`)

**Question.** Can the URL string alone rank incoming URLs so that analysts review likely phishing first?

**Model.** Calibrated logistic regression (LR-B, C = 10, isotonic calibration) on four URL counts and the top-level domain. Threshold 0.22, chosen on development data only, from nested out-of-fold predictions.

**Test status.** The test set is **not** a clean holdout. An earlier version of this notebook read it and reported the same model and cost, and no independent sample exists in the repository. Section 8 of the notebook, and item T2 in `CHECKLIST_REQUISITOS.md`, state this.

**Read first:** `RESULTADOS_Y_METRICAS.md` (results and limits), `CHECKLIST_REQUISITOS.md` (status of each requirement) and `../INFORME_AUDITORIA_ENTREGA2.md` (audit report). The reasoning is in `project-model.ipynb`.

## Contents

| File | What it is |
|---|---|
| `project-model.ipynb` | The notebook, sections 0 to 13, with outputs saved from the final run: 58 cells (28 code, 30 Markdown), 0 errors, 2,477 Markdown words. |
| `model.joblib` | The final scikit-learn pipeline, from a raw `url` column to a probability (379,808 bytes). |
| `model_config.json` | Threshold, illustrative costs, seed, inputs, SHA-256 fingerprints of the model, feature code and Public Suffix List, and recorded demo predictions. |
| `url_features.py` | Feature code. `model.joblib` cannot be loaded without it. |
| `psl/public_suffix_list.dat` | Pinned Public Suffix List (version 2026-11-11_17-18-20_UTC). Its SHA-256 is checked on every load. |
| `figures/` | Eight charts, each as a static PNG (shown on GitHub) and an interactive Plotly HTML file. |
| `data/` | Dataset and publisher splits (`data/dataset_url.csv`, `data/splits/...`). Paths are relative to this folder. |
| `test_saved_model.py` | Independent check, run in a separate Python process (21 checks). |
| `requirements.txt` | Pinned package versions of the verified environment. |
| `count_markdown_words.py` | Counts the visible words of the Markdown cells. |
| `project-brief.md` | Deliverable 1: business problem, hypotheses, KPIs and references. |
| `CHECKLIST_REQUISITOS.md`, `RESULTADOS_Y_METRICAS.md` | Requirement status, and results with their limits. |

## Run from scratch

1. Use Python 3.13 and run `pip install -r requirements.txt`. `matplotlib` is included because the static PNG charts are drawn with it.
2. From this folder, execute the notebook. It rewrites `model.joblib`, `model_config.json` and `figures/`:

   ```bash
   jupyter nbconvert --to notebook --execute --inplace project-model.ipynb --ExecutePreprocessor.timeout=1500 --ExecutePreprocessor.kernel_name=python3
   ```

   The final run took 279 s of cell computation (under 5 minutes). `random_state` is 42 everywhere, and two runs gave identical outputs apart from the run-time lines.
3. Check the saved model in a separate process. This can be run from any folder:

   ```bash
   python test_saved_model.py
   ```

   Exit code 0 means all 21 checks passed.

The dataset is read from `data/dataset_url.csv`, a relative path.

## Load the model and score URLs

```python
import joblib
import pandas as pd

model = joblib.load("model.joblib")  # url_features.py and psl/ must be in the same folder
urls = pd.DataFrame({"url": ["http://demo-login.example/account"]})
prob = model.predict_proba(urls)[:, 1]
review_first = prob >= 0.22          # threshold from model_config.json
```

`review_first` sets analyst review priority. It is not an automatic block.

## Known behaviour

- **Malformed or empty input still receives a score.** In the test, `http://[bad` and an empty string both scored 0.915, the highest value in the check. Validate URLs before scoring; this must be in place before any deployment (block 4).
- **Trained on Vietnamese-context sources.** Results do not show performance on other regions, languages or current traffic.
- **The test set is newer than the training data.** All 487 test phishing URLs were first seen in 2023 to 2025; recall on the test set is 35 %, against 73 % in primary validation. See `RESULTADOS_Y_METRICAS.md`.

## Data

PhishVN Version 4 (Nguyen Vu, 2026), CC BY 4.0. Cite it as given in `../data_docs/CITATION.cff`. The publisher states that personal data are redacted.
