---
name: toki-pona-formatting-pass
description: Continue, format, or mechanically audit layered source-language/Toki Pona/sitelen pona ODT manuscripts, including glossary anchors, name guides, canonical-form consistency, structural QA, script-specific fonts, and safe saves. Use for layered book manuscripts; not for literary or translation-quality certification.
license: MIT
metadata:
  abvx_status: experimental
  abvx_origin: local-production
---

# Toki Pona Formatting Pass

Use this skill for staged source-language/Toki Pona document production. Choose the narrowest applicable mode:

- **Formatting mode:** continue the existing LibreOffice workflow below.
- **Editorial audit mode:** read [references/editorial-qa.md](references/editorial-qa.md), then run the bundled audit script. This mode is strictly read-only toward source ODT/PDF files.

Do not treat mechanical findings as proof of literary or translation quality.

## Establish the edit point

- Confirm the intended document and current insertion point. Never assume a historical path or version is current.
- Inspect the nearby text and font state before pasting. Fresh pasted material may arrive as `Liberation Mono` even when that is not intended.
- Distinguish three content types: English/source prose, Toki Pona prose, and glossary or name-guide anchors.

## Stage the next batch

Use the approved source context to prepare only the requested continuation. Keep headings and progress notes separate from document prose unless the user explicitly wants them inserted.

For a glossary anchor, preserve the observed three-part pattern:

```text
English anchor — toki pona phrase toki pona phrase
```

The first Toki Pona copy remains readable Latin text; the repeated copy is the span intended for the sitelen pona font. Do not silently change or deduplicate this structure. If the source provides a different approved pattern, preserve it instead.

Do not claim that generated continuation, glossary wording, names, or progress estimates are translation-verified. Ask before inventing missing content when the source context is insufficient.

## Paste and format in LibreOffice

1. Paste at the confirmed insertion point.
2. Select the newly pasted Latin-script block and apply the approved Latin font where it matches the surrounding document. The original production profile used `Georgia`; do not apply any font document-wide.
3. Select only each intended Toki Pona rendering span and apply `nasin-sitelen-pu`.
   - In prose, style the complete Toki Pona line or phrase selected for rendering.
   - In a duplicated glossary anchor, style only the second Toki Pona copy unless the nearby document proves another convention.
   - Keep English text, the dash, headings, and the readable Toki Pona copy out of the sitelen pona selection.
4. Work in coherent batches, but make font changes at span level. If a selection crosses scripts or adjacent prose, cancel or undo and retry with a smaller selection.
5. Visually inspect the edited batch for missing spans, mixed/default fonts, altered order, and accidental changes to nearby material.
6. Save after each meaningful batch and before switching tasks. Treat a visible save completion as save evidence; do not infer it from formatting alone.

## Completion criteria

- The intended block is present once at the correct location.
- Latin text uses the surrounding document's approved font.
- Only intended Toki Pona rendering spans use `nasin-sitelen-pu`.
- Glossary anchors retain both the readable and rendered Toki Pona copies when that convention applies.
- Nearby unrelated text is unchanged, the batch was visually inspected, and the current document was saved.

## Editorial audit mode

Use `scripts/odt_editorial_qa.py audit --dry-run` for extraction, canonical proposals, consistency and anomaly checks, layer QA, PDF extraction boundaries, and publication-readiness reporting.

- Require explicit ODT and output paths. Treat the ODT as source of truth; PDF extraction is supporting evidence only.
- Preserve variant frequency plus Book/location distribution in canonical proposals.
- Classify PDF-only or sitelen-font extraction anomalies as `SOURCE_ARTIFACT`, never as manuscript typos without ODT evidence.
- Keep severity separate from confidence.
- Report proposed fixes only. The script intentionally has no replacement or write-back command.
- Verify source hashes before and after the audit.
