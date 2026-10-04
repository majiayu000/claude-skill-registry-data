---
name: notion-hf-curator
description: End-to-end Notion-to-Hugging Face dataset and model curation workflow for SCBE repositories (export, QA, comparison, GitHub Actions, publishing).
---

# Notion-to-HF Curator

Use when a user asks to turn Notion content into an AI-ready dataset and sync to Hugging Face.

## Prereqs

- `NOTION_TOKEN` or `NOTION_API_KEY` (Notion integration token).
- `HF_TOKEN` and `HF` CLI installed (for publishing/validation).
- In a clone of `SCBE-AETHERMOORE`, run from repository root.

## Pipeline workflow

1. Export Notion pages to dataset JSONL.
   - `python scripts/notion_to_dataset.py --category all --output training-data/`
   - Output files include `training-data/notion_export_<cat>_<yyyymmdd>.jsonl` and `training-data/metadata.json`.

2. Push dataset to Hugging Face.
   - `python scripts/push_to_hf.py --data-path training-data/notion_export_all_$(Get-Date -Format yyyyMMdd).jsonl --repo-id <owner>/scbe-aethermoore-training-data --token $env:HF_TOKEN`
   - For repository-level updates, use `HF_TOKEN` or pass `hf upload` directly.

3. Run pipeline health checks.
   - `python scripts/notion_pipeline_gap_review.py --output artifacts/notion_pipeline_gap_review.json --summary-path artifacts/notion_pipeline_gap_review.md`
   - `python scripts/compare_notion_to_codebase.py --notion-jsonl training-data/notion_raw_clean.jsonl`

4. Trigger GitHub Actions for repeatable runs.
   - `gh workflow run notion-to-dataset`
   - `gh workflow run cloud-kernel-data-pipeline -f ship_targets=hf,github`

5. Optional browser validation (Playwright).
   - Open target HF dataset/model pages and verify cards/metadata before/after publish.

## Notes

- If dataset export records are 0, check Notion token scope and `scripts/sync-config.json` entries.
- Use `artifacts/notion_pipeline_gap_review.json` and `.md` for the highest-priority remediation list.
- Use `training/NOTION_CODEBASE_COMPARISON.md` to compare Notion coverage against repository code/docs.
