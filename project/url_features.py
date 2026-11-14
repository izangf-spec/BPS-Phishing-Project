"""Feature definitions for the PhishVN URL model (Entrega 2).

Every model input is computed from the raw URL string by ``UrlFeatures``, so a
scikit-learn pipeline built on it accepts a raw URL and returns a prediction.

Exact definitions (checked against the development rows of ``data/dataset_url.csv``
in ``project-model.ipynb``, section 4):

- ``url_len``: number of characters of the URL after removing a leading scheme
  such as ``https://``. DEVIATION: the dataset column ``url_len`` counts the full
  string, scheme included (12,997 of 14,665 development rows agree).
- ``num_dots``: number of ``.`` characters in the whole URL (host, path and
  query). Matches the dataset column for 14,665 of 14,665 development rows.
- ``num_subdomains``: labels of the host minus the labels of its registrable
  domain, using the ICANN section of the Public Suffix List (PSL). Matches the
  dataset column for 14,631 of 14,665 development rows; the 34 differences (33
  of them ``.vn`` hosts) are reported in the notebook.
- ``has_at``: 1 if ``@`` appears anywhere in the URL string, else 0. Only 3 URLs
  in the development rows contain ``@``, so this input is almost constant.
- ``has_ip``: 1 if the host is an IPv4 or IPv6 literal. It is 0 in every row of
  the dataset and is not a model input.
- ``tld``: last label of the host, not the public suffix (``x.gov.vn`` -> ``vn``).
  Matches the dataset column for 14,665 of 14,665 development rows.
- ``registrable_full``: registrable domain under the full PSL (ICANN and PRIVATE
  sections). Used only to build cross-validation and temporal groups.

The PSL file is stored in ``psl/`` and its SHA-256 is checked on every load.
Nothing is downloaded at run time.
"""
import hashlib
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd
from publicsuffixlist import PublicSuffixList
from sklearn.base import BaseEstimator, TransformerMixin

PSL_PATH = Path(__file__).resolve().parent / "psl" / "public_suffix_list.dat"
PSL_SHA256 = "c0c17430faf1d0edb352e165dd3e5e6dfe890b1305cf548e20a572e8c46ff399"
PSL_VERSION = "2026-11-11_17-18-20_UTC"
PSL_COMMIT = "529030148729033bc6c30dbb05753b805a7d2155"

SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*://", re.IGNORECASE)
IPV4 = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
MODEL_INPUTS = ("url_len", "num_dots", "num_subdomains", "has_at")


@lru_cache(maxsize=2)
def load_psl(only_icann: bool) -> PublicSuffixList:
    """Load the pinned Public Suffix List. Raises if the file was altered."""
    digest = hashlib.sha256(PSL_PATH.read_bytes()).hexdigest()
    if digest != PSL_SHA256:
        raise ValueError(f"PSL checksum mismatch: {digest}")
    with open(PSL_PATH, encoding="utf-8") as fh:
        return PublicSuffixList(fh, only_icann=only_icann)


def _host(url: str) -> str:
    """Lower-cased host of a URL; empty string when the URL cannot be parsed."""
    try:
        parts = urlsplit(url if SCHEME.match(url) else "http://" + url)
        return (parts.hostname or "").lower()
    except ValueError:  # malformed netloc, e.g. unbalanced IPv6 brackets
        return ""


@lru_cache(maxsize=None)
def url_features(url: str) -> dict:
    """All candidate features for one raw URL (pure function, cached)."""
    host = _host(url)
    is_ip = bool(IPV4.match(host)) or ":" in host  # IPv4 literal or IPv6 literal
    num_subdomains, registrable_full = 0, host
    if host and not is_ip:
        registrable_icann = load_psl(True).privatesuffix(host)
        registrable_full = load_psl(False).privatesuffix(host) or host
        if registrable_icann:
            num_subdomains = max(len(host.split(".")) - len(registrable_icann.split(".")), 0)
    return {
        "url_len": len(SCHEME.sub("", url, count=1)),
        "num_dots": url.count("."),
        "num_subdomains": num_subdomains,
        "has_at": int("@" in url),
        "has_ip": int(is_ip),
        "tld": "" if (is_ip or not host) else host.rsplit(".", 1)[-1],
        "registrable_full": registrable_full,
    }


def features_frame(urls) -> pd.DataFrame:
    """Feature table for an iterable of raw URLs (one row per URL)."""
    return pd.DataFrame([url_features(str(u)) for u in urls])


class UrlFeatures(BaseEstimator, TransformerMixin):
    """Map a DataFrame with a ``url`` column to the requested feature columns."""

    def __init__(self, columns=("url_len", "num_dots", "num_subdomains", "has_at")):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        urls = X["url"] if isinstance(X, pd.DataFrame) else pd.Series(X)
        feats = features_frame(urls.tolist())
        return feats[list(self.columns)].reset_index(drop=True)

    def get_feature_names_out(self, input_features=None):
        return list(self.columns)
