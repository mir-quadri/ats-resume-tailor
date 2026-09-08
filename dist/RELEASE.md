# ATS Resume Tailor v1.0

**Release Date:** September 8, 2026

## Overview

Complete implementation of the ATS Resume Tailor skill — a Claude Skill that rebuilds a resume for one specific job description with verified facts and four-persona review.

## What's Included

### Core Skill (SKILL.md)
The complete workflow and non-negotiable rules for:
- Assessing fit before writing anything
- Building a fact ledger and auditing for unverified claims
- Asking structured gap confirmation questions
- Picking a positioning lane and holding it
- Building an ATS-safe .docx
- Validating programmatically
- Reviewing as four personas (parser, recruiter, hiring manager, interviewer)

### Documentation (references/)
Eight comprehensive guides covering the skill's methodology:
- Fit assessment strategy
- Fact verification and zero-hallucination protocol
- Confirm-then-build process with structured questions
- Positioning lane discipline
- Company research and honest framing
- ATS parsing and reviewer strategy
- Four-persona review rubric
- Complete build-and-validate workflow

### Validation Tools (scripts/)
- **validate_resume.py**: Python validator checking dashes, numeric facts, and banned phrases
- **build_resume.js**: Node.js template for ATS-safe DOCX building

### Templates (assets/)
- Fact ledger template for transcribing verified facts
- Gap questions template with structured confirmation patterns

### Evaluation Suite (evals/)
Five test scenarios with 9 checks grading the skill's core behaviors:
- Ownership audit and flagged-for-confirmation lists
- Complete fit assessment with percentage and explicit calls
- Structured gap confirmation questions
- No resume content in the first turn (confirm-then-build discipline)
- Validator functionality (dashes, facts, banned phrases)

**Eval Status:** ✓ All 9 checks pass on first run

## Installation

### Claude App (web, desktop, mobile)
1. Unzip `ats-resume-tailor-v1.0.zip`
2. Go to Customize > Skills
3. Click "+", "Create skill", "Upload a skill"
4. Select the unzipped folder
5. Toggle the skill on

### Claude Code
```bash
mkdir -p ~/.claude/skills
unzip -d ~/.claude/skills/ats-resume-tailor ats-resume-tailor-v1.0.zip
claude [start a session]
```

The skill triggers on "tailor my resume", "is this job worth applying to", or when you paste a resume + job description.

## Key Features

**Zero hallucination:** Every fact traces to the source resume or explicit confirmation. Unverified claims are never promoted as strengths.

**Visible audit findings:** Ownership issues, scope language ambiguities, date gaps, and currency problems are written into a "flagged for confirmation" list that the candidate sees.

**Fit assessment first:** Before writing anything, the skill gives a plain read on fit with named strengths, gaps, a percentage, and an explicit recommendation (go/conditional/skip).

**Confirm then build:** Gap questions are structured and specific. The skill stops after the first turn and waits for answers before writing the resume.

**Four-persona review:** Every resume is reviewed as an ATS parser (keyword matching), recruiter (6-second skim), hiring manager (evidence-based assessment), and skeptical interviewer (can they defend every claim?).

## Requirements

- Node.js with the `docx` package (`npm install docx`)
- Python 3
- LibreOffice for PDF conversion (`soffice`)
- Poppler utilities (`pdftotext`, `pdftoppm`)

## Using the Validator Standalone

```bash
python3 scripts/validate_resume.py resume.docx \
  --source ledger.txt \
  --jd jd.txt \
  --banned banned.txt
```

Exit code 0 = all checks pass. Non-zero if dashes, unverified facts, or banned phrases are found.

## Support

See `CONTRIBUTING.md` for the contribution process. Bring a failing eval transcript if you find an issue.

## License

MIT. See LICENSE.
