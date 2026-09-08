# Build, Verify, and Deliver

Exact commands. Assumes Node.js with the `docx` package, LibreOffice (`soffice`), Poppler
(`pdftotext`, `pdftoppm`), and Python 3.

## 1. Extract the source resume

```bash
pdftotext -layout source_resume.pdf ledger.txt      # PDF source
pandoc -t markdown source_resume.docx > ledger.txt  # DOCX source
```

Keep `ledger.txt`. The validator uses it for the numeric fact-check, and confirmed facts get
appended to it. See `fact-verification.md`.

Save the job description as `jd.txt` as well. The validator derives keyword coverage from it.

## 2. Build the .docx (ATS-safe)

Copy `scripts/build_resume.js` and fill in the content. Key constraints:

- US Letter: `size: { width: 12240, height: 15840 }` in twips.
- Standard font, Calibri or Georgia, 10 to 11pt body.
- Single column. No tables for content the ATS must read.
- Real bullets via a `numbering` config with `LevelFormat.BULLET`, never typed characters.
- Section headings as bold paragraphs with a bottom border, not heading styles with odd fonts.
- `keepNext: true` on every heading, company line, and role line, so a heading never strands
  alone at the bottom of a page.
- No `\n` inside a TextRun. One `Paragraph` per line.
- No em or en dashes anywhere.

```bash
node build_resume.js
```

## 3. Patch the bullet indentation

The `docx` library writes a wide default indent into `word/numbering.xml` that wastes horizontal
space and looks wrong on a dense resume. Unzip, patch, rezip:

```bash
rm -rf unz && mkdir unz && cd unz
unzip -o -q ../resume.docx
python3 -c "
p='word/numbering.xml'; s=open(p).read()
s=s.replace('w:left=\"720\" w:hanging=\"360\"','w:left=\"216\" w:hanging=\"216\"')
open(p,'w').write(s)"
zip -q -r ../resume.docx . -x '.*'
cd ..
```

Do this after every rebuild, since rebuilding overwrites the patch.

## 4. Validate programmatically (every build)

```bash
python3 scripts/validate_resume.py resume.docx --source ledger.txt --jd jd.txt --banned banned.txt
```

Four checks:

- **Dash check** must PASS.
- **Numeric fact-check** must PASS. Every number in the resume must appear in the ledger. A number
  that is not there is either a hallucination or a confirmed fact you forgot to write down. Fix the
  right one of those two things. Never fix it by deleting the check.
- **Banned phrase check** must PASS. Retired claims never reappear.
- **Keyword coverage** is reported, not enforced.

## 5. Close the keyword loop

Read the missing-keyword list and sort each term into one of three buckets:

- **Honestly true and simply absent.** Add it. Usually a wording choice: the resume says "clients"
  where the JD says "customers", or the resume says "coaching" where the JD says "mentoring".
  Adjust the phrasing and rerun.
- **True but only in a weaker form.** Add the weaker form and let it read as the weaker form.
- **Not true.** Leave it missing. Report it as a gap in the delivery summary. Never place a term
  the candidate cannot defend.

Iterate until every remaining missing term is genuinely a gap. Two passes of pure honest rewording
usually closes most of the list. Whatever is left after that is almost always a real gap, and that
is the correct place to stop. A resume at full keyword coverage is usually a resume that started
lying somewhere.

## 6. Render the PDF and look at it (every build)

The PDF is the final deliverable, so always eyeball it.

```bash
soffice --headless --convert-to pdf resume.docx
pdftoppm -jpeg -r 100 resume.pdf page
ls page-*.jpg
```

View every page image. Check: one to two pages, no orphaned headings, no section split awkwardly
across the page break, no line overflowing the margin, dates aligned, no widowed single-word lines
at the bottom of a bullet. If a heading is stranded, add `keepNext` and rebuild.

## 7. Multi-persona review (every build)

Run all four personas in `persona-review.md`. Fix findings, then repeat steps 3, 4, and 6 until
clean. Verification is not skipped for small changes; a one-line edit can push a page break.

## 8. Deliver

Copy both the PDF and the .docx to the output directory and present them, PDF first. Then write
the delivery summary described in `SKILL.md`.
