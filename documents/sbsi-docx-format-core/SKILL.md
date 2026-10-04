---
name: sbsi-docx-format-core
description: |
  Enforce SBSI Word document formatting conventions on a DOCX after the
  correct document-type template has already been resolved: exact
  ordinary-text typography (Times New Roman 13pt), real Word heading/
  outline styles, real Word numbering (never typed "1."/"a)" prefixes),
  a real dynamic TOC field, and preservation of the selected template's
  sections/header/footer/tables. Ends with blocking structural validation
  and render/visual QA — a structurally-valid-but-visually-broken file is
  not acceptable.
  Use when: generating or reformatting any SBSI governance-style DOCX
  (Quy trình, Quy định, Quy chế, Hướng dẫn, and similar) once a template has
  been resolved; asked to "fix the format" of an SBSI Word document; asked
  what the SBSI DOCX typography/numbering/TOC rules are.
  Triggers on: "format theo SBSI", "chỉ sửa format", requests to generate/
  reformat a Quy trình/Quy định/Quy chế/Hướng dẫn document, TNR 13pt,
  "Times New Roman 13", real Word numbering vs typed numbering.
  Skip when: no template has been resolved yet — invoke `sbsi-template-router`
  first, this skill never chooses a template itself. Also skip for BRD
  generation's own business-content workflow (see `brd-generation`), though
  BRD's ordinary-text typography can still be checked with this skill's
  validator.
---

# SBSI DOCX Format Core

## Purpose

This is the **format enforcement layer** — deliberately independent of
document type. It answers "once the correct template is selected, how must
the DOCX be built/edited so it's structurally and visually compliant?" It
does **not** answer "which template?" — that's `sbsi-template-router`'s job,
always invoked first.

```
sbsi-template-router  →  RESOLVED {document_type, template_path}
        ↓
sbsi-docx-format-core →  copy template → edit content → normalize → validate → render QA
        ↓
final DOCX (delivered only if validation + render QA both pass)
```

## Mandatory dependency

Before creating or reformatting an SBSI governance DOCX, obtain a resolved
template from `sbsi-template-router` — unless the user has explicitly
supplied a template file for this specific task. Never silently reuse a
template that belongs to a different document type; that's exactly the
failure this two-skill split exists to prevent.

Read `references/FORMAT_CONVENTIONS.md` for the full rule set (typography,
numbering, headings, TOC, layout preservation, tables, format-only mode)
before generating or reformatting anything — it's the source of truth, this
file only summarizes. `references/format_contract.json` is the
machine-readable mirror of the same rules — it's what `_sbsi_docx_common.py`
actually loads its constants from at runtime, so it and
`FORMAT_CONVENTIONS.md` must be edited together; never let them drift.

Read `references/IMPLEMENTATION_GUIDE.md` for the actual workflow (copy →
edit → normalize → validate → render QA) and the exact script invocations.

## Rule precedence

1. User's explicit instruction in the current task.
2. Common SBSI structural conventions (`references/FORMAT_CONVENTIONS.md`).
3. The **selected template** for layout, branding, special typography,
   table geometry, sections, header/footer, and type-specific styles.
4. The source document being reformatted (if any).

If a template-specific element intentionally differs from a common rule
(e.g. a compact landscape appendix matrix), preserve the template's
element rather than flattening it to the generic rule.

## The five headline rules (full detail in FORMAT_CONVENTIONS.md)

1. **Typography** — ordinary text is Times New Roman, exactly 13pt by
   default (`format_contract.json`'s global default for governance docs) —
   a template with its own verified convention (e.g. BRD's 12pt) declares
   an explicit `typography_profile` override in its own
   `template_manifest.json`; the same shared engine reads it rather than
   special-casing that document type in code. Cover typography, real
   headings, TOC entries, and headers/footers are exempt regardless.
2. **Numbering** — structural clauses/sub-points use real `w:numPr`, never
   typed "1."/"a)" prefixes. A tolerated exception: manually-numbered
   reference lists inside an appendix.
3. **Headings** — real Word paragraph styles with real outline levels, not
   bold-Normal text mimicking heading vocabulary.
4. **TOC** — a real Word field (`instrText` containing `TOC`), never typed
   dot-leader text. Must survive `Ctrl+A → F9` in Word.
5. **Layout preservation** — page size/orientation, sections, margins,
   headers/footers, logos, tables, and appendix orientation come from the
   selected template, not reinvented.

## Golden-template principle

Clone the selected template, preserve its styles/numbering/sections/
headers/footers/relationships/media, then replace/insert content. Do not
build blank and try to visually imitate the template — visual similarity is
not the acceptance bar, structural correctness is.

## Generating NEW structural content — use the helpers, don't hand-roll XML

When adding a Chương/Điều/Khoản/Điểm that doesn't already exist in the
template (not just reformatting existing content), use
`scripts/_sbsi_docx_common.py`'s `clone_structural_paragraph()`,
`clone_empty_structural_paragraph()`, `build_new_chapter_paragraphs()`, and
`build_toc_field_paragraph()` — never construct `numPr`/`outlineLvl` XML by
hand, and never type "Chương I", "Điều 5.", or a dot-leader TOC line as
literal text. A style name alone does not tell you its outline level (a
style's own `outlineLvl` can differ from what every real paragraph using it
actually shows via a direct per-paragraph override — see
`IMPLEMENTATION_GUIDE.md`'s "Common pitfalls" for a verified example that
caused a real bug). Full detail: `references/IMPLEMENTATION_GUIDE.md` §A.4
and §B.5.

## Format-only mode

When the user says "chỉ sửa format" / "không sửa nội dung" / "only fix the
format": no content rewriting, shortening, correction, terminology changes,
or restructuring. The only allowed transformation is converting a manually
typed structural prefix into equivalent real Word numbering/heading style,
keeping the visible wording semantically identical. Full detail in
`FORMAT_CONVENTIONS.md` §7.

## Validation gates (blocking)

```bash
python3 scripts/validate_sbsi_docx.py --doc <output.docx> \
  --template <selected_template.docx> \
  [--manifest <template_manifest.json>]
```

Any `ERROR:` line is blocking — do not deliver the file. Fix and re-run.
`WARNING:` lines must be reported to the user, never silently dropped.

If ordinary text needs normalizing first:

```bash
python3 scripts/normalize_ordinary_text.py <input.docx> <normalized.docx> \
  [--manifest <template_manifest.json>]
```

Then render + visually inspect every page (structural validation alone is
not sufficient — a structurally valid but visually broken file is not
acceptable):

```bash
python3 scripts/render_qa.py <output.docx> <out_dir> [--expect-min-pages N]
```

Look at every PNG `render_qa.py` produces against
`references/QA_CHECKLIST.md`'s Visual section before telling the user the
document is ready.

## Acceptance checklist

See `references/QA_CHECKLIST.md` for the full list. Summary: correct
template resolved first; TNR 13pt ordinary text with no font leakage; real
outline-level headings; real Word numbering (no manual sequences outside a
tolerated appendix); dynamic TOC when required; header/footer/sections
preserved; every page rendered and visually inspected; content preserved
exactly in format-only mode.

## Genericity — read before editing the scripts

This skill's scripts (`scripts/_sbsi_docx_common.py`,
`validate_sbsi_docx.py`, `normalize_ordinary_text.py`) must stay
document-type-agnostic: no hardcoded article names, chapter numbers, or one
org's specific text. Anything that's genuinely specific to one template
(a cover-page-detection quirk, an appendix marker in a different
vocabulary, extra heading patterns) belongs in that template's own
`template_manifest.json`, registered alongside it in
`sbsi-template-router/templates/<type>/`. If you find yourself wanting to
hardcode a document-specific string into these scripts, that's the signal
to add a manifest field instead.

This skill must never choose a template by itself — use
`sbsi-template-router` for that.
