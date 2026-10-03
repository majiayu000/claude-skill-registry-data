---
name: papers-reading-skill
description: Evidence-grounded AI research workflow for turning supplied economics, finance, management, and social-science papers or structured records into versioned PaperReading artifacts. Use when Codex must ingest text, Markdown, or a text-based PDF; separate source-grounded claims from researcher analysis; bind findings to evidence IDs and locators; review extraction candidates; migrate v0.2 PaperRecord JSON; validate or verify a v0.3 PaperPackage; generate research extensions; export reviewable JSON or Markdown; or safely update a compatible 13-field literature workbook.
---

# PaperReading Core Adapter

## Workflow

1. Establish the supplied-source boundary. Identify which title, author, journal, date, DOI, page, section, table, figure, equation, appendix, and full-text surfaces are actually available.
2. For UTF-8 text, Markdown, or a text-based PDF, run `paperreading ingest <source> --output <document.json>`. Use the resulting source, page, section, block, character-range, and hash metadata; do not invent locators. A scanned PDF requires a separately authorized OCR workflow.
3. Read the abstract and introduction, theory or hypotheses, data and variables, research design, baseline results, mechanisms, heterogeneity, robustness or endogeneity checks, conclusion, and relevant appendix material.
4. Build a v0.3 `PaperPackage` using `references/paper-record.md`. When provider output is available, preserve it through `extract`, `review`, and `finalize`; never bypass unresolved Candidate or Conflict state. Keep `GroundedPaperRecord`, `EvidenceSpan`, and `ResearchAnalysis` conceptually and structurally separate.
5. For an existing v0.2 record, run `paperreading migrate <record.json> --output <package.json>` rather than rewriting it manually. Preserve the resulting migration notes and unverified state.
6. Run `paperreading validate <package.json>`. When a matching `PaperDocument` exists, also run `paperreading verify <package.json> --document <document.json> --strict --output <verified.json>`.
7. Resolve every validation error before export. Keep partial or failed verification visible; never upgrade a package to verified by assertion.
8. Produce only the user-selected output. Load `references/reading-fields.md` when reviewing the legacy 13-field projection or workbook style.

## Evidence protocol

- Record a source claim only when the paper explicitly states it and bind it to at least one evidence ID.
- Record a finding only when supplied text, table, figure, equation, or appendix material supports it.
- Keep researcher or AI-assisted assessment outside the source-grounded record.
- Preserve null results, caveats, sample limits, identification limits, conflicts, and unresolved fields.
- Never fabricate a quotation, page, section, block, table, column, figure, equation, appendix, variable, model, test, ranking, or causal claim.
- Treat traceability as locator specificity, not truth, study quality, causal validity, or external validity.
- Treat source-content verification as a resolution check against the supplied document, not proof that the paper's methods or conclusions are correct.
- Do not translate one journal-ranking system into another. Record only independently verified labels with their source and version boundary.

## Causal and analysis boundaries

- Use causal language only when an eligible design and an explicit identification strategy support it.
- Preserve stronger wording made by the paper as a source claim when necessary, but keep the PaperReading assessment and caveats separate.
- Put proposed research extensions in `ResearchAnalysis`; never present them as paper findings.
- Ground each extension in a reported limitation, evidence boundary, contradiction, or identification constraint, and include at least one executable design element.

## CLI operations

Initialize a local project and ingest a supported source:

```bash
paperreading init
paperreading ingest source.md --output document.json
```

Replay an auditable extraction, review it, and finalize only when it is ready:

```bash
paperreading extract document.json \
  --provider-manifest extraction-manifest.json \
  --output bundle.json
paperreading review bundle.json \
  --decisions review-decisions.json \
  --output reviewed.json
paperreading finalize reviewed.json \
  --document document.json \
  --output package.json
```

Migrate a v0.2 record:

```bash
paperreading migrate record.json --output package.json
```

Validate and, when the matching document exists, verify a v0.3 package:

```bash
paperreading validate package.json
paperreading verify package.json \
  --document document.json \
  --strict \
  --output verified-package.json
```

Review or export without changing a workbook:

```bash
paperreading project package.json
paperreading export package.json review.md --format markdown
paperreading export package.json package.normalized.json --format json
```

Append through the compatibility projection only after the user authorizes the workbook destination:

```bash
paperreading export package.json literature.xlsx --format excel --sheet 中文
```

The legacy `scripts/append_paper_reading.py` entry point remains a compatibility wrapper for existing 13-field JSON. Prefer the CLI for new workflows.

## Current implementation boundary

- Core ingestion supports UTF-8 text, Markdown, and optional PDFs that already contain an extractable text layer.
- Core PDF ingestion does not implement OCR, page geometry, table reconstruction, or figure extraction.
- The shipped JSON Provider is a deterministic replay adapter. It does not call a hosted model; real model adapters remain roadmap work.
- Draft conflicts and unresolved fields require explicit review before finalization.
- If the host can inspect another supplied format, record that review boundary honestly, but do not claim `paperreading verify` ran without a matching `PaperDocument`.
- Batch processing, SQLite search, cross-paper synthesis, gap discovery, and method-specific auditing are not implemented.

## Mutation rules

- Produce draft, validation, or stdout output when no destination is explicitly provided.
- Do not overwrite JSON or Markdown unless the user requests replacement and `--force` is used.
- For Excel, require an explicit path or existing `PAPER_READING_WORKBOOK` configuration.
- Treat `duplicate_skipped` as a successful no-op and report the existing worksheet row.
- Treat schema mismatch, unresolved evidence, failed validation, locked workbook, or write error as a hard stop.
- After a successful Excel append, report the worksheet, appended row, and timestamped backup path.

If the `paperreading` command is unavailable, report that the Core package and any required exporter extra must be installed. Do not bypass the validator or reimplement workbook mutation ad hoc.
