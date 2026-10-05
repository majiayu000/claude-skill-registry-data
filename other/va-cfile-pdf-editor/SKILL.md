---
name: va-cfile-pdf-editor
description: Vision-first grounded PDF extraction and deterministic page editing workflow. VA C-file is the default profile, but the same pipeline supports general-purpose document extraction with entity/event evidence anchors and citation-bound timelines.
---

# VA C-File PDF Editor

## Purpose
Produce a case-ready grounded extraction bundle with this locked order:
1. Render raw pages.
2. Run Codex visual analysis on raw pages.
3. Derive deterministic, entity-bound edit intents from raw analysis.
4. Optional review gate to approve/reject/override entity boxes.
5. Apply targeted page edits.
6. Run Codex visual analysis on edited pages.
7. Reconcile raw vs edited extraction.
8. Build chronologies, citations, timelines, QA report.

Never run blind edits before raw visual analysis.
Default annotation policy is entity-level, not broad region-level. Generic broad boxes are fallback-only and must be explicitly flagged in uncertainties.

### Domain Notes
- VA profile: use `legal` and `medical` event types for canonical VA timelines.
- General-purpose profile: `event_type` and `chronology_role` can be any non-empty domain label (e.g. `invoice`, `policy`, `lab_result`, `contract`, `shipment`).
- All entity-level extractions should be evidence-linked (`entity_id` + bbox + quote-backed event evidence rows).

## Output Bundle
Write outputs to:
- `output/pdf_cases/<case_id>/manifest.json`
- `output/pdf_cases/<case_id>/pages/raw/*.png`
- `output/pdf_cases/<case_id>/pages/edited/*.png`
- `output/pdf_cases/<case_id>/pages/edited/edit_manifest.json`
- `output/pdf_cases/<case_id>/edits/edit_intents.json`
- `output/pdf_cases/<case_id>/edits/edit_intents_final.json`
- `output/pdf_cases/<case_id>/edits/review_audit.json`
- `output/pdf_cases/<case_id>/extractions/raw/page_*.json`
- `output/pdf_cases/<case_id>/extractions/edited/page_*.json`
- `output/pdf_cases/<case_id>/extractions/reconciled/page_*.json`
- `output/pdf_cases/<case_id>/extractions/reconciliation_report.json`
- `output/pdf_cases/<case_id>/chronologies/legal_chronology.md`
- `output/pdf_cases/<case_id>/chronologies/medical_chronology.md`
- `output/pdf_cases/<case_id>/chronologies/all_events_chronology.md`
- `output/pdf_cases/<case_id>/chronologies/legal_timeline.mmd`
- `output/pdf_cases/<case_id>/chronologies/medical_timeline.mmd`
- `output/pdf_cases/<case_id>/chronologies/all_events_timeline.mmd`
- `output/pdf_cases/<case_id>/chronologies/event_type_breakdown.md`
- `output/pdf_cases/<case_id>/citations/citation_map.json`
- `output/pdf_cases/<case_id>/qa/quality_report.md`

## Workflow Commands
### 1) Render PDFs to raw PNG pages
```bash
uv run python scripts/render_pdf_pages.py \
  --input /path/to/case_pdfs \
  --case-id CASE_001 \
  --out output/pdf_cases/CASE_001
```

### 2) Analyze raw pages (Codex vision normalization)
```bash
uv run python scripts/analyze_raw_pages_codex.py \
  --pages-dir output/pdf_cases/CASE_001/pages/raw \
  --out-dir output/pdf_cases/CASE_001/extractions/raw \
  --codex-findings output/pdf_cases/CASE_001/extractions/raw/codex_findings.json
```

### 3) Derive deterministic edit intents
```bash
uv run python scripts/derive_edit_intents.py \
  --raw-extractions output/pdf_cases/CASE_001/extractions/raw \
  --out output/pdf_cases/CASE_001/edits/edit_intents.json
```

### 4) Resolve intents (review file optional)
```bash
uv run python scripts/review_annotation_intents.py \
  --edit-intents output/pdf_cases/CASE_001/edits/edit_intents.json \
  --out output/pdf_cases/CASE_001/edits/edit_intents_final.json \
  --review-file output/pdf_cases/CASE_001/edits/annotation_review.json
```

If no `--review-file` is supplied, this step still runs in auto mode:
- high-confidence intents auto-apply
- review-required intents are skipped

### 5) Apply page edits
```bash
uv run python scripts/apply_page_edits.py \
  --pages-dir output/pdf_cases/CASE_001/pages/raw \
  --edit-intents output/pdf_cases/CASE_001/edits/edit_intents_final.json \
  --out-dir output/pdf_cases/CASE_001/pages/edited
```

### 6) Analyze edited pages (Codex vision normalization)
```bash
uv run python scripts/analyze_edited_pages_codex.py \
  --pages-dir output/pdf_cases/CASE_001/pages/edited \
  --out-dir output/pdf_cases/CASE_001/extractions/edited \
  --codex-findings output/pdf_cases/CASE_001/extractions/edited/codex_findings.json \
  --final-intents output/pdf_cases/CASE_001/edits/edit_intents_final.json
```

### 7) Reconcile two-pass extraction
```bash
uv run python scripts/reconcile_extractions.py \
  --raw-dir output/pdf_cases/CASE_001/extractions/raw \
  --edited-dir output/pdf_cases/CASE_001/extractions/edited \
  --out-dir output/pdf_cases/CASE_001/extractions/reconciled
```

### 8) Build case bundle chronologies + citations + timelines + QA
```bash
uv run python scripts/build_case_bundle.py \
  --case-id CASE_001 \
  --base-dir output/pdf_cases/CASE_001 \
  --reconciled-dir output/pdf_cases/CASE_001/extractions/reconciled
```

### 9) Validate bundle
```bash
uv run python scripts/validate_bundle.py \
  --base-dir output/pdf_cases/CASE_001
```

## Required Tooling
- `pdftoppm` for PDF rendering.
- Python 3.9+.
- `Pillow` for deterministic image edits (`pip install Pillow`).

No Tesseract/traditional OCR fallback is part of this skill.
Raw/edited Codex findings should follow `schemas/codex_findings_v2.schema.json`.

## Iteration 2 Research Track (Segmentation)
Research-only benchmark assets are available for segmentation-assisted parsing experiments.

- Script: `scripts/benchmark_segmentation_iteration2.py`
- Config: `research/configs/segmentation_benchmark_iteration2.json`
- Report: `research/segmentation_iteration2.md`
- Decision memo: `research/segmentation_decision_memo.md`

This track is gated by feature flag `SEGMENTATION_RESEARCH_V2` and does not modify the v1 production flow.

## References
- `references/jerome_workflow_playbook.md`
- `references/extraction_schema.md`
- `references/chronology_rules.md`
- `references/editor_profiles.md`
