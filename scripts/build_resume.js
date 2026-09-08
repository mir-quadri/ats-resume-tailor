#!/usr/bin/env node
/**
 * ATS-safe resume builder template.
 * Uses the docx package to build a Word document.
 * Copy this template and fill in with candidate data.
 *
 * Usage: node build_resume.js > resume.docx
 */

const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  AlignmentType,
  UnderlineType,
} = require('docx');

// Build the document
const doc = new Document({
  sections: [
    {
      properties: {},
      children: [
        // Name and title
        new Paragraph({
          text: 'CANDIDATE NAME',
          style: 'Heading1',
          alignment: AlignmentType.CENTER,
          spacing: { after: 0 },
        }),
        new Paragraph({
          text: 'Target Title | City, State',
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
        }),

        // Contact (optional)
        new Paragraph({
          text: 'email@example.com | (555) 123-4567',
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
        }),

        // Summary
        new Paragraph({
          text: 'SUMMARY',
          style: 'Heading2',
          spacing: { after: 100 },
        }),
        new Paragraph({
          text: 'Brief professional summary emphasizing positioning lane and top achievements.',
          spacing: { after: 200 },
        }),

        // Experience
        new Paragraph({
          text: 'EXPERIENCE',
          style: 'Heading2',
          spacing: { after: 100 },
        }),
        new Paragraph({
          text: 'Job Title',
          run: new TextRun({ bold: true }),
          spacing: { after: 0 },
        }),
        new Paragraph({
          text: 'Company Name | Jan 2020 to Present',
          spacing: { after: 100 },
        }),
        new Paragraph({
          text: 'Achievement or responsibility using verified facts only.',
          spacing: { after: 50 },
        }),
        new Paragraph({
          text: 'Metric or outcome tied to company goals.',
          spacing: { after: 200 },
        }),

        // Skills
        new Paragraph({
          text: 'SKILLS',
          style: 'Heading2',
          spacing: { after: 100 },
        }),
        new Paragraph({
          text: 'List tools and skills with recent usage year.',
          spacing: { after: 200 },
        }),

        // Certifications
        new Paragraph({
          text: 'CERTIFICATIONS',
          style: 'Heading2',
          spacing: { after: 100 },
        }),
        new Paragraph({
          text: 'Certification Name, Issuer, Year',
          spacing: { after: 200 },
        }),

        // Education
        new Paragraph({
          text: 'EDUCATION',
          style: 'Heading2',
          spacing: { after: 100 },
        }),
        new Paragraph({
          text: 'Degree, Institution, Year',
          spacing: { after: 200 },
        }),
      ],
    },
  ],
});

// Write to stdout or file
Packer.toBuffer(doc).then((buffer) => {
  process.stdout.write(buffer);
});
