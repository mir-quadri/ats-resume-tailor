# Fact Ledger

The complete universe of facts allowed in the resume. Anything not here cannot appear.
Keep a plaintext copy (`ledger.txt`) on disk so `validate_resume.py --source` can read it.

## From the source resume

### Employers, titles, dates
- Employer | Exact Title | Mon YYYY to Mon YYYY | City, State

### Scope numbers
- Headcount managed, teams, programs, users, transactions, requests

### Financials
- Budget, portfolio value, cost figures

### Metrics and outcomes
- Metric, the number, and what work it attaches to. If ownership is unclear, mark it UNVERIFIED
  and ask before using it.

### Tools, platforms, technologies
- Name | what it actually is | the candidate's real relationship to it (built, operated,
  directed, evaluated, studied)

### Education and certifications
- Institution, degree, field, year. Certifications including any in progress, labeled as such.

## Confirmed in conversation

One line per fact, in the candidate's own words, dated. These are usable only after being written
down here.

- [YYYY-MM-DD] Fact exactly as the candidate stated it. Confirmed by candidate.

## Banned claims (never use again)

Mirror these into `banned.txt`, one phrase per line, for the automated sweep.

- Retired claim, plus one line on why it was retired.

## Boundaries

The lines this candidate's resume must not cross, from `positioning-lanes.md`.

- Never claim: ...
- Always frame X as: ...
