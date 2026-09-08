# ATS Resume Tailor

A Claude Skill that rebuilds a resume for one specific job description, then proves the result is
both machine-readable and true.

Most resume tools optimize for the keyword parser and quietly invent whatever the job description
asks for. That gets you the interview and loses it ten minutes in. This skill is built the other
way around: it starts by telling you honestly whether the role is worth your time, it treats your
verified facts as the only material it is allowed to use, and it enforces that with a script rather
than a promise.

## What it does

1. **Assesses fit before writing anything.** You get a plain read on where you are strong, where
   the gaps are, a rough percentage, and a go, conditional, or skip recommendation. Sometimes the
   most useful output is "do not apply to this one, here is why."
2. **Builds a fact ledger.** Every metric, title, date, scope number, tool, and certification you
   have. Nothing outside the ledger can appear in the resume.
3. **Asks about gaps instead of filling them.** Short multiple-choice questions with recommended
   defaults. A one-word "yes" licenses exactly what you confirmed and nothing more.
4. **Picks a positioning lane and holds it.** The resume argues you are a particular kind of
   professional, and the boundary it must not cross gets written down and checked.
5. **Writes an ATS-safe .docx**, single column, real bullets, standard headings, no em dashes.
6. **Validates programmatically.** Every number in the output must trace to your ledger. Retired
   claims get swept for automatically. Keyword coverage is reported against the job description.
7. **Renders the PDF and inspects it** for orphaned headings, overflow, and page-break problems.
8. **Reviews as four personas**: the parser, the recruiter, the hiring manager, and the skeptical
   interviewer who probes every line with three follow-up questions.
9. **Delivers PDF plus .docx** with a summary of how you were repositioned, how each gap was
   covered, and what is still open.

## Install

**Claude app (web, desktop, mobile).** Zip the `ats-resume-tailor` folder, then go to
Customize > Skills, click "+", "Create skill", "Upload a skill", and select the zip. Toggle it on.
Requires code execution to be enabled.

```bash
git clone https://github.com/mir-quadri/ats-resume-tailor.git
cd ats-resume-tailor && zip -r ats-resume-tailor.zip . --exclude ".git/*" "evals/out/*"
```

**Claude Code.** Skills load from a folder:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/mir-quadri/ats-resume-tailor.git ~/.claude/skills/ats-resume-tailor
claude --list-skills
```

Then start a conversation with your resume and a job description. It triggers on "tailor my resume
to this role", "is this job worth applying to", or just pasting a posting alongside your resume.
You do not name the skill.

## Tests

```bash
cd evals && ./run_evals.sh
```

Five scenarios against a fictional fixture resume with six planted flaws, graded against
`evals/RUBRIC.md`. See `evals/SETUP.md` for details and the manual fallback.

## Requirements

- Node.js with the `docx` package (`npm install docx`)
- Python 3
- LibreOffice for PDF conversion (`soffice`)
- Poppler utilities (`pdftotext`, `pdftoppm`)

## Using the validator standalone

```bash
python3 scripts/validate_resume.py resume.docx \
  --source ledger.txt \
  --jd jd.txt \
  --banned banned.txt
```

Non-zero exit if the dash check, numeric fact-check, or banned-phrase check fails, so it can gate a
build in CI or a script.

## The design principle

A defensible resume beats a keyword-perfect one. Every constraint in this skill exists to make
overstating your experience harder than stating it accurately, because the resume is not the goal.
The interview is, and the interview is where an inflated resume becomes a liability.

## Structure

```
ats-resume-tailor/
  SKILL.md                              the workflow and the non-negotiable rules
  README.md
  references/
    fit-assessment.md                   the go, no-go, conditional read
    fact-verification.md                fact ledger, banned claims, zero-hallucination protocol
    confirm-then-build.md               how to ask about gaps and handle the answers safely
    positioning-lanes.md                choosing a lane, holding it, seniority framing
    company-research.md                 gathering and honestly applying employer vocabulary
    ats-and-reviewer-strategy.md        keyword mapping, formatting, section order, top third
    persona-review.md                   the four-persona verification rubric
    build-and-validate.md               exact commands end to end
  scripts/
    validate_resume.py                  dash, numeric fact, banned phrase, keyword coverage
    build_resume.js                     ATS-safe .docx builder template
  assets/
    fact_ledger_template.md
    gap_questions_template.md
```

## Development notes

Four failures found in testing, each patched and re-tested:

| Failure | Fix |
|---|---|
| Restated a team's metric as the candidate's, and listed it as a strength | Ownership audit that must emit a visible flagged-for-confirmation list |
| Upgraded "coordinate a shift of 22" to "22 direct reports" | Scope-language pass that records the source's exact relationship word |
| Missed an 18-month employment gap | Date-gap pass, plus a required question about each gap |
| Gave strength and gap categories with no verdict | A percentage and an explicit go, conditional, or skip |

The pattern behind all four: a rule that can be followed silently will be, and then it evaporates
during summarizing. Rules that survive are the ones that must produce output someone can see.

## Contributing

See `CONTRIBUTING.md`. Bring a failing eval transcript.

## License

MIT. See `LICENSE`.
