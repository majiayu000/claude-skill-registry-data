---
name: aiwf-dataset
description: Use for AIWF and MoK dataset intake, source and license validation, additive curation, cleanup, manifests, receipts, freshness and retention gates, text/image/video/audio data, multimodal captions, synthetic-data labeling, and dataset QA or reporting.
---

# AIWF Dataset

Use this skill as the coordinator for local-first dataset intake, validation, cleanup, and reporting. Prefer existing specialized skills for heavy work, but keep the operating contract here: verify the real root, preserve provenance, label synthetic material, and avoid destructive cleanup.

## Operating Rules

- Verify the active repo or dataset root before acting. If `datasets/` or `.git` is missing, report that and continue only with root-independent work.
- Keep MoK and AIWF work local unless the user explicitly asks to publish, push, upload, or open a pull request.
- Treat current dataset work as a library or candidate corpus unless the user explicitly asks for a final merged training set.
- Do not delete, truncate, overwrite, or append into an existing subject dataset folder. Write a new folder, manifest version, quarantine report, or patch file instead.
- Preserve receipts: source URLs, access dates, license notes, hashes when available, source type, generated-by fields, validation results, and unresolved issues.
- When facts could be current or unstable, verify with primary or official sources. Do not reuse stale model memory as a source of truth.
- Use AI-writing checks as writing-quality signals, not authorship proof.
- Allow AI-generated text for synthetic guardrail training rows only when it is labeled and separated. Original research used as the factual basis for a dataset must come from human-authored, official, primary, or otherwise traceable non-synthetic sources.

## Workflow

1. Verify scope.
   - Identify the active root, target dataset folders, requested modalities, and whether the work is intake, cleanup, generation, validation, or reporting.
   - Run `scripts/validate_dataset_receipts.py <root>` for a cheap read-only pass when working on local dataset folders.

2. Route to the right reference.
   - For source vetting and daily automated research, read `references/research-validation.md`.
   - For freshness windows, media duration gates, retention, and cleanup cadence, read `references/curation-lifecycle.md`.
   - For image, video, audio, captions, embeddings, or scene/clip extraction, read `references/multimodal-captioning.md`.
   - For dashboards, reports, or handoff artifacts, read `references/reporting-widgets.md`.
   - For AI-writing boundaries and guardrail training data, read `references/guardrails-ai-writing.md`.
   - For the reviewed companion skills and when to call them, read `references/current-skill-map.md`.

3. Validate research before curation.
   - Separate raw intake from accepted sources.
   - Classify each source as primary, official, peer-reviewed, dataset card, repository, benchmark, secondary, scraped, model-generated, or unknown.
   - Reject or quarantine sources with unclear origin, missing license, broken citations, AI citation markup leaks, placeholder text, or unsupported claims.

4. Curate and clean.
   - For small local passes, use repo-native scripts and structured parsers first.
   - For large text or multimodal corpora, inspect installed tooling and data volume before proposing NeMo Curator, Ray Data, sentence-transformers, FAISS, or another optional dependency.
   - Do not add a GPU or distributed stack when hashes, metadata, or a bounded CPU pass can answer the task.

5. Caption and label multimodal data.
   - Keep raw file metadata, model captions, verified captions, and source captions in separate fields.
   - Record model name, prompt or config hash, confidence, reviewer, and validation status for generated captions.
   - Do not promote generated captions into factual ground truth without a verification step.

6. Report outcomes.
   - Summarize reviewed folders, files changed, sources accepted, sources rejected or quarantined, validation results, and judgment calls.
   - For dashboard or report requests, use an installed analytics capability when available; otherwise produce a bounded local report from validated counts.

## Default Local Checks

Use the bundled validator before and after cleanup work:

```powershell
python <this-skill>\scripts\validate_dataset_receipts.py .\datasets
python <this-skill>\scripts\validate_dataset_receipts.py .\datasets --strict --json
```

The script is read-only. It checks root existence, manifest/source-registry parseability, JSONL parseability, duplicate IDs, missing IDs, common placeholder leaks, common AI citation leaks, and expected receipt files.

## Output Contract

End with:

- Dataset root inspected.
- Sources or folders reviewed.
- Files changed or new files written.
- Validation commands and results.
- Accepted, rejected, quarantined, or needs-review counts.
- Remaining gaps that need user judgment.
