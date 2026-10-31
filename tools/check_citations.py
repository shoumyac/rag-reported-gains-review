#!/usr/bin/env python3
"""Check that every DOI in references.bib resolves and that the title matches.

Looks the DOI up in Crossref first and then in DataCite (for arXiv and other
DataCite DOIs). Fails (exit code 1) if a DOI does not resolve, if an entry has
no DOI, or if the registered title is not similar to the title in the bib file.

Usage: python tools/check_citations.py [references.bib]
"""
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "rag-reported-gains-review/0.1 (https://github.com/shoumyac/rag-reported-gains-review)"
THRESHOLD = 0.90


def norm(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def parse_bib(path):
    raw = open(path, encoding="utf-8").read()
    raw = "\n".join(line for line in raw.splitlines() if not line.lstrip().startswith("%"))
    entries = []
    for block in re.split(r"(?m)^@", raw)[1:]:
        key = re.match(r"\w+\{([^,]+),", block)
        fields = {}
        for name, val in re.findall(r"(?m)^\s*(\w+)\s*=\s*[{\"](.*?)[}\"],?\s*$", block):
            fields[name.lower()] = val.strip()
        entries.append((key.group(1) if key else "?", fields))
    return entries


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            if err.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise
    return None


def registered_title(doi):
    quoted = urllib.parse.quote(doi, safe="")
    data = fetch_json("https://api.crossref.org/works/" + quoted)
    if data:
        titles = data["message"].get("title") or []
        if titles:
            return titles[0], "crossref"
    data = fetch_json("https://api.datacite.org/dois/" + quoted)
    if data:
        titles = data["data"]["attributes"].get("titles") or []
        if titles:
            return titles[0]["title"], "datacite"
    return None, None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "references.bib"
    failures = 0
    entries = parse_bib(path)
    if not entries:
        print("no entries found")
        return 1
    for key, fields in entries:
        doi = fields.get("doi")
        if not doi:
            print(f"FAIL {key}: no DOI")
            failures += 1
            continue
        title, source = registered_title(doi)
        if not title:
            print(f"FAIL {key}: DOI {doi} did not resolve")
            failures += 1
            continue
        ratio = difflib.SequenceMatcher(None, norm(title), norm(fields.get("title", ""))).ratio()
        if ratio < THRESHOLD:
            print(f"FAIL {key}: title mismatch ({ratio:.2f}); registered: {title}")
            failures += 1
        else:
            print(f"ok   {key}: {doi} ({source}, title match {ratio:.2f})")
    print(f"{len(entries) - failures}/{len(entries)} entries verified")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
