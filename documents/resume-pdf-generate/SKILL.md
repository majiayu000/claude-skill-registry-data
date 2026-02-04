---
name: resume-pdf-generate
description: Generate the resume PDF with the existing Puppeteer-based script and blank-page trimming. Use when asked to regenerate the resume PDF, validate print styling, or troubleshoot PDF output in dev/apps/resume.
---

# Resume PDF Generate

## Overview
Render the resume app to PDF via Puppeteer and trim blank pages using the project scripts.

## Workflow
1. Run the PDF generator: `cd dev/apps/resume && pnpm generate:pdf`.
2. Find the output at `dev/apps/resume/public/aleksi-asikainen-resume.pdf`.
3. If layout or paging changes are needed, inspect `dev/apps/resume/scripts/pdf/cli.ts` and `dev/apps/resume/scripts/pdf/trim-blank-pages.sh`.
