# Contributing

The bar for a change here is evidence, not opinion. This skill was built by finding four real
failures in testing and patching each one, so that is the shape a contribution should take.

## Before you open a PR

1. **Reproduce the problem.** Run `evals/run_evals.sh` on the current version and show the failing
   check from `evals/out/`. A transcript is worth more than a description.
2. **Make the change.**
3. **Rerun the evals.** Confirm your fix passes and nothing in the regression watch broke.
4. **Include both transcripts** in the PR, before and after.

## What tends to work

Rules that produce a visible artifact. The ownership audit failed twice as an instruction to "mark
it UNVERIFIED" and passed immediately once it required writing a flagged list into the reply. If
your rule can be followed silently, it will be followed silently, and then it will be forgotten
during summarizing.

## What tends not to work

- Moving a rule into a reference file. References load on demand. If a step must always happen, it
  belongs in `SKILL.md`'s workflow.
- Adding a rule without deleting one. `SKILL.md` competes for attention with itself.
- Tightening a rule the model already handles well. One run produced "conditional, leaning skip",
  which the rubric technically forbade. The rubric changed, not the skill.

## Adding an eval

New scenarios go in `evals/RUBRIC.md` with a matching call in `run_evals.sh`. Fixtures must be
fictional. Every planted flaw should map to a documented check.

## Scope

Bug reports, new evals, and better fixtures are all welcome. Personal fact ledgers and
banned-claims lists are not: those are per-candidate and belong in your own working directory,
never in this repo.
