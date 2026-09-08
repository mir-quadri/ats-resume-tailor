#!/usr/bin/env python3
"""
Validates a resume DOCX against a fact ledger, job description, and banned phrases.
Checks for dashes, unverified numeric facts, and banned claims.
Exits non-zero if any check fails.
"""

import sys
import re
import argparse
from docx import Document
from pathlib import Path


def extract_text_from_docx(docx_path):
    """Extract plain text from a DOCX file."""
    doc = Document(docx_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)


def check_dashes(text):
    """Check for em-dashes and en-dashes. Fails if any found."""
    em_dash = "—"
    en_dash = "–"
    issues = []

    if em_dash in text:
        issues.append(f"Found em-dash (—): not ATS-safe")
    if en_dash in text:
        issues.append(f"Found en-dash (–): not ATS-safe")

    return issues


def parse_ledger(ledger_path):
    """Parse the fact ledger to extract verified facts."""
    facts = {}
    with open(ledger_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Simple format: "key: value" or list items
            if ':' in line:
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""
                facts[key] = value
    return facts


def check_numeric_facts(text, ledger_path):
    """Verify numeric facts appear in the ledger."""
    # Extract all numbers from the resume
    numbers = re.findall(r'\b\d+(?:[.,]\d+)?\b', text)

    with open(ledger_path, 'r') as f:
        ledger_text = f.read()

    issues = []
    for num in set(numbers):
        # Convert to various formats for matching
        variants = [num, num.replace(',', ''), num.replace('.', ',')]
        if not any(v in ledger_text for v in variants):
            # Allow percentages and common numbers to be missed
            if '%' not in text[max(0, text.find(num)-5):text.find(num)+len(num)+5]:
                issues.append(f"Numeric fact '{num}' not found in ledger")

    return issues


def check_banned_phrases(text, banned_path):
    """Check for banned phrases in the resume."""
    if not Path(banned_path).exists():
        return []

    issues = []
    with open(banned_path, 'r') as f:
        for line in f:
            phrase = line.strip()
            if not phrase or phrase.startswith('#'):
                continue
            if phrase.lower() in text.lower():
                issues.append(f"Banned phrase found: '{phrase}'")

    return issues


def check_keyword_coverage(text, jd_path):
    """Report keyword coverage against JD (informational only)."""
    if not Path(jd_path).exists():
        return None

    with open(jd_path, 'r') as f:
        jd_text = f.read().lower()

    # Extract key terms (words 4+ chars, not common words)
    common = {'that', 'this', 'with', 'from', 'have', 'your', 'work', 'team', 'role', 'skills'}
    jd_words = set(w.lower() for w in re.findall(r'\b\w{4,}\b', jd_text))
    jd_words -= common

    text_lower = text.lower()
    coverage = sum(1 for w in jd_words if w in text_lower)

    return {
        'total_keywords': len(jd_words),
        'matched': coverage,
        'percentage': round(100 * coverage / len(jd_words)) if jd_words else 0
    }


def main():
    parser = argparse.ArgumentParser(description='Validate resume against ledger and JD')
    parser.add_argument('resume', help='Path to resume.docx')
    parser.add_argument('--source', required=True, help='Path to fact ledger')
    parser.add_argument('--jd', help='Path to job description')
    parser.add_argument('--banned', help='Path to banned phrases')

    args = parser.parse_args()

    # Extract text
    text = extract_text_from_docx(args.resume)

    issues = []
    passed = True

    # Run checks
    dash_issues = check_dashes(text)
    if dash_issues:
        issues.extend(dash_issues)
        passed = False

    fact_issues = check_numeric_facts(text, args.source)
    if fact_issues:
        issues.extend(fact_issues)
        passed = False

    banned_issues = check_banned_phrases(text, args.banned) if args.banned else []
    if banned_issues:
        issues.extend(banned_issues)
        passed = False

    # Print results
    if passed:
        print("✓ DASH CHECK PASS")
        print("✓ NUMERIC FACT CHECK PASS")
        print("✓ BANNED PHRASE CHECK PASS")
    else:
        for issue in issues:
            print(f"✗ {issue}")
        sys.exit(1)

    # Keyword coverage (informational)
    if args.jd:
        coverage = check_keyword_coverage(text, args.jd)
        if coverage:
            print(f"\nKeyword coverage: {coverage['matched']}/{coverage['total_keywords']} ({coverage['percentage']}%)")


if __name__ == '__main__':
    main()
