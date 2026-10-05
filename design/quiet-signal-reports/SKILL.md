---
name: quiet-signal-reports
description: Create, revise, render, or visually audit Quiet Signal A4 long-form PDF reports from source material using editable HTML/CSS, source-backed content, and full-page rendering QA. Use for detailed reports; not for slides or Xiaohongshu summaries.
---

# Quiet Signal Reports

Produce the finished report, not a design plan. Treat editable HTML/CSS as the source of truth, PDF as the deliverable, and rendered page images as the visual acceptance evidence.

## Read before working

1. Read `../quiet-signal-design/references/SPEC.md` completely for the Quiet Signal core visual language. If the base skill is unavailable, report the missing dependency instead of inventing a replacement style.
2. Read `references/SPEC.md` completely for report-specific content, typography, page, source, and QA rules.
3. For a new report or substantial redesign, read `references/APPROVED.md` and `references/REJECTED.md`.
4. Open the relevant full implementation listed in `references/IMPLEMENTATIONS.md`. Read its HTML and CSS, inspect its demo image, and use it as production evidence rather than a fixed template.

## Workflow

1. Establish the report question, audience, evidence boundary, required sections, and source ledger.
2. Write the complete long-form content first. Preserve necessary explanation, caveats, methods, and source distinctions; do not compress the work into social-media takeaways.
3. Choose each page relationship from its content: continuous prose, sequential argument, true parallel comparison, figure plus explanation, evidence table, or full-bleed image. Keep one obvious primary reading path.
4. Implement directly in editable HTML/CSS. Use local assets and relative paths. Do not add a schema, router, registry, planner, compiler, candidate matrix, or review UI.
5. Render the PDF with `scripts/render_report.mjs`. Fix overflow through editing or page structure; never solve it by shrinking required text below the limits in `references/SPEC.md`.
6. Render every PDF page and a contact sheet with `scripts/render_review.py`. Inspect the complete contact sheet, then inspect pages with dense text, tables, images, bottom notes, and closing references at full size.
7. Deliver the HTML/CSS source, source ledger, PDF, page PNGs, and contact sheet in the user's chosen project directory. Report any unverified source or visual boundary explicitly.

## Commands

Run from this skill directory:

```bash
node scripts/render_report.mjs \
  --input references/implementations/lunar-microbe-longform/index.html \
  --output /path/to/output/quiet-signal-lunar-microbe-longform-report.pdf \
  --expected-pages 26

python3 scripts/render_review.py \
  --pdf /path/to/output/quiet-signal-lunar-microbe-longform-report.pdf \
  --output-dir /path/to/output/review
```

Use `node scripts/render_report.mjs --help` and `python3 scripts/render_review.py --help` for options.

## Completion gate

A report is not complete when the prose, rules, or HTML merely exist. It is complete only when the final PDF is source-backed, text remains selectable, every page has been rendered, no page overflows or clips, and the full visual sequence has been inspected.
