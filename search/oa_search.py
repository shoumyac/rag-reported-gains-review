#!/usr/bin/env python3
"""OpenAlex search for the RAG reported-gains review.

Implements the query registered at https://doi.org/10.17605/OSF.IO/XGPCZ.

Usage:
    python search/oa_search.py count
    python search/oa_search.py harvest --out data/raw/openalex [--max-pages N]

The API key is read from the environment variable OPENALEX_API_KEY (or from a
local .env file). The key is sent as a Bearer token and is never written to disk
or to the run log.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.openalex.org/works"

# The query exactly as registered on OSF.
QUERY_REGISTERED = (
    '("retrieval-augmented generation" OR "retrieval augmented generation" '
    'OR "retrieval-augmented language model" OR "retrieval-augmented language models" '
    'OR "retrieval-augmented LLM" OR "retrieval-augmented large language model" '
    'OR ("RAG" AND (retrieval OR retriever OR "language model" OR LLM)))'
)
# Extended query, logged as deviation D1 in protocol/deviations_log.md (1 Nov 2026).
# It adds two clauses to the registered query and drops nothing.
QUERY_EXTENDED = (
    QUERY_REGISTERED[:-1]
    + ' OR "retrieval augmentation"'
    + ' OR ("retrieval-augmented" AND (language OR LLM OR LLMs OR generation OR generative)))'
)
QUERY = QUERY_EXTENDED
FROM_DATE = "2020-01-01"
TO_DATE = "2026-11-30"
LANGUAGE = "en"
TYPES = "article|preprint|conference-paper"

SELECT = ",".join([
    "id", "doi", "title", "display_name", "publication_year", "publication_date", "type",
    "language", "primary_location", "locations", "authorships", "cited_by_count",
    "is_retracted", "ids", "referenced_works", "abstract_inverted_index", "open_access",
])


def load_dotenv(path=".env"):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def build_filter(with_types=True):
    parts = [
        f"title_and_abstract.search:{QUERY}",
        f"from_publication_date:{FROM_DATE}",
        f"to_publication_date:{TO_DATE}",
        f"language:{LANGUAGE}",
    ]
    if with_types:
        parts.append(f"type:{TYPES}")
    return ",".join(parts)


def request(params, key, retries=5):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = resp.read()
            return url, body
        except urllib.error.HTTPError as err:
            if err.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError("unreachable")


def cmd_count(key):
    for with_types in (False, True):
        _, body = request({"filter": build_filter(with_types), "per-page": 1}, key)
        meta = json.loads(body)["meta"]
        label = "with types" if with_types else "no type filter"
        print(f"{label}: {meta['count']}")


def cmd_harvest(key, out_dir, max_pages):
    os.makedirs(out_dir, exist_ok=True)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cursor = "*"
    page = 0
    manifest = []
    total = None
    while cursor:
        page += 1
        if max_pages and page > max_pages:
            break
        params = {"filter": build_filter(True), "per-page": 200, "cursor": cursor, "select": SELECT}
        url, body = request(params, key)
        data = json.loads(body)
        total = data["meta"]["count"]
        name = f"page_{page:05d}.json.gz"
        path = os.path.join(out_dir, run_id + "_" + name)
        with gzip.open(path, "wb") as fh:
            fh.write(body)
        manifest.append({
            "file": os.path.basename(path),
            "sha256": hashlib.sha256(body).hexdigest(),
            "n_results": len(data["results"]),
            "request_url": url,
            "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        })
        cursor = data["meta"].get("next_cursor")
        if not data["results"]:
            break
        time.sleep(0.2)
    log = {
        "run_id": run_id,
        "query_variant": "registered" if QUERY == QUERY_REGISTERED else "extended",
        "filter": build_filter(True),
        "hit_count_reported": total,
        "pages_saved": len(manifest),
        "records_saved": sum(m["n_results"] for m in manifest),
        "pages": manifest,
    }
    log_path = os.path.join("search", "runs", f"openalex_{run_id}.json")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as fh:
        json.dump(log, fh, indent=2)
    print(f"saved {log['records_saved']} records in {log['pages_saved']} pages; log: {log_path}")


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    parser.add_argument("--query", choices=["registered", "extended"], default="extended",
                        help="registered = exact OSF query; extended = deviation D1 (default)")
    sub.add_parser("count")
    harvest = sub.add_parser("harvest")
    harvest.add_argument("--out", default="data/raw/openalex")
    harvest.add_argument("--max-pages", type=int, default=0)
    args = parser.parse_args()
    global QUERY
    QUERY = QUERY_REGISTERED if args.query == "registered" else QUERY_EXTENDED
    key = os.environ.get("OPENALEX_API_KEY")
    if not key:
        sys.exit("OPENALEX_API_KEY is not set")
    if args.cmd == "count":
        cmd_count(key)
    else:
        cmd_harvest(key, args.out, args.max_pages)


if __name__ == "__main__":
    main()
