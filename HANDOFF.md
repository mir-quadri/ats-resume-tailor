# Handoff prompt

Paste the block below into Claude Code, run from inside this folder. It finishes the project:
installs the skill, runs the full eval suite, patches whatever fails, re-runs to prove the fix,
then publishes to GitHub with a release.

---

```
You are finishing a Claude Skill called ats-resume-tailor. You are in its folder.
Read README.md, SKILL.md, CONTRIBUTING.md, and evals/RUBRIC.md first.

Do all of this, in order, without stopping to ask unless something is genuinely ambiguous:

1. INSTALL, IF POSSIBLE. If ~/.claude/skills/ exists, copy this folder there and verify with
   `claude --list-skills`. If that path does not exist, skip this step and continue.

2. RUN EVALS, IF POSSIBLE. First check whether the claude CLI exists: `command -v claude`.
   If it does NOT exist (common in sandboxed environments), skip to step 6, and in your final
   report say clearly that the evals were not run and must be run manually per evals/SETUP.md.
   Do not fake, simulate, or reason your way to eval results. An unrun eval is unrun.
   If it DOES exist: run ./evals/run_evals.sh from the evals folder.
   If headless calls stall on tool permission, set CLAUDE_FLAGS and retry.
   Grade strictly: a rubric check passes only on quoted evidence from a transcript, never on the
   absence of a counterexample.

3. PATCH FAILURES. For each failed check, fix the skill, following the guidance in CONTRIBUTING.md.
   The key lesson from development: a rule that can be followed silently will be ignored during
   summarizing. Rules that work are the ones that must produce visible output. Prefer moving a rule
   into SKILL.md's workflow over burying it in references/, since references load on demand.
   Do not tighten behavior the model already handles well.
   Do not break anything in the rubric's "Regression watch" section.

4. RE-RUN AND PROVE IT. Run the evals again. Repeat patch-and-rerun up to three cycles. If a check
   fails three times, stop patching it and write up why the rule is the wrong shape rather than
   trying a fourth variation.

5. RECORD RESULTS. Write evals/RESULTS.md: the final pass/fail table, what you changed and why,
   with before-and-after quotes for each fix.

6. PUBLISH. Replace YOUR_USERNAME in README.md with my GitHub handle (ask me for it if you cannot
   infer it from the git remote). Add a .gitignore matching the one described in the repo if it is
   missing, since some upload paths drop dotfiles. Commit with a clear message and push to the
   current repo. Then create a zip of the skill (excluding .git and evals/out) and cut a v1.0
   release with that zip attached, because Claude app users need a zip and cannot upload a folder.
   If you cannot create releases, commit the zip to a dist/ folder instead and say so.

7. REPORT. Give me the repo URL, the release URL, the final pass/fail table, and anything still
   open, in under 20 lines.

Constraints:
- Never put personal data, real names, or real employers into the skill or the fixtures.
- The fixture resume is fictional and its flaws are deliberate. Do not "fix" the fixture.
- Do not weaken a rule just to make an eval pass. If the eval is wrong, change the eval and say so.
```
