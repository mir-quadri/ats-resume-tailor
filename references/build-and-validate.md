# Build and Validate

Step-by-step commands and process for the full workflow.

## Extracting the source

```bash
# Extract text from a PDF resume
pdftotext resume.pdf resume.txt

# Or convert a DOCX
python3 -c "from docx import Document; doc = Document('resume.docx'); print('\n'.join(p.text for p in doc.paragraphs))" > resume.txt
```

## Building the fact ledger

1. Open the source resume text.
2. Transcribe every fact into a plain text file, grouped by role.
3. Use the template in `assets/fact_ledger_template.md`.
4. Save as `ledger.txt`.

Example:
```
# Experience

## Role 1: Senior Software Engineer at Acme (2020-2023)
- Title: Senior Software Engineer
- Dates: January 2020 to December 2023
- Company: Acme Corp
- The team reduced deployment time from 2 hours to 15 minutes
- Built real-time event pipeline
- Led code review practice for 4 engineers
```

## Building the JD file

```bash
# Save the job description as plain text
# Remove HTML, keep just the text
# Save as jd.txt
```

## Running the validator

```bash
# Full validation
python3 scripts/validate_resume.py resume.docx --source ledger.txt --jd jd.txt --banned banned.txt

# Exit code 0 = all checks pass
# Exit code 1 = at least one check failed
```

The validator checks:
- **Dashes:** No em-dashes or en-dashes.
- **Numeric facts:** Every number in the resume appears in the ledger (approximately).
- **Banned phrases:** No banned words appear.
- **Keyword coverage:** Informational report on JD keyword matching.

## Building the DOCX

Using the Node.js template in `scripts/build_resume.js`:

```bash
# Install docx package (one-time)
npm install docx

# Edit build_resume.js with the candidate's information
# Fill in: name, roles, achievements, skills, education

# Build the DOCX
node scripts/build_resume.js > resume.docx
```

Or use Microsoft Word / Google Docs with these rules:
- Single column
- Standard font (Arial, Calibri, Times New Roman)
- No em-dashes or en-dashes
- Real bullet points
- Standard section headings

## Rendering to PDF

```bash
# Convert DOCX to PDF using LibreOffice
soffice --convert-to pdf resume.docx

# Render pages to images for visual inspection
pdftoppm resume.pdf page -jpeg

# Review: page-1.jpg, page-2.jpg
```

## Creating the banned list

After the candidate confirms gaps, create `banned.txt` with phrases to exclude:

```
grew the business
synergy
thought leader
```

## Full workflow

```bash
# 1. Extract text
pdftotext source.pdf source.txt

# 2. Build ledger
# (manual, use template)
# Save as ledger.txt

# 3. Save JD
# (manual, copy-paste)
# Save as jd.txt

# 4. Build resume
node scripts/build_resume.js > resume.docx

# 5. Build banned list
echo "grew the business" > banned.txt

# 6. Validate
python3 scripts/validate_resume.py resume.docx --source ledger.txt --jd jd.txt --banned banned.txt

# 7. Render to PDF
soffice --convert-to pdf resume.docx

# 8. Inspect
pdftoppm resume.pdf page -jpeg
open page-1.jpg
```

## Exit codes

```bash
# All checks pass
if python3 scripts/validate_resume.py resume.docx --source ledger.txt; then
  echo "Resume is valid"
fi

# Check failed
if ! python3 scripts/validate_resume.py resume.docx --source ledger.txt; then
  echo "Resume has issues"
  exit 1
fi
```
