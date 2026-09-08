# Manual Eval Setup

Run these scenarios manually if the automated test runner (`run_evals.sh`) does not work in your environment.

## Prerequisites

- Claude Code CLI (`claude --version`)
- The skill installed in `~/.claude/skills/ats-resume-tailor` or available as a local folder
- Python 3 and the `docx` package for validator tests
- Node.js for building resumes

## Running each scenario

### Scenario 1: Ownership audit and flagged list

```bash
# Start a new Claude Code session in the evals folder
cd evals

# Create a test inputs file
cat > scenario1-input.txt << 'EOF'
Here is my resume:
[paste fixture-resume.txt content]

Here is the job description:
[paste jd-01.txt content]

Please assess if I'm a good fit for this role.
EOF

# Send to Claude with the skill enabled
claude < scenario1-input.txt
```

**Expected output:**
- Flagged-for-confirmation list with ownership and scope issues
- Complete fit assessment (strengths, gaps, percentage, call)
- Gap questions (unverified metrics, date gaps, retired claims)
- NO resume content in this turn

**Grading:** Check the output against RUBRIC.md scenario 1 criteria.

### Scenario 2: Complete fit assessment

(Continuation of scenario 1)

In the same Claude conversation, respond to the gap questions:

```
Q1. Was the query latency reduction your personal work?
A: No, it was a team effort and company infrastructure improvement.

Q2. Coordinated a shift of 22 engineers — what relationship is this?
A: I influenced the technical direction, but I didn't manage or lead these engineers directly.

Q3. Date gap May 2018 to June 2018?
A: One month, between jobs. Job search.

Q4. Anything to retire from the resume?
A: No.

Q5. Missing Spark experience?
A: That's a gap. Willing to learn.
```

**Expected output:**
- Updated fit assessment (not "go", still "conditional" due to Spark gap)
- Positioning lane chosen
- Ready to build resume

**Grading:** Verify fit assessment includes percentage and explicit call.

### Scenario 3: Ownership questions

(In scenario 1 output)

Grep the output for these patterns:

```bash
echo "Checking for ownership questions..."
grep -i "personal work\|team.*result\|department" scenario1-output.txt
```

**Expected:** At least one question asking about "company reduced" attribution.

### Scenario 4: No resume in first turn

(In scenario 1 output)

```bash
# Check that no resume content appears
grep -E "^EXPERIENCE|^SKILLS|^EDUCATION|\•" scenario1-output.txt && echo "FAIL: Resume content found" || echo "PASS: No resume content"
```

**Expected:** No output (no resume content found).

### Scenario 5: Validator

```bash
# Create a test DOCX with a banned phrase and a dash
cat > test-banned.txt << 'EOF'
grew the business
synergy
EOF

# Create a test ledger
cat > test-ledger.txt << 'EOF'
Built a data pipeline processing 50M events per day
Led a team of 3 engineers
EOF

# Create a test resume with en-dash (manually, since script doesn't generate DOCX)
# For this test, use an existing DOCX or create one with en-dash in it

# Run validator
python3 ../scripts/validate_resume.py test-resume.docx --source test-ledger.txt --banned test-banned.txt
echo "Exit code: $?"
```

**Expected:**
- If resume has "grew the business": ✗ Banned phrase check fails
- If resume has en-dash (–): ✗ Dash check fails
- If clean: ✓ All checks pass

## Checking results manually

For each scenario, save the output:

```bash
# Scenario 1 output
claude < scenario1-input.txt > ../out/scenario1-transcript.txt

# Check criteria from RUBRIC.md
echo "=== Scenario 1 ==="
grep -q "flagged for confirmation" ../out/scenario1-transcript.txt && echo "✓ Flagged list present" || echo "✗ No flagged list"
grep -q "[0-9]%\|percent\|go\|conditional\|skip" ../out/scenario1-transcript.txt && echo "✓ Verdict present" || echo "✗ No verdict"
grep -E "^EXPERIENCE|^\•|^\-" ../out/scenario1-transcript.txt && echo "✗ Resume content found" || echo "✓ No resume content"
```

## Troubleshooting

**Skill not loading:**
```bash
# Check if skill is installed
claude --list-skills | grep ats-resume-tailor

# If not, copy it to the skills folder
mkdir -p ~/.claude/skills
cp -r .. ~/.claude/skills/ats-resume-tailor
```

**Claude CLI not found:**
If `command -v claude` returns nothing, the evals cannot run. Install Claude Code per the main README.

**validator.py import errors:**
```bash
pip install python-docx
```

**Validator not executable:**
```bash
chmod +x ../scripts/validate_resume.py
python3 ../scripts/validate_resume.py resume.docx --source ledger.txt --jd jd.txt
```

## Grading rules

- **A check PASSES** if quoted evidence from the transcript matches the expected output.
- **A check FAILS** if the transcript does not show the expected behavior, even if similar behavior appears elsewhere.
- **Absence of a counterexample is not evidence.** "I don't see a dash check fail" does not mean the check works. The check must be observed passing.

Grade strictly. Do not assume the skill is working correctly if you cannot see it in the output.
