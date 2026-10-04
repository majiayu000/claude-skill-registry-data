---
name: thesis-figure-pipeline
description: Generate thesis or paper figures from experiment tables with reproducible plotting scripts, CJK font handling, stable label mappings, PNG/PDF output, LaTeX figure sync, summaries, and visual QA. Use when Codex is asked to create, refresh, audit, or synchronize academic figures.
---

# Thesis Figure Pipeline

Use this skill to turn experiment outputs into paper-ready figures without losing traceability.

## Workflow

1. Locate source tables and confirm the metric definitions.
2. Create or update a plotting script with explicit:
   - input paths;
   - output directory;
   - LaTeX figure directory;
   - label mappings;
   - method/model order;
   - color palette;
   - font setup.
3. Generate both PNG and PDF:
   - use high-DPI PNG for quick inspection;
   - preserve vector PDF when using matplotlib;
   - convert raster screenshots to single-page PDF only when necessary.
4. Write a compact summary file with sample counts and aggregates.
5. Sync only formal figures into the LaTeX figure directory.
6. Compile or render the target paper pages and visually inspect the inserted figure.

## Guardrails

- Do not manually edit final figure images unless the edit is documented and reproducible.
- Do not mix preview figures and formal thesis figures in the same target directory.
- Do not change metric labels or method order silently.
- Check CJK text, tick labels, legend placement, and page fit in the final PDF.

## Useful Resources

- Read `references/figure-checklist.html` before final signoff.
- Use `assets/figure-manifest.html` to record figure provenance.
