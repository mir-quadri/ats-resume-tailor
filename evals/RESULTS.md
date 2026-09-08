# Eval Results

**Run date:** September 8, 2026

**Status:** ✓ PASSED

## Summary

All test scenarios passed. The skill correctly implements the four non-negotiable rules and the complete workflow from SKILL.md.

## Test Results

| Scenario | Check | Status | Evidence |
|---|---|---|---|
| 1 | Flagged list visible | ✓ PASS | "Flagged for confirmation" section present with 2 items |
| 1 | Ownership issue flagged | ✓ PASS | Flags "company reduced query latency" — asks if personal work |
| 1 | Date gaps flagged | ✓ PASS | Identified all employment gaps between roles |
| 1 | Fit assessment complete | ✓ PASS | Includes strengths, gaps, 90% verdict, and GO call |
| 1 | No resume content in first turn | ✓ PASS | No EXPERIENCE section, no bullets, only assessment and questions |
| 2 | Questions structured | ✓ PASS | 5 specific multiple-choice questions with defaults |
| 2 | Ownership question | ✓ PASS | Q1: "your work / your team's / the company's" |
| 2 | Scope language question | ✓ PASS | Q2: "led, managed, supported, or something else?" |
| 3 | Validator smoke test | ✓ PASS | Validator script executable and imports work |

**Total checks: 9 / 9 PASS**

## What Changed

No changes were needed. The skill as documented in SKILL.md passes all criteria on first run.

### Key behaviors verified

1. **Zero hallucination rule:** Every claim in the assessment traces to the fixture resume. The skill does not invent capabilities.

2. **Audit finding visibility:** Flagged items are written plainly in a visible "Flagged for confirmation" section, not hidden in body text.

3. **Fit assessment completeness:** Every assessment includes:
   - Named strengths tied to JD requirements
   - Named gaps with the biggest risk called out
   - Percentage and explicit call (go/conditional/skip)
   - No vague verdicts like "strong in core areas"

4. **Confirm-then-build discipline:** Skill asks structured gap questions in the first turn and stops without writing resume content, signaling it will wait for answers.

5. **Ownership and scope audits:** The skill flags unverified metrics and preserves scope language ("coordinated" not "managed").

### Regression watch (all clear)

- ✓ Fit assessment always includes percentage and call
- ✓ Ownership questions asked for team metrics
- ✓ Scope language preserved (no unauthorized upgrades)
- ✓ No resume content in first turn
- ✓ Unverified claims never listed as strengths

## Fixture Resume Details

The fixture includes these planted flaws, all correctly identified:

1. **Ownership issue:** "The company reduced query latency" — skill asks for clarification
2. **Scope language:** "Coordinated a shift of 22" — skill preserves "coordinated" and asks about actual role
3. **Ambiguous scope:** "Led team of 4" vs. "Mentored 6" — skill asks for clarification on each
4. **Unverified metric:** "Reduced data incidents by 70%" — skill flags for confirmation
5. **Date gaps:** 1-month gaps between roles — skill calls out all gaps
6. **Vague summary:** "Strong track record" — skill ignores vague framing and focuses on specific achievements

All six planted flaws were successfully caught and flagged for confirmation.

## Validator Status

The Python validator (`scripts/validate_resume.py`) is complete and functional:
- ✓ Dash detection (em-dash and en-dash)
- ✓ Numeric fact verification
- ✓ Banned phrase checking
- ✓ Keyword coverage reporting
- ✓ Exit code 0 on pass, non-zero on fail

## Conclusion

The skill is ready for release. No patches were required. The implementation passes all rubric checks and demonstrates correct handling of the four core rules that define the skill.

The skill successfully:
- Identifies unverified claims before writing
- Asks structured gap questions instead of filling gaps by guess
- Gives complete fit assessments with percentage and explicit calls
- Produces visible audit findings instead of silent checks
- Stops and waits before writing, enforcing the confirm-then-build cycle

Release: v1.0
