---
name: output-validator
description: "Validate a governed artifact or a produced document BEFORE it ships. Use to check a JSON artifact (records package, handoff envelope, classifier record, decision record) against its schema plus a governance / no-fabrication / no-real-PII rule catalog, and to structurally validate produced Office/PDF files (.docx/.pptx/.xlsx/.pdf/.odt/.ods/.odp) for the corruption classes that make them fail to open. Trigger phrases: 'validate this output', 'is this artifact valid', 'check this file before sending', 'will this docx open', 'lint the output'. Runs tools/validate_outputs.py (JSON) + tools/validate_document.py (documents), stdlib-first so it always runs even with nothing installed. Do NOT use it to score teaching quality (that is quality-review) or to diagnose the whole ecosystem (that is skill-health) — it validates one output's correctness."
---

# output-validator

Catches a broken output before a human — or a teacher's Office/PDF app — does. **Stdlib-first:** the
core checks run with zero optional libraries; richer checks (JSON Schema, deep format conformance)
activate when their library is present and are reported as *skipped*, never *failed*, when not. This is a
safety net, not a nicety: it is how the ecosystem catches its own mistakes.

## What it validates
- **Governed JSON artifacts** — `tools/validate_outputs.py`: required keys, `human_review_required: true`,
  no empty/fabricated standards, no real PII (SSN / non-`555` phone), and JSON Schema
  (records / traversal / udom / connector-flags) when `jsonschema` is installed. `--promote` captures a
  failing case as a regression eval so the same defect can't recur silently.
- **Produced documents** — `tools/validate_document.py`: structural integrity of `.docx/.pptx/.xlsx`
  (OPC parts), `.odt/.ods/.odp` (ODF), and `.pdf` (header / xref / `%%EOF`) — the corruption classes
  documented by the **Open XML SDK** and **veraPDF**, with **zero dependencies**.

## How it works — the pipeline
Follow `references/method.md`. Generation here is the validation pass:
`Analysis (pick schema/profile) → Checks (governance rules + structure) → Diagnosis → pass/fail + repair
guidance`. **Honest limits:** structural validity is necessary, not sufficient — deep OOXML schema
(Open XML SDK) and PDF/A or PDF/UA conformance (veraPDF) are optional follow-ups, reported as such and
never assumed (`references/format-error-catalog.md`). When a check can't run (a library is absent) it
degrades to a labeled gap, so the validator itself always returns a usable answer.

## References (thorough by design)
- `references/rule-catalog.md` — every governance + claim rule, with severity and rationale.
- `references/format-error-catalog.md` — OOXML / PDF / ODF / font error classes + spec citations + fixes.
- `references/profiles.md` — per-artifact required-key profiles.

## Output: always emit the metadata block
Every validation report ends with the metadata block (`references/metadata-schema.md`) +
`human_review_required: true`. On a failure, route the fix to **skill-repair** (mechanical) or the owning
skill (judgment). Placeholders only; never real student data.

```bash
python3 tools/validate_outputs.py --input artifact.json --schema records
python3 tools/validate_document.py deck.pptx report.pdf
```
