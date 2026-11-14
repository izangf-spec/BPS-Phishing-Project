"""Independent check of the saved model, meant to run in a fresh Python process.

Run from any directory:  python /path/to/project/test_saved_model.py

The script does not import the notebook. It checks, in order:
1. SHA-256 fingerprints of model.joblib, url_features.py and the Public Suffix
   List against model_config.json (the files were not altered after saving);
2. that the required package versions match requirements.txt;
3. that the pipeline loads and reproduces the probabilities recorded for the
   two fictitious demo URLs (tolerance 1e-6);
4. that probabilities lie in [0, 1] and decisions use the configured threshold;
5. that malformed or empty inputs return finite probabilities instead of
   raising an error.

Exit code 0 means every check passed; 1 means at least one failed.
"""
import hashlib
import json
import math
import sys
from importlib import metadata
from pathlib import Path

HERE = Path(__file__).resolve().parent
# url_features.py must be importable, because the pickled pipeline refers to it.
sys.path.insert(0, str(HERE))

import joblib  # noqa: E402
import pandas as pd  # noqa: E402

import url_features as uf  # noqa: E402

FAILURES = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_requirements():
    for line in (HERE / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "==" not in line:
            continue
        name, pinned = line.split("==", 1)
        try:
            installed = metadata.version(name)
        except metadata.PackageNotFoundError:
            installed = "not installed"
        check(f"requirement {name}=={pinned}", installed == pinned, f"installed {installed}")


def main():
    cfg = json.loads((HERE / "model_config.json").read_text(encoding="utf-8"))

    # 1. Fingerprints
    check("model.joblib SHA-256 matches model_config.json",
          sha256(HERE / "model.joblib") == cfg["model_sha256"])
    check("url_features.py SHA-256 matches model_config.json",
          sha256(HERE / "url_features.py") == cfg["url_features_sha256"])
    psl_path = HERE / "psl" / "public_suffix_list.dat"
    check("Public Suffix List SHA-256 matches model_config.json and url_features.py",
          sha256(psl_path) == cfg["psl_sha256"] == uf.PSL_SHA256)

    # 2. Dependencies
    check_requirements()

    # 3. Reload and reproduce the recorded demo predictions
    model = joblib.load(HERE / "model.joblib")
    demo = pd.DataFrame({"url": list(cfg["demo_expected"].keys())})
    proba = model.predict_proba(demo)[:, 1]
    for url, p in zip(demo["url"], proba):
        expected = cfg["demo_expected"][url]
        check(f"demo probability for {url}", abs(float(p) - expected) < 1e-6,
              f"got {float(p):.6f}, recorded {expected:.6f}")

    # 4. Range and decision rule
    check("probabilities lie in [0, 1]", bool(((proba >= 0) & (proba <= 1)).all()))
    thr = cfg["threshold"]
    flags = [int(float(p) >= thr) for p in proba]
    recorded_flags = [int(cfg["demo_expected"][u] >= thr) for u in demo["url"]]
    check("reloaded decisions equal the decisions implied by the recorded probabilities",
          flags == recorded_flags, f"threshold {thr}, flags {flags}")
    check("configured inputs can be computed from raw URL strings",
          set(cfg["inputs"]) <= set(uf.features_frame(demo["url"]).columns))

    # 5. Robustness to malformed input
    odd = pd.DataFrame({"url": ["http://[bad", "", "http://192.168.0.1/login", "https://ünïcode.example/路径"]})
    odd_proba = model.predict_proba(odd)[:, 1]
    check("malformed or unusual URLs give finite probabilities",
          all(math.isfinite(float(p)) and 0 <= float(p) <= 1 for p in odd_proba),
          ", ".join(f"{float(p):.3f}" for p in odd_proba))

    print()
    print(f"Python {sys.version.split()[0]} | executable {sys.executable}")
    print("RESULT:", "ALL CHECKS PASSED" if not FAILURES else f"{len(FAILURES)} CHECK(S) FAILED")
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
