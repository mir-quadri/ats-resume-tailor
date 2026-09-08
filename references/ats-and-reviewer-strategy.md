# ATS and Reviewer Strategy

Design the resume for both the parser and the human.

## ATS parsing

The ATS is a keyword matcher. It looks for:
- Job titles that match the role.
- Skills and technologies named explicitly.
- Years of experience in the function.
- Degree and institution names (for educational requirements).

**To pass the ATS:**
- Use the exact titles and skill names from the JD.
- Include the years of experience clearly: "5 years of Python" not "proficient in Python."
- Name technologies directly: "AWS", "Kubernetes", "Salesforce". Do not say "cloud platforms."
- Spell out acronyms the first time: "Amazon Web Services (AWS)" gives two search targets.

## Reviewer parsing

The recruiter reads your resume in 6 seconds. They are looking for:
- Does your most recent role match the JD?
- Do you have the required experience in the core function?
- Do you have any red flags (big employment gaps, job-hopping, unrelated background)?

**Top third matters.** The first role, first achievement in the summary, first skill in the skills section—these get the most attention. Put your best match there.

**Section order.** Standard order is:
1. Summary (if used)
2. Experience (most recent first)
3. Skills
4. Certifications (if relevant)
5. Education

Do not reorder to "optimize." The standard order is what both the ATS and the recruiter expect.

## No em-dashes

Em-dashes and en-dashes are ATS poison and a common "AI wrote this" tell.
- ✗ "Led a data team—of 3 engineers—to ship a real-time pipeline"
- ✓ "Led a data team of 3 engineers to ship a real-time pipeline"

Use periods, commas, or "to" for ranges:
- ✗ "2020–2023"
- ✓ "2020 to 2023"

## Keyword mapping

For each major requirement in the JD:
1. Find your strongest ledger fact that matches.
2. Reframe it using company language (from research).
3. Include the exact skill or title name from the JD.

Example:
- JD asks: "Experience with real-time data pipelines."
- Your ledger: "Built batch data pipeline on AWS Glue, 2021."
- Reframe: "Designed AWS-based data pipeline (transitioning from batch to event-driven for real-time processing)."
  - This is honest (you did build a pipeline, you know about real-time even if your hands-on was limited).
  - It includes the exact technology (AWS).
  - It flags the gap (batch not real-time) without lying.

Never manufacture experience you do not have. Reframe to emphasize relevance and mitigate gaps, but stay inside your ledger.

## Formatting for parsing

- **Bold or underline for section headings.** Standard: "EXPERIENCE", "SKILLS".
- **Real bullet points.** Not dashes, not asterisks. Proper Unicode bullets or the standard bullet character.
- **No tables, no text boxes, no unusual fonts.** Stick to Arial, Calibri, or Times New Roman.
- **Single column.** The ATS cannot parse multi-column layouts.
- **One job title per line.** Do not nest or abbreviate.

Example format:
```
EXPERIENCE

Senior Software Engineer
Company Name | Jan 2020 to Present

• Built a real-time data pipeline using Kafka and Spark, processing 10M events per day.
• Led migration from batch to event-driven architecture, reducing latency by 60%.
```

## Ranking within experience

List roles in reverse chronological order (most recent first). Within each role, order bullets by:
1. Relevance to the JD.
2. Scale or impact.
3. Recency.

Put the most relevant achievement first, even if it is not your biggest win.
