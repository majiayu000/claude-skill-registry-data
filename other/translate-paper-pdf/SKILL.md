---
name: translate-paper-pdf
description: Translate born-digital academic PDF papers into Chinese monolingual and bilingual PDFs with PDFMathTranslate-next/BabelDOC while preserving the original page structure, figures, tables, and formulas as far as the engine permits. Use when Codex is asked to translate an English paper, arXiv PDF, conference paper, thesis chapter, or research report into Chinese without flattening it into plain text, especially when terminology consistency, glossary control, page rendering, layout comparison, code/reference protection, or a fidelity-risk report is required.
---

# Translate Paper PDF

## Overview

Use PDFMathTranslate-next as the supported front end to BabelDOC. Treat translation generation and fidelity acceptance as separate stages: a command can succeed while code, references, author metadata, or dense appendix layouts remain unsafe.

## Workflow

1. Confirm the source boundary.
   - Work only with a user-provided, public, or otherwise authorized PDF.
   - Prefer born-digital PDFs. For scanned PDFs, pass `--scanned` and expect weaker layout fidelity.
   - Put large outputs, renders, and logs in the paper project or run directory, not in a planning repository.
2. Check the runtime:

```powershell
python C:\Users\Administrator\.codex\skills\translate-paper-pdf\scripts\translate_paper_pdf.py doctor
```

3. If `pdf2zh-next` is missing, reuse an existing project environment or create an isolated one. Read `references/engine-setup.md` before installing or configuring a non-default engine.
4. Prepare a paper-specific glossary. Copy `assets/glossary-template.csv`, keep method/model/dataset names unchanged when appropriate, and validate every high-impact term. Disable automatic glossary extraction by default.
5. Choose a profile:
   - `quick-read`: generate mono/dual PDFs and structural checks for comprehension.
   - `fidelity-review`: also render source and translated pages and require manual page-level review. Read `references/quality-contract.md` before claiming fidelity.
6. Run the wrapper:

```powershell
python C:\Users\Administrator\.codex\skills\translate-paper-pdf\scripts\translate_paper_pdf.py translate paper.pdf `
  --output-dir output\paper-zh `
  --profile fidelity-review `
  --glossary paper-glossary.csv
```

7. Inspect `run-manifest.json` and `qa-report.md`. For `fidelity-review`, visually inspect every rendered page or complete contact sheets, with focused checks on all priority pages.
8. Report both the usable artifacts and their limitations. Never describe `manual_review_required`, `partial`, or `failed` QA as fidelity-passed.

Re-run QA without retranslating when outputs already exist:

```powershell
python ...\translate_paper_pdf.py qa paper.pdf `
  --translated output\paper.zh.mono.pdf `
  --translated output\paper.zh.dual.pdf `
  --output-dir output `
  --profile fidelity-review
```

## Runtime Selection

The wrapper discovers the engine in this order:

1. `--pdf2zh-cli <path>`;
2. `PDF2ZH_CLI` environment variable;
3. `pdf2zh` / `pdf2zh.exe` on `PATH`.

The default engine is `siliconflowfree`, which sends paper text to an external translation service. Obtain user approval before sending private, unpublished, confidential, or restricted text to any external provider. Use a local or user-approved configured engine when external transfer is not allowed.

For non-default engines, pass only the engine selector and an existing user-managed config:

```powershell
python ...\translate_paper_pdf.py translate paper.pdf --output-dir out `
  --engine openaicompatible --config-file C:\private\pdf2zh-config.toml
```

Do not read, print, copy, commit, or place API keys in command arguments, manifests, task traces, or the skill bundle.

## Output Contract

Each completed run should contain:

- Chinese monolingual PDF when enabled;
- bilingual PDF when enabled;
- `run-manifest.json` with source/output hashes, versions, page counts, profile, and structural QA status;
- `qa-report.md` with high-risk pages, render locations, and manual review requirements;
- rendered pages under `qa/rendered/` for `fidelity-review` when Poppler is available.

The wrapper preserves the source PDF and never overwrites it.

## Hard Gates

- Fail if the source is missing, not a PDF, or the engine returns nonzero.
- Fail if the engine reports success but no expected PDF output is found.
- Mark structural QA failed when mono/dual page counts unexpectedly differ from the source.
- Keep `manual_review_required` until visual checks cover every page in `fidelity-review`.
- Treat translated code, altered citations/bibliography, corrupted author affiliations, clipped tables, covered text, missing formulas, and unreadable dense appendices as fidelity failures.
- Keep figure-internal English text when translating it safely would require reconstructing the figure; disclose this instead of inventing replacements.

## Resources

- `scripts/translate_paper_pdf.py`: doctor, translation orchestration, existing-output QA, manifest generation, risk-page detection, rendering, and QA report.
- `scripts/bootstrap_pdf2zh.py`: install the tested `pdf2zh-next` version into an isolated virtual environment.
- `references/engine-setup.md`: engine selection, installation, configuration, and privacy boundaries.
- `references/quality-contract.md`: acceptance profiles, mandatory visual checks, and allowed claims.
- `assets/glossary-template.csv`: paper-level terminology template.
