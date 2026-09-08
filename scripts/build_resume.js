/**
 * ATS-safe resume builder template.
 *
 * Usage:
 *   npm install docx
 *   node build_resume.js
 *   (then run the numbering patch from references/build-and-validate.md)
 *
 * Replace everything in the CONTENT section. Do not change the helpers unless you have a reason:
 * they encode the ATS-safe formatting rules (single column, real bullets, keepNext on headings,
 * US Letter, standard fonts, no dashes).
 */
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat,
  convertInchesToTwip, BorderStyle,
} = require('docx');

const OUT = 'resume.docx';
const FONT = 'Calibri';
const BODY = 20; // half-points, so 20 = 10pt
const NAME = 30; // 15pt

// ---------------------------------------------------------------- helpers

/** A bulleted paragraph. Pass strings, or {text, bold} objects for inline bold lead-ins. */
function bullet(runs, size = BODY) {
  return new Paragraph({
    numbering: { reference: 'bullets', level: 0 },
    spacing: { after: 40, line: 240 },
    children: runs.map(r =>
      typeof r === 'string'
        ? new TextRun({ text: r, font: FONT, size })
        : new TextRun({ ...r, font: FONT, size })),
  });
}

/** A plain paragraph. opts: {bold, italics, align, before, after, size, keepNext} */
function line(text, opts = {}) {
  return new Paragraph({
    keepNext: !!opts.keepNext,
    alignment: opts.align || AlignmentType.LEFT,
    spacing: {
      before: opts.before || 0,
      after: opts.after === undefined ? 40 : opts.after,
      line: 240,
    },
    children: [new TextRun({
      text, font: FONT, size: opts.size || BODY,
      bold: !!opts.bold, italics: !!opts.italics,
    })],
  });
}

/** A section heading: bold, underlined by a border, always kept with what follows. */
function heading(text) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: 140, after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '444444', space: 1 } },
    children: [new TextRun({ text, font: FONT, size: 21, bold: true })],
  });
}

/** Job title on the left, dates flush right via a right tab stop. */
function roleLine(title, dates) {
  return new Paragraph({
    keepNext: true,
    tabStops: [{ type: 'right', position: 10080 }],
    spacing: { before: 30, after: 40, line: 240 },
    children: [
      new TextRun({ text: title, font: FONT, size: BODY, bold: true }),
      new TextRun({ text: '\t' + dates, font: FONT, size: BODY, bold: true }),
    ],
  });
}

// ---------------------------------------------------------------- content

const children = [];

// Contact block. Keep it in the document body, never in a header/footer.
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 20 },
  children: [new TextRun({ text: 'CANDIDATE NAME', font: FONT, size: NAME, bold: true })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 20 },
  children: [new TextRun({
    text: 'City, State | Phone | Email | LinkedIn | Portfolio',
    font: FONT, size: 18,
  })],
}));
// Headline: the target title (or an honest variant) plus the positioning tag. ATS reads this.
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({
    text: 'TARGET TITLE | POSITIONING TAG FROM THE CHOSEN LANE',
    font: FONT, size: 18, bold: true,
  })],
}));

children.push(heading('SUMMARY'));
children.push(line(
  'Three to five lines. Years, domain, the value proposition tuned to THIS job description. ' +
  'Every sentence should serve the lane chosen in positioning-lanes.md. No generic openers.'
));

// The fastest way to signal fit. Map the JD top asks to real evidence, strongest first.
children.push(heading('WHAT I BRING TO THIS ROLE'));
children.push(bullet([
  { text: 'Bold lead-in naming the JD requirement. ', bold: true },
  'Then the candidate evidence that proves it, with owned numbers from the ledger.',
]));

children.push(heading('CORE CAPABILITIES'));
children.push(bullet(['Grouped, keyword-dense, all true. One grouping per line.']));

children.push(heading('PROFESSIONAL EXPERIENCE'));
children.push(line('EMPLOYER | City, State', { bold: true, before: 60, keepNext: true }));
children.push(roleLine('Exact Title From The Source Resume', 'Mon YYYY to Mon YYYY'));
children.push(bullet(['Outcome first, then how. Strongest and most relevant bullet leads the role.']));

children.push(heading('EARLIER CAREER'));
children.push(line('Older roles compressed to one or two lines.'));

children.push(heading('EDUCATION'));
children.push(line('Institution, Degree, Field'));

children.push(heading('CERTIFICATIONS'));
children.push(line('Cert | Cert | Cert | Anything in progress, labeled as in progress'));

// ---------------------------------------------------------------- document

const doc = new Document({
  numbering: {
    config: [{
      reference: 'bullets',
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: '\u2022',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 216, hanging: 216 } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter
        margin: {
          top: convertInchesToTwip(0.45), bottom: convertInchesToTwip(0.45),
          left: convertInchesToTwip(0.55), right: convertInchesToTwip(0.55),
        },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log('built ' + OUT);
});
