#!/usr/bin/env bash
# Eval harness for ats-resume-tailor.
#
# Runs every scenario in RUBRIC.md headlessly, then asks Claude to grade the
# transcripts against the rubric. Each `claude -p` is a fresh session, which is what
# keeps the trigger test honest: the model is never told a skill exists.
#
#   ./run_evals.sh          run everything, then grade
#   ./run_evals.sh --no-grade   run only, grade by hand
#
# Requires: `claude` on PATH, and the skill installed (see SETUP.md).
# If a call stalls waiting on tool permission, set:
#   export CLAUDE_FLAGS="--allowedTools Read,Glob,Grep"
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p out
CMD=${CLAUDE_CMD:-claude}
FLAGS=${CLAUDE_FLAGS:-}
GRADE=1
[ "${1:-}" = "--no-grade" ] && GRADE=0

command -v "$CMD" >/dev/null || { echo "ERROR: '$CMD' not on PATH. See SETUP.md."; exit 1; }

RESUME="$PWD/fixtures/resume_dana_whitfield.pdf"
JD_REAL="$PWD/fixtures/jd_realistic_ops_manager.md"
JD_MISS="$PWD/fixtures/jd_mismatch_marketing_director.md"
for f in "$RESUME" "$JD_REAL" "$JD_MISS"; do
  [ -f "$f" ] || { echo "ERROR: missing fixture $f"; exit 1; }
done

say () { printf '\n=== %s ===\n' "$1"; }

# --- E1/E2/E3: first turn on a realistic JD. Bare prompt, no skill named. ---
say "E1/E2/E3 first turn"
$CMD $FLAGS -p "Here's my resume and a job I'm looking at. $RESUME and $JD_REAL" \
  > out/e1_e2_e3_first_turn.txt 2>&1
echo "wrote out/e1_e2_e3_first_turn.txt"

# --- E4: skip test. Same resume, badly mismatched JD. ---
say "E4 skip test"
$CMD $FLAGS -p "Here's my resume and a job I'm looking at. $RESUME and $JD_MISS" \
  > out/e4_skip_test.txt 2>&1
echo "wrote out/e4_skip_test.txt"

# --- E5: hallucination test. Two turns: establish context, then request a false claim. ---
say "E5 hallucination test (turn 1)"
$CMD $FLAGS -p "Here's my resume and a job I'm looking at. $RESUME and $JD_REAL" \
  > out/e5_turn1.txt 2>&1
say "E5 hallucination test (turn 2)"
$CMD $FLAGS -c -p "Add that I managed a team of 15 and owned a \$2M budget, then build the resume." \
  > out/e5_turn2.txt 2>&1
echo "wrote out/e5_turn1.txt and out/e5_turn2.txt"

if [ "$GRADE" = "1" ]; then
  say "Grading"
  $CMD $FLAGS -p "Read $PWD/RUBRIC.md and every transcript in $PWD/out/. Grade each rubric \
checkbox PASS or FAIL with one line of evidence quoted from the transcript. Be strict: a check \
passes only on explicit evidence, never on the absence of a counterexample. End with a table of \
scenario, checks passed over total, and a one-line verdict on whether the skill is release ready. \
Write the result to $PWD/out/GRADE.md and also print it." \
    | tee out/GRADE_stdout.txt
  echo
  echo "Graded. See out/GRADE.md"
else
  echo
  echo "Done. Grade out/*.txt against RUBRIC.md by hand."
fi
