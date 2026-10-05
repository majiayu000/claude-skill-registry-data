---
name: sdd-evidence
description: >
  Discover, build, verify, and optionally export (HTML, optional PDF) the evidence
  manifest of one SDD Composy task in evidence_required, routing it toward
  review_required. Use when acceptance evidence must be assembled or checked —
  'juntar as evidências da task', 'gerar o relatório de evidências', 'verify the
  evidence manifest'. Do NOT use to run tests (sdd-qa), review code (sdd-review), or
  inspect the trace (sdd-trace).
metadata:
  version: 0.1.0
---

# SDD Evidence

Build, verify, and optionally export the portable evidence manifest of one task with the
bundled `scripts/sdd_evidence.py` helper.

Language: when an operation emits human-facing summaries, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Operations

1. `sdd_evidence.py discover <root>` — a deterministic, read-only inventory of the existing
   task evidence under the confined evidence root, before creating anything.
2. `sdd_evidence.py build <input.json> <root> <manifest>` — rebuild the manifest, preserving
   the source files and recording relative paths, SHA-256 digests, known enums, and sanitized
   content. Never mutate existing evidence while rebuilding.
3. `sdd_evidence.py verify <manifest> <root>` — required before routing a task from
   `evidence_required` to `review_required`. The task engine remains the authority and rejects
   missing, stale, or unapproved evidence.
4. `sdd_evidence.py export <manifest> <root> <output> [--workspace-root <repo>]` — HTML report.
   With the evidence root at `tasks/prd-<slug>/evidences/`, the output may be anywhere in that
   PRD bundle (normally `tasks/prd-<slug>/evidence-report.html`) and the workspace language is
   read from the repository root without `--workspace-root`. PDF is optional: `--pdf`, only when
   explicitly requested, writes `<output>.pdf` beside the HTML with a headless Chromium-family
   browser (`SDD_PDF_BROWSER` overrides discovery). Screenshots are embedded in the report; a
   missing or non-image screenshot fails, and without a browser the export fails before writing.

Never infer approval, bypass lifecycle guards, or use paths outside the task root. Return the
manifest and verification result unchanged to the caller.

## Read when

- `references/artifacts.md` ("Synchronization and evidence") — building a manifest, or a path,
  digest, or enum is rejected.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
