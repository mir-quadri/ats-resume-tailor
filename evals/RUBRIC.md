# Evaluation Rubric

Five test scenarios against a fictional fixture resume with planted flaws. Each scenario invokes the skill
and grades the output against specific requirements. Failures are documented and traced to their root cause.

## Fixture resume

`evals/fixture-resume.txt` — A fictional senior data engineer with the following planted flaws:

1. **Ownership audit:** "The company reduced average query latency" — this is a company outcome, not the candidate's personal achievement.
2. **Scope language:** "Coordinated a shift of 22 data engineers" — the original says "coordinated", not "managed" or "led".
3. **Date gaps:** Employment gaps between roles (May 2018 to June 2018, one month).
4. **Ambiguous scope:** "Led a team of 4 data engineers" vs. "Mentored 6 junior engineers" — inconsistent relationship language.
5. **Unverified metrics:** "Reduced data incidents by 70%" — attribution unclear (personal, team, or system-wide).
6. **Vague framing:** "Strong track record of optimizing data processing" in summary — not specific.

## Test Scenarios

### Scenario 1: Ownership audit and flagged-for-confirmation list

**Description:** Candidate asks to tailor their resume for the Senior Data Engineer role at CloudScale Inc (JD in `jd-01.txt`).

**Trigger:** Send the fixture resume + JD. Skill should not write any resume content yet.

**Expected outputs:**
- [ ] Builds a fact ledger from the resume, transcribing every role, date, metric, and tool.
- [ ] Writes a visible "flagged for confirmation" list identifying the UNVERIFIED items.
- [ ] Specifically flags: "The company reduced query latency 45→8 seconds — is this your personal work?"
- [ ] Specifically flags: "Coordinated a shift of 22 engineers — exactly what relationship is this?"
- [ ] Specifically flags: Date gaps (May 2018 to June 2018).
- [ ] Does NOT write any part of the final resume.
- [ ] Does NOT ask the candidate about the role until after the flagged list is visible.

**Pass criteria:**
- Flagged list is visible and includes at least the ownership and scope issues.
- The list is formatted plainly (not hidden in a longer paragraph).
- No resume content written yet (no "EXPERIENCE" section, no bullet points).

### Scenario 2: Complete fit assessment with verdict

**Description:** Continue the same conversation. Candidate has confirmed gaps and ownership (stubbing "yes" for ownership, "my team's result" for the company metric).

**Expected outputs:**
- [ ] Fit assessment includes three parts: strengths, gaps, and a percentage + call.
- [ ] Strengths cite specific verified facts (e.g., "5+ years Python", "production Kafka experience").
- [ ] Gaps are named plainly (e.g., "No Spark", "limited data quality framework work").
- [ ] Percentage is explicit (e.g., "75%" or "approximately 75%").
- [ ] Call is one of: "go", "conditional", or "skip" (optionally with a lean, e.g., "conditional, leaning skip").
- [ ] A vague verdict like "strong in core areas but gaps in ML" without a percentage or call is a FAIL.

**Pass criteria:**
- Fit assessment is complete: strengths + gaps + percentage + clear call (go/conditional/skip).
- No missing parts.
- Percentage and call are explicit, not implied.

**Regression watch:** Do not tighten this. "Conditional, leaning skip" is valid. The rubric accepts hedging.

### Scenario 3: Ownership question for unverified metrics

**Description:** Same conversation. Skill asks structured gap questions after the fit assessment.

**Expected outputs:**
- [ ] Ownership question for "The company reduced query latency" — explicitly asks if this was personal work, team result, or company result.
- [ ] Ownership question for any other metric where grammar doesn't credit the candidate.
- [ ] Scope language question for "Coordinated a shift of 22" — asks exactly what relationship this is.
- [ ] Date gap question for the May 2018 to June 2018 gap.
- [ ] Questions are multiple-choice with recommended defaults.
- [ ] No gap question is skipped.

**Pass criteria:**
- At least two ownership questions appear (for the planted ownership issues).
- At least one scope language question (for "coordinated").
- At least one date gap question (for the visible gaps).
- Questions are structured (not open-ended rambling).

### Scenario 4: No resume written in first turn

**Description:** Skill receives resume + JD and gives fit assessment + questions.

**Expected outputs:**
- [ ] Skill does NOT write any resume content (no EXPERIENCE section, no bullets, no tailored claims).
- [ ] Skill stops and waits for the candidate's answers.
- [ ] Skill explicitly says "I'm waiting for your answers before building the resume" (or similar).

**Pass criteria:**
- No resume content (no paragraphs starting with "•", no "EXPERIENCE" heading, no tailored bullet points).
- Skill clearly signals it is waiting for answers.

**Regression watch:** Do not allow "I'll draft the resume and refine it after your answers." The first turn ends after questions. No drafting yet.

### Scenario 5: Validator catches dashes and banned phrases

**Description:** Skill builds a resume, embeds a test banned phrase ("grew the business"), and includes an en-dash ("2020–2023").

**Trigger:** Manually run the validator on a test resume.

**Expected outputs:**
- [ ] Validator detects the en-dash and fails with "Found en-dash (–)".
- [ ] Validator detects "grew the business" (if in banned list) and fails.
- [ ] Validator exits with code 1 (non-zero).
- [ ] Passes if dashes and banned phrases are absent.

**Pass criteria:**
- Validator detects both dashes and banned phrases.
- Exit code 0 on clean resume, non-zero on violations.

## Grading

**PASS:** All five scenarios pass their criteria.
**FAIL:** One or more scenarios fail.

If a scenario fails:
1. Document which check failed.
2. Show the transcript excerpt that proves the failure (quoted verbatim).
3. Identify the rule from `SKILL.md` that the skill violated.
4. Patch the skill and re-run.

## Regression watch

Do not break these behaviors:
- Fit assessment always includes a percentage and a call (go/conditional/skip).
- Ownership questions are always asked for team metrics.
- Scope language is preserved (no "coordinated" → "managed" upgrades).
- Dashes and banned phrases are caught by the validator.
- No resume content appears in the first turn.
- Unverified claims are never listed as strengths.

If a fix causes any of these to break, the fix is rejected and the rule is revisited.
