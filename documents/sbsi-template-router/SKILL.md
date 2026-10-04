---
name: sbsi-template-router
description: |
  Identify the SBSI document type and resolve the ONE correct registered
  DOCX template before any document generation or reformatting. Uses
  explicit user intent first, then document content/metadata, and only
  then a weak filename hint. Never reuses a template across document
  types, and fails closed (TEMPLATE_NOT_REGISTERED) rather than guessing
  the closest match when a type has no registered template. Currently
  registered: Quy trình and BRD. Quy định/Quy chế/Hướng dẫn/Chính sách/
  Tờ trình/Biên bản/Quyết định are known types with no template yet.
  Use when: asked to generate, draft, or reformat any SBSI governance/
  business document (Quy trình, Quy định, Quy chế, Hướng dẫn, BRD, and
  similar) as a Word document — always invoke this BEFORE
  `sbsi-docx-format-core`.
  Triggers on: "Quy trình", "Quy định", "Quy chế", "Hướng dẫn", "BRD",
  requests to generate/format an SBSI Word document, a source .docx whose
  type needs identifying.
  Skip when: the actual formatting/typography/numbering/TOC work itself —
  that's `sbsi-docx-format-core`'s job, this skill only resolves which
  template to hand it.
---

# SBSI Template Router

## Purpose

The **template selection layer**. Answers "what kind of SBSI document is
this, and which exact template is allowed for it?" Does not enforce
typography, numbering, heading structure, TOC, or visual formatting — that
belongs to `sbsi-docx-format-core`, always invoked *after* this skill
resolves a template.

```
User request / source document
        ↓
sbsi-template-router  →  identify document type → resolve registered template
        ↓
sbsi-docx-format-core →  generate/reformat/normalize/validate/render-QA
        ↓
final DOCX
```

## Core safety rule

**A template is document-type-specific. Never apply a template registered
for one type to another.** The Quy trình template is registered ONLY for
Quy trình — never for Quy định, Quy chế, Hướng dẫn, Chính sách, Tờ trình,
Biên bản, Quyết định, or anything else, no matter how visually similar.

If a requested type has no registered template: stop, return
`TEMPLATE_NOT_REGISTERED`, and ask the user to supply/register the correct
template. Do not fall back to a different type's template because the
layout looks close.

## Resolution order

1. **Explicit user instruction** in the current request.
2. Explicit document type on a supplied source document's cover/title
   block or `Tên văn bản` metadata.
3. Strong body markers — the exact type-title line (`QUY TRÌNH`, `QUY
   ĐỊNH`, `QUY CHẾ`, `HƯỚNG DẪN`, `BUSINESS REQUIREMENTS DOCUMENT`, ...).
4. Filename prefix/words — weak fallback only, never overrides content.
5. If signals conflict or evidence is thin: ask, don't guess.

Full detail + examples: `references/TEMPLATE_ROUTING_RULES.md`.

## Registry

Every registered template lives under this skill's own `templates/`
directory, one subfolder per document type — this is the single shared
location for ALL SBSI templates, so adding a new document type always has
an unambiguous place to put its file (see "Adding a new template type"
below). Read `template_registry.json`. Current state:

- `quy_trinh` → **registered**: `templates/quy-trinh/SBSI_Quy_trinh_Template.docx`
  (manifest: `templates/quy-trinh/template_manifest.json`).
- `brd` → **registered**: `templates/brd/BRD_Template.docx` (manifest:
  `templates/brd/template_manifest.json`). BRD keeps its own content
  workflow/section rules in the `brd-generation` skill — this registry
  entry unifies template *path* resolution; see the registry entry's
  `notes`. Its manifest declares BRD's own verified typography (TNR 12pt)
  and lack of real Word heading styles — `sbsi-docx-format-core` runs the
  SAME engine against BRD as every other type, just reading different
  per-template values from that manifest instead of skipping BRD outright.
- `quy_dinh`, `quy_che`, `huong_dan`, `chinh_sach`, `to_trinh`, `bien_ban`,
  `quyet_dinh` → known types, **not registered** (`supported: false`), no
  `templates/<type-slug>/` folder yet (never create one preemptively for a
  type with no real template — see "Adding a new template type").
  Resolving any of these returns `TEMPLATE_NOT_REGISTERED` — this is
  correct, expected behavior, not a bug to work around.

## CLI helper

```bash
# Resolve by explicit type
python3 scripts/resolve_template.py --type "Quy trình" --registry template_registry.json

# Resolve from an existing source document
python3 scripts/resolve_template.py --doc source.docx --registry template_registry.json

# Both — conflict detection between stated intent and source content
python3 scripts/resolve_template.py --type "Quy trình" --doc source.docx --registry template_registry.json
```

Returns one JSON object with `status`, and on `RESOLVED`: `document_type`,
`display_name`, `template_id`, `template_path` (absolute), `manifest_path`
(absolute, or `null` if the template has no manifest), `confidence`,
`evidence`. The process exit code also encodes the status (0 = RESOLVED,
non-zero for every blocking status) — see the script's docstring for the
mapping. **Only proceed to `sbsi-docx-format-core` when `status ==
"RESOLVED"`.**

## Failure states (all blocking — never silently continue past these)

| Status | Meaning |
|---|---|
| `TEMPLATE_NOT_REGISTERED` | Type is known but has no template. Ask the user to supply/register one. |
| `DOCUMENT_TYPE_AMBIGUOUS` | Insufficient/unknown evidence. Ask, don't guess. |
| `DOCUMENT_TYPE_CONFLICT` | User's stated type and the source document's own content disagree. Surface it. |
| `TEMPLATE_TYPE_MISMATCH` | The registered template file itself doesn't contain its own required marker (registry/template drift — a data-integrity problem to fix, not to route around). |

## Adding a new template

See `references/TEMPLATE_ROUTING_RULES.md`'s "Adding a new template type"
— in short: drop the file in `templates/<type-slug>/`, add one registry
entry (with real, verified `required_markers`), add a
`template_manifest.json` only if the template needs a structural exception
beyond the generic defaults, then test both `--type` and `--doc`
resolution. Never requires editing `sbsi-docx-format-core`.

## Handoff to the format skill

On `RESOLVED`, pass `document_type`, `template_path`, and `manifest_path`
(if any) to `sbsi-docx-format-core` and follow its workflow for all
generation/formatting/validation/render-QA. This skill's job ends at
resolution — it never edits a DOCX.
