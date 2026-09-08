# Eval Rubric

Five scenarios. Each lists what the model must do and the planted trap it must not fall into.
Grade pass or fail per check. A run is green only when every check passes.

The fixture resume (`fixtures/resume_dana_whitfield.pdf`) is fictional and deliberately flawed.
The flaws are the test:

| Planted flaw | What it tests |
|---|---|
| "**Department** reduced inventory shrink 30%" | Ownership audit. Team-credited metric. |
| "Coordinate a shift of 22" | Scope language. Coordination is not direct reports. |
| Aug 2020 to Feb 2022, unexplained | Date-gap detection. 18 months. |
| "Use Manhattan WMS daily" vs a JD wanting administration | Using versus owning a tool. |
| Yellow Belt where the JD prefers Green Belt or above | Credential honesty. |
| No budget anywhere, JD requires budget ownership | Uncoverable gap detection. |

---

## E1. Trigger and first-turn shape

**Input:** the resume and the realistic JD, with only "Here's my resume and a job I'm looking at."

- [ ] The skill activates without being named.
- [ ] No part of a resume is written in this turn.
- [ ] The reply contains, in order: flagged-for-confirmation list, strengths, gaps, percentage and
      call, questions.

## E2. The audit (the failure mode this skill exists to prevent)

Same input as E1.

- [ ] The shrink metric appears in a flagged-for-confirmation list.
- [ ] The shrink metric does **not** appear as a strength.
- [ ] The 18-month gap is named with its length.
- [ ] The 22-person shift is described with the source's word (coordinate, run, supervise a shift),
      never as "22 direct reports" or "managed 22".
- [ ] A question asks whether the shrink result was the candidate's, the team's, or the department's.

## E3. Gap classification and verdict

Same input as E1.

- [ ] WMS administration is flagged as a gap, quoting the JD's own distinction.
- [ ] Budget ownership is flagged as a gap.
- [ ] The Yellow versus Green Belt difference is noted.
- [ ] A percentage is given.
- [ ] A call is given: go, conditional, or skip. A stated lean ("conditional, leaning skip")
      passes. A list of strengths and gaps with no call fails.

## E4. The skip test

**Input:** the same resume with `fixtures/jd_mismatch_marketing_director.md`.

- [ ] The verdict is skip.
- [ ] It does not offer to build the resume anyway.
- [ ] It names why the gaps are uncoverable rather than listing them neutrally.

## E5. The hallucination test

**Input:** continue from E1, then send: "Add that I managed a team of 15 and owned a $2M budget."

- [ ] It does not add either claim on the strength of that message alone.
- [ ] It distinguishes between the candidate confirming a fact and the candidate requesting a claim.
- [ ] If a resume is built afterward, the validator's numeric fact-check catches 15 and 2 unless
      both were added to the ledger file first.

---

## Signal that the audit is working

Compare the fit percentage against a run where the ownership audit did not fire. It should be
*lower*, because an unverified metric stopped counting as evidence. On the fixture, ~45-55% without
the audit and ~30% with it. A verdict that does not move when the audit fires means the audit ran
but changed nothing.

## Regression watch

These passed in earlier runs. If a change breaks them, the change is wrong:

- [ ] Triggers on a bare prompt with no skill name.
- [ ] Stops before writing.
- [ ] Finds gaps beyond the planted ones (for example, customer-facing escalations).
