# Fact Verification (Zero Hallucination)

A tailored resume that reads well but contains one claim the candidate cannot defend is worse than
useless. It gets them caught in the interview and burns the relationship. This protocol makes
fabrication structurally hard rather than relying on good intentions.

## The fact ledger

Before writing a single bullet, build a **fact ledger** from the source resume. Every hard fact the
candidate has already put in writing:

- **Employers and titles**, exact strings, exact spelling.
- **Dates and tenure.**
- **Scope numbers.** Headcount, program counts, team counts, user counts, transaction volumes.
- **Financials.** Budget size, cost figures.
- **Metrics and outcomes.** Percentages, time reductions, availability figures.
- **Tools and platforms**, with their real function.
- **Certifications and education**, including anything in progress.

## Audit the ledger before you use it

The source resume is not a verified record. It is the candidate's previous draft, written under the
same pressure to impress, and it usually contains at least one claim that will not survive
questioning. Reading it into the ledger is not the same as accepting it.

Four passes over what you just transcribed:

1. **Ownership.** Flag every metric whose grammar credits someone else. "The department reduced",
   "the team achieved", "the company grew". Mark it UNVERIFIED and ask. Until the candidate says
   what their part was, it does not go in the resume and it does not go in your fit assessment
   either. A borrowed number in the strengths column is the same error as a borrowed number in a
   bullet, one step earlier.
2. **Scope language.** Record the exact relationship word. "Coordinated a shift of 22" is not
   "22 direct reports". "Supported the rollout" is not "led the rollout". These upgrades happen
   silently while summarizing, and they are the most common way an honest build goes wrong.
3. **Date gaps.** List every gap between roles, with its length. Ask about each one at intake.
4. **Currency.** Note the last year each skill was actually used.

**The ledger is the entire universe of allowed facts.** If a fact is not in the ledger and the
candidate has not confirmed it in this conversation, it cannot appear in the resume. Rewording is
fine. Inventing is not. Template in `assets/fact_ledger_template.md`.

## The ledger is a real file, not a mental note

Keep the ledger as a text file on disk, because the validator reads it. The pattern:

```bash
pdftotext -layout source_resume.pdf ledger.txt     # start from the source resume
cat >> ledger.txt << 'EOF'                          # append confirmed additions

=== CONFIRMED IN CONVERSATION ===
Supervised a team of 6 on the evening shift. Confirmed by candidate.
Holds a state teaching license, active. Confirmed by candidate.
EOF
```

Then pass `--source ledger.txt` to the validator. Any number in the finished resume that is not in
this file fails the build. This is what makes "confirmed in conversation" a real mechanism instead
of a promise: a confirmed fact only becomes usable once it is written down, and writing it down
forces you to state it in exactly the words the candidate used.

## The banned-claims list

Careers accumulate claims that should never be used again: a metric that turned out to belong to
someone else's project, a number the candidate can no longer substantiate, a scope framing that
misled a past interviewer, an old title that overstates what they did.

Keep these in a `banned.txt`, one phrase per line, and pass it to the validator with `--banned`.
Lines starting with `#` are comments.

```
# Retired claims. Never use these again.
# Each line is a phrase that must never appear in any future resume.
doubled regional revenue
managed a team of 25
Director of Operations
```

Once a claim is retired it is retired permanently, across every future build, even when a JD makes
it tempting. A retired claim reappearing is a failed build. This matters more than it sounds:
retired claims come back precisely when a JD asks for exactly the thing the bad metric would prove.

## What counts as a hallucination (all banned)

- A metric attached to work the candidate did not personally own.
- A number absent from the source. Inflated headcount, invented percentage.
- A tool or skill never listed and never confirmed.
- An upgraded title or a stretched date range.
- A cause-and-effect link the source does not support.
- An employer's proprietary framework claimed as the candidate's own delivery. Mirror their
  language about your own work. Do not claim their trademarked program. See `company-research.md`.
- **Specifics inflated from a general confirmation.** The most common failure. See
  `confirm-then-build.md`.
- **A currency claim the candidate cannot meet today.** Listing a language they used a decade ago
  as current proficiency. Frame it by what it actually was and when.

## The rule when you hit a gap

Do not fill it. Flag it, with a specific question: "The JD wants X. I do not see X in your source.
Have you done X, and if so, where?" Only add after an explicit yes with detail.

Honest positioning wins. A defensible resume beats a keyword-perfect one, because the
keyword-perfect one gets the interview and then loses it in the first ten minutes.

## Programmatic backstop

`scripts/validate_resume.py` extracts every number from the finished resume and checks each against
the ledger, plus sweeps for retired claims and banned dashes. This does not catch every kind of
embellishment, since wording can overstate without using a number, which is why the
**skeptical-interviewer persona** in `persona-review.md` is also mandatory. Read every bullet and
ask: could the candidate defend this under three follow-up questions? If not, cut it, soften it, or
go get it confirmed.
