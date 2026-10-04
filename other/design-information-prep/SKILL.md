---
name: design-information-prep
description: "Extract evidence-grounded project facts from user-provided design attachments, identify missing information, and prepare the exact written fields required by supported design-award entry forms. Use when a user asks to prepare, draft, adapt, translate, or validate application text for iF, iF Student, Red Dot Product Design, IDEA, DIA, K-Design, GOOD DESIGN AWARD Japan, Core77, James Dyson, or EPDA. Also use to build a reusable project dossier from briefs, decks, reports, manuals, patents, research, images, or prior application materials. Do not use for award selection alone, winner retrieval, design-quality scoring, final file-format auditing, or winning-probability prediction."
---

# Design Information Prep

## Purpose

Turn user-authorized attachments into a reusable, evidence-linked project dossier, then compile that dossier into the exact text fields required by one supported award route. Generate no project fact from past-winner copy or unsupported inference.

## Runtime Boundary

- Treat user attachments and explicit user confirmations as the only sources of project facts.
- Read local award field specifications for field names, limits, routing, and drafting instructions.
- Do not connect to Supabase, read `.env`, query winner databases, or place full winner descriptions in model context.
- Use optional aggregate benchmark profiles only for coverage prompts such as what evidence to look for. Never use them as project facts, prose templates, hidden judging preferences, or winning probabilities.
- Verify current official rules at request time. Stored specifications record a checked date, not permanent truth.

## Input Contract

Accept PDFs, presentations, documents, spreadsheets, images, videos, structured JSON, or plain text. Determine or request:

- exact award, cycle, route, and language;
- applicant type and project maturity when they affect routing;
- all user-authorized project materials;
- confidentiality or publication restrictions;
- whether the user wants a dossier, missing-information audit, draft fields, translation, or final text validation.

If the award or route is unknown, use `$design-award-match` first. If the user only wants final file and portal compliance, use `$design-submission-check` after drafting.

## Workflow

### 1. Lock the target

Read the selected file under `references/awards/`. Record the exact award id, cycle, route, stage, language, official sources, and checked date. Verify any current cycle rule that could have changed, including requiredness, limits, language, conditional fields, and publication behavior.

Do not silently merge professional, student, product, and concept routes.

### 2. Build the project dossier

Read [references/evidence-policy.md](references/evidence-policy.md) and [references/project-dossier-schema.json](references/project-dossier-schema.json). Extract canonical facts into `facts` records containing:

- value;
- status: `supported`, `inferred`, `confirmed_by_user`, or `missing`;
- confidence;
- attachment evidence and locator;
- whether user confirmation is required.

Preserve contradictions as separate findings. Do not choose a convenient value without reporting the conflict. Mark unavailable facts `missing`; never fill them from general knowledge or a past winner.

### 3. Prepare an award-specific evidence packet

Save the dossier as structured JSON and run:

```powershell
python scripts/prepare_entry_packet.py `
  --dossier examples/project-dossier.example.json `
  --award idea `
  --route general `
  --pretty
```

The packet identifies ready fields, missing essential facts, available evidence, limits, and drafting instructions. Ask only the questions that block required fields. Continue with partial output when the user prefers, labeling every unresolved field.

### 4. Draft field by field

Use only facts listed in each field's prepared evidence packet. Follow the official field purpose rather than forcing one generic description into every form.

- Lead with the answer, not promotional framing.
- Prefer specific mechanisms and outcomes over unverified superlatives.
- Distinguish measured outcomes from intended benefits.
- Preserve units, denominators, dates, maturity, and uncertainty.
- Do not convert an inference into a confirmed claim through fluent wording.
- Count words and characters according to the field specification.
- Keep translations semantically aligned; do not introduce new claims in one language.

Prepare machine-checkable output using [references/entry-output-schema.json](references/entry-output-schema.json). Include `used_fact_ids` for every drafted field.

### 5. Validate the draft

Run:

```powershell
python scripts/validate_entry_output.py `
  --dossier examples/project-dossier.example.json `
  --entry examples/idea-entry-output.example.json `
  --pretty
```

Resolve every Blocker before presenting a field as submission-ready. Treat unsupported or inferred claims awaiting confirmation as Important. The validator checks required fields, route alignment, list limits, word/character limits, and fact provenance; it does not verify scientific truth or live portal behavior.

### 6. Report

Follow [references/output-template.md](references/output-template.md). Return:

1. target award, route, cycle, language, and rule freshness;
2. prepared field text with limit usage;
3. evidence coverage and assumptions;
4. missing information as concise user questions;
5. fields requiring confirmation;
6. validation decision and remaining findings.

## Supported Award Specifications

The `references/awards/` directory contains versioned public-field specifications for:

- iF DESIGN AWARD;
- iF DESIGN STUDENT AWARD;
- Red Dot Award: Product Design;
- IDEA;
- Design Intelligence Award, with separate Product and Concept routes;
- K-Design Award;
- GOOD DESIGN AWARD Japan;
- Core77 Design Awards;
- James Dyson Award;
- European Product Design Award, with Professional and Student routes.

Validate all specifications after editing:

```powershell
python scripts/validate_field_specs.py --pretty
```

## Decision Rules

- Current official rules override stored specifications, previous cycles, winner pages, and memory.
- Missing attachment evidence never becomes a supported fact by inference.
- A field may be drafted provisionally from an inferred fact only when clearly labeled and confirmed before final submission.
- Public winner descriptions are not evidence of the user's design and are not application-form ground truth.
- Evaluation criteria are not separate form fields unless official entry materials explicitly expose them as fields.
- `Ready` requires every required field to pass limits and provenance checks.
- A completed text audit does not prove portal acceptance or legal clearance.

## Example Invocations

- `使用 $design-information-prep，从附件建立作品信息母稿，并生成 IDEA 需要填写的全部英文文字字段。`
- `使用 $design-information-prep，检查这套材料是否足以填写 DIA 概念组；不要补造缺失的市场或测试数据。`
- `Use $design-information-prep to adapt this project dossier to iF and Red Dot while preserving evidence links and character limits.`
