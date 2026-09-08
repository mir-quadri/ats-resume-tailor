# Fact Verification

Build a fact ledger from the source resume, then audit it. This is where hallucination stops.

## The fact ledger

Transcribe every verified fact from the source resume:
- Titles and employers
- Dates (employment, credentials)
- Metrics and outcomes
- Tools and technologies
- Certifications
- Education

Format: plain text, one fact per line, grouped by role. See `assets/fact_ledger_template.md`.

## The audit

After transcribing, read what you wrote and flag unverified items. Three types:

### 1. Ownership

**Flag any metric whose grammar does not credit the candidate personally.**

Examples:
- "The department cut shrink 30%" → UNVERIFIED. Was it their work?
- "Led cost reduction from 40% to 22%" → VERIFIED. Active voice, personal claim.
- "The team shipped the feature in 6 weeks" → UNVERIFIED. Did they lead it?

The grammar tells you: "We reduced", "The team achieved", "The department grew" are red flags.
"I led", "I built", "I achieved" are green.

**Action:** Ask the candidate for each unverified metric: "Was that your work, your team's, or the department's result?"

### 2. Scope language

**Record the exact relationship word: led, managed, supervised, coordinated, supported, contributed to.**

These are not interchangeable. Never upgrade "coordinated a shift" to "managed a shift" or "led a team of 22" when the source says "coordinated with 22 people."

**Action:** Keep the original word. If the candidate confirms in the gap-question round, record their answer.

### 3. Date gaps

**Flag every gap between roles, with length.**

Example:
- Role A ended June 2021
- Role B started January 2023
- Gap: 18 months

**Action:** Ask the candidate how they want it handled. Education, contract work, leave, relocation—know the story.

### 4. Currency

**Record the last year each skill was used.**

If the source says "Python, 2018" and it's now 2025, flag it. Ask if it is still active or if the candidate wants to omit it.

## The flagged list

Write the flagged-for-confirmation list into your reply, where the candidate can see it. This list must be visible. One line per item. Example:

> **Flagged for confirmation:**
> - "Department cut shrink 30%" — was this your personal work?
> - Date gap Jan 2022 to June 2022 (5 months) — what was this?
> - "Python" last used 2018 — still active?

## Zero hallucination rule

Every fact in the final resume must come from one of two places:
1. The candidate's source resume (from the ledger).
2. Something they explicitly confirmed in conversation.

Never invent. If the JD asks for something unconfirmed, that is a gap to flag in the fit assessment, never a blank to fill.

## Banned phrases

After confirmation, ask the candidate which claims they want to retire. These become the banned list. Example:

> **Banned (do not use):**
> - "grew the business"
> - "synergy"

The validator checks the final resume against this list.
