---
name: ats-resume-tailor
description: >
  Tailor a resume to a specific job description so it passes automated screening (ATS) and wins
  over recruiters and hiring managers, then deliver it as a verified PDF with a companion .docx.
  Includes an honest fit assessment before any writing happens, a zero-hallucination fact ledger,
  structured gap questions, and programmatic validation. Use this skill whenever the user wants to
  tailor, rewrite, customize, optimize, or ATS-proof a resume for a named role or pasted job
  description, wants their resume "matched to this JD", asks to "prepare my resume for this job",
  asks whether a role is worth applying to, wants keyword or ATS coverage checked, or wants a
  resume built as a PDF or Word file. Trigger even if they only paste a job posting and a resume
  without the word "tailor". Do NOT use for cover letters alone or LinkedIn profile rewrites
  unless a resume is also involved.
---

# ATS Resume Tailor

v1.0

Rebuild a resume for one target role so it survives every gatekeeper, in order: the **ATS**
(keyword parser), the **recruiter** (six-second must-have skim), the **hiring manager** (evidence
they can do the job), and the **skeptical interviewer** (will any claim survive questioning). A
resume that beats one lane but fails another loses.

**Analogy.** Airport security. The ATS is the metal detector, pure pattern match. The recruiter
glances at your passport to see if the basics line up. The hiring manager decides whether you
belong on the flight. The interviewer pulls you aside and asks follow-ups. The same document has
to clear all four, and optimizing hard for the metal detector is exactly how you get pulled aside.

## Four rules that override everything

**1. Zero hallucination.** Every fact must trace to the candidate's source resume or to something
they explicitly confirmed in conversation. Never invent a skill, tool, metric, title, date,
employer, or outcome. If the JD wants something unconfirmed, that is a GAP to flag, never a blank
to fill. Enforced programmatically and by the skeptical-interviewer persona. One unverifiable
number is a failed build. See `references/fact-verification.md`.

**2. An audit finding must be visible to count.** Anything you flag while reading the source, an
unverified metric, a date gap, an inflated scope word, gets written into the reply. Findings kept
in your head do not survive summarizing. This is the failure mode this skill exists to prevent.

**3. Assess fit before building.** Do not open a document until you have told the candidate,
plainly, how well they actually match and whether the role is worth their time. Someone with a
strong pipeline is better served by an honest "skip this one" than by a beautiful resume for a
role they will not get. See `references/fit-assessment.md`.

**4. Confirm, then build.** Gaps get resolved by asking the candidate, with recommended defaults,
before writing. Never resolve a gap by guessing, and never expand a one-word confirmation into
specifics they did not give. See `references/confirm-then-build.md`.

These four rules govern everything you say, not just what you put in the document. The fit
assessment is part of the output. If it restates a team's result as the candidate's, or calls
coordination "direct reports", the resume has already been compromised, because every later step
builds on that summary.

## Workflow

1. **Read both inputs fully.** Extract the source resume and read the JD end to end. Never work
   from a skim. Commands in `references/build-and-validate.md`.
2. **Research the company.** Gather real terminology, methodology, values, and named frameworks so
   the tailoring mirrors how they talk. See `references/company-research.md`. Company knowledge
   shapes framing and keywords only. It never becomes invented candidate experience.
3. **Build the fact ledger, then audit it.** Transcribe every metric, title, date, employer, scope
   number, tool, and certification from the source. Then audit what you wrote, because a source
   resume is not a verified record, it is the candidate's previous draft:
   - **Ownership.** Any metric whose grammar credits someone else ("the department reduced", "the
     team achieved", "the company grew") is UNVERIFIED.
   - **Scope language.** Record the exact relationship word. "Coordinated", "supported", "led",
     "supervised", and "managed" are different claims. Never upgrade one to another.
   - **Date gaps.** Every gap between roles, with its length.
   - **Currency.** The last year each skill was actually used.

   **Write the UNVERIFIED list down where the candidate can see it.** A short "flagged for
   confirmation" list, one line each, stating the claim and why it is flagged. This is not
   optional and it is not internal. An audit finding that produces no visible output does not
   survive into the next step, which is the single most common way this skill fails.

   The ledger is the only pool of facts allowed in the output. Template in
   `assets/fact_ledger_template.md`.
4. **Map evidence to requirements, then assess fit.** For each JD requirement find the strongest
   TRUE evidence. Anything with no honest match is a gap.

   **No UNVERIFIED item may appear as a strength.** If an unverified metric is the candidate's
   strongest apparent evidence for a requirement, that requirement is unevidenced pending
   confirmation, and it is listed with the gaps, not the strengths. Promoting it "for now" and
   sorting it out later never happens, because every later step reads the summary, not the source.

   Then give a verdict with all three parts:
   - Where they are strong, tied to the JD's own weightings.
   - The gaps, named plainly, with the biggest risk called out.
   - **A rough percentage and one of three calls: go, conditional, or skip.** A lean is fine and
     often more useful than a label ("conditional, leaning skip"). What is not fine is stopping at
     categories of strengths and gaps. The candidate needs a recommendation they can act on.

   See `references/fit-assessment.md`.
5. **Ask one round of questions,** in the same reply as the verdict. Short, structured, answerable by choosing rather than composing,
   with a recommended default. It must cover, in this order:
   - **Every UNVERIFIED metric.** "Your resume says the department cut shrink 30%. Was that your
     work, your team's, or the department's result?" Never skip these. An unasked ownership
     question means the metric is either dropped or, worse, quietly kept.
   - **Every date gap.** How the candidate wants it handled.
   - **Anything to retire.** Claims they no longer want to make. This builds the banned list.
   - **The JD gaps.** Whether each is a real gap or just missing from the page.
   - **Target title, location, or licensure**, only if the source resume leaves them unclear.

   Patterns in `assets/gap_questions_template.md`. See `references/confirm-then-build.md` for the
   one-word confirmation rule, which governs what you may do with the answers.

   **Then stop and wait.** Steps 3, 4, and 5 are one reply and the whole of your first turn. It
   looks like this, in this order: the flagged-for-confirmation list, where they are strong, the
   gaps, the percentage and the call, then the questions. Do not write any part of the resume in
   this turn, and do not proceed on a maybe.
6. **Pick the positioning lane.** Decide which identity the resume leads with, and write down the
   boundary it must not cross. See `references/positioning-lanes.md`.
7. **Rebuild from scratch.** Do not lightly edit the old resume. Use only ledger facts, confirmed
   additions, and honest company framing. Follow the section order and top-third rules in
   `references/ats-and-reviewer-strategy.md`.
8. **Build the .docx** with ATS-safe formatting per `references/build-and-validate.md`. A working
   template is in `scripts/build_resume.js`.
9. **Verify, every time, in this order:**
   - **Programmatic.** Run `scripts/validate_resume.py resume.docx --source <ledger> --jd <jd>
     --banned <banned.txt>`. Dash check, numeric fact-check, and banned-phrase check must all PASS.
   - **Close the keyword loop.** Read the missing-keyword list. Add only the ones that are honestly
     true, rerun, repeat. Leave the rest missing and flag them as gaps.
   - **Render to PDF and look at it.** Rasterize the pages and view the images. Confirm clean
     layout, one to two pages, no overflow, no orphaned headings.
   - **Multi-persona review.** All four personas in `references/persona-review.md`.
10. **Deliver the PDF** as the final output with the .docx as a companion, then summarize: how you
    repositioned them, how each gap was covered, what is still open, and the single highest-leverage
    upgrade left. See "Delivery summary" below.

## Non-negotiable output rules

- **PDF is the final deliverable**, generated from the verified .docx. Ship both. Tell the
  candidate to submit the .docx if a portal asks for Word.
- **The numeric fact-check and banned-phrase check must pass.**
- **No em dashes or en dashes.** They are an ATS and readability liability and a common "AI wrote
  this" tell. Use periods, commas, or "to" for ranges ("3 to 5 years"). One dash is a failed build.
- **Plain, short sentences.** No consultant-speak, no filler. Write like a sharp, direct professional.
- **One to two pages**, single column, standard headings, standard fonts.

## Delivery summary

End every build with a short, plain-spoken summary. Four parts, no padding:

1. **Validation status.** Checks passed, keyword coverage as a fraction, page count.
2. **How you repositioned them.** The lane you chose and what moved to the top third, in one
   short paragraph.
3. **How each gap was covered.** One line per gap. Name the gap, then say what honest material
   compensates for it, or say plainly that it was left uncovered.
4. **What is still open.** What you deliberately left out for lack of confirmation, and the single
   highest-leverage thing the candidate could add or do before submitting.

Never claim a gap is closed when it is only reframed. The candidate has to walk into the interview
knowing exactly where the soft ground is.

## References and scripts

- `references/fit-assessment.md` — the go, no-go, conditional read. Run before writing anything.
- `references/fact-verification.md` — fact ledger, banned claims, zero-hallucination protocol.
- `references/confirm-then-build.md` — how to ask gap questions and handle answers safely.
- `references/positioning-lanes.md` — choosing the lane, lane discipline, seniority framing.
- `references/company-research.md` — gathering and honestly applying employer vocabulary.
- `references/ats-and-reviewer-strategy.md` — keyword mapping, ATS-safe formatting, section order,
  the top-third value proposition. Read before writing bullets.
- `references/persona-review.md` — the four-persona verification rubric. Run before every delivery.
- `references/build-and-validate.md` — exact commands to extract, build, patch, validate, render.
- `scripts/validate_resume.py` — dash check, numeric fact-check, banned-phrase check, JD keyword coverage.
- `scripts/build_resume.js` — working ATS-safe .docx builder to copy and fill in.
- `assets/fact_ledger_template.md` — the ledger format.
- `assets/gap_questions_template.md` — patterns for the confirm-then-build questions.
