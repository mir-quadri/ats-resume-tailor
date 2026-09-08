# Running the evals in Claude Code

Two phases. Setup is one-time.

## 1. Install the skill where Claude Code looks for it

Claude Code reads skills from a folder, not a zip. Personal install:

```bash
mkdir -p ~/.claude/skills
cp -r /path/to/ats-resume-tailor ~/.claude/skills/
```

Or project-scoped, from inside a project directory:

```bash
mkdir -p .claude/skills && cp -r /path/to/ats-resume-tailor .claude/skills/
```

Verify with `claude --list-skills`, or `/skills` inside a session. `ats-resume-tailor` should
appear. If it does not, check that `SKILL.md` sits directly inside the `ats-resume-tailor` folder.

## 2. Run

```bash
cd ~/.claude/skills/ats-resume-tailor/evals
./run_evals.sh
```

Transcripts land in `out/`, and a graded report in `out/GRADE.md`.

## Why the script uses separate headless calls

Every `claude -p` starts a fresh session. That matters: the whole point of E1 is whether the
skill's description triggers on a bare prompt, with nothing naming it. If you set this up as one
long conversation that begins "test my resume skill", the model knows the skill exists and E1 can
no longer fail. E5 is the one exception and uses `-c` deliberately, because a request to invent a
credential only means something once the model is mid-task.

## If a call hangs or returns a permission error

Headless mode may block on tool permission. Try:

```bash
export CLAUDE_FLAGS="--allowedTools Read,Glob,Grep"
```

Flag names vary by Claude Code version. Check `claude --help` if that one is not recognized.

## Manual fallback

If the CLI fights you, run the scenarios by hand in the chat app instead. Open a fresh chat per
scenario, attach the fixtures, send only the prompt text from `run_evals.sh`, and grade the
replies against `RUBRIC.md` yourself. Same test, more clicking.

## Grading honestly

The grader is told to pass a check only on explicit evidence. Resist the urge to accept "it
didn't do the bad thing" as a pass for a check that requires it to do a good thing. Three of the
four bugs found in development looked like passes under loose grading.
