#!/usr/bin/env python3
"""Validate a tailored resume .docx.

Checks:
  1. DASH CHECK  - FAIL on any em/en dash (and other unicode dash variants).
  2. FACT CHECK  - FAIL on any number in the resume that is absent from the source resume.
                   This is the zero-hallucination backstop: fabricated metrics get caught here.
  3. BANNED PHRASE CHECK - FAIL on any retired/forbidden claim listed in a banned-claims file.
  4. KEYWORD COVERAGE - report which top JD terms appear in the resume.

Usage:
  python validate_resume.py resume.docx --source source_resume.txt [--jd jd.txt] [--banned banned.txt]

The banned-claims file is one phrase per line; blank lines and lines starting with # are ignored.
Matching is case-insensitive and whitespace-normalized.

Exit code is non-zero if the dash, fact, or banned-phrase check fails, so it can gate a build.
"""
import argparse
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

BANNED_DASHES = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u2012": "figure dash",
    "\u2015": "horizontal bar",
    "\u2212": "minus sign",
}

STOPWORDS = set("""a an and or the of to in on for with at by from as is are be been being this
that these those you your we our they their it its will would should can could may might must
have has had do does did not no yes if then else when where who whom which what how why all any
each more most other some such than too very just also into out up down over under again further
about across after before during without within work role team teams help make made including
etc per based upon ability able""".split())


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    return " ".join(n.text for n in root.iter(f"{ns}t") if n.text)


def read_source(path):
    if path.lower().endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            root = ET.fromstring(z.read("word/document.xml"))
        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        return " ".join(n.text for n in root.iter(f"{ns}t") if n.text)
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def numbers(text):
    # Digit sequences with optional decimals; commas stripped so 3,500 == 3500.
    return set(re.findall(r"\d+(?:\.\d+)?", text.replace(",", "")))


def check_dashes(text):
    return [(name, text.count(ch)) for ch, name in BANNED_DASHES.items() if text.count(ch)]


def check_numbers(resume_text, source_text):
    r_nums = numbers(resume_text)
    s_nums = numbers(source_text)
    return sorted(r_nums - s_nums, key=lambda x: (len(x), x))


def normalize(text):
    return re.sub(r"\s+", " ", text).lower()


def check_banned(resume_text, banned_path):
    norm = normalize(resume_text)
    hits = []
    with open(banned_path, encoding="utf-8", errors="ignore") as f:
        for raw in f:
            phrase = raw.strip()
            if not phrase or phrase.startswith("#"):
                continue
            if normalize(phrase) in norm:
                hits.append(phrase)
    return hits


def derive_keywords(jd_text, top=40):
    words = re.findall(r"[A-Za-z][A-Za-z0-9+/.\-]{1,}", jd_text)
    freq = {}
    for w in words:
        lw = w.lower()
        if lw in STOPWORDS or len(lw) < 3:
            continue
        freq[lw] = freq.get(lw, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:top]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume")
    ap.add_argument("--source", help="source resume (.txt or .docx) for the fact-check")
    ap.add_argument("--jd", help="job-description text file")
    ap.add_argument("--banned", help="file of retired/forbidden claims, one phrase per line")
    args = ap.parse_args()

    text = docx_text(args.resume)
    failed = False

    print("=== DASH CHECK ===")
    hits = check_dashes(text)
    if hits:
        failed = True
        for name, n in hits:
            print(f"  FAIL: {n} x {name}")
    else:
        print("  PASS: no banned dashes.")

    if args.source:
        print("\n=== NUMERIC FACT CHECK (zero-hallucination) ===")
        src = read_source(args.source)
        extra = check_numbers(text, src)
        # Ignore trivial single digits that are usually formatting (1, 2, 3 in lists) only if you
        # want; here we report everything for full transparency.
        if extra:
            failed = True
            print(f"  FAIL: numbers in resume not found in source: {', '.join(extra)}")
            print("        Each must trace to the source or a candidate-confirmed fact.")
        else:
            print("  PASS: every number in the resume appears in the source.")
    else:
        print("\n=== NUMERIC FACT CHECK ===\n  SKIPPED: pass --source to enable the fact-check.")

    if args.banned:
        print("\n=== BANNED PHRASE CHECK (retired claims) ===")
        hits = check_banned(text, args.banned)
        if hits:
            failed = True
            for h in hits:
                print(f"  FAIL: retired claim present: {h}")
        else:
            print("  PASS: no retired claims found.")

    if args.jd:
        with open(args.jd, encoding="utf-8", errors="ignore") as f:
            jd = f.read()
        low = text.lower()
        kws = derive_keywords(jd)
        present = [k for k in kws if k in low]
        missing = [k for k in kws if k not in low]
        print("\n=== JD KEYWORD COVERAGE (top terms) ===")
        print(f"  Present ({len(present)}): {', '.join(present)}")
        print(f"  Missing ({len(missing)}): {', '.join(missing)}")
        print("  Missing terms are candidates for HONEST inclusion or gaps to flag, never fabrication.")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
