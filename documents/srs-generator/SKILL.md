---
name: srs-generator
description: Generates complete Software Requirements Specification (SRS) documents, following the standard template based on ISO/IEC/IEEE 29148:2018. Use this skill whenever the user asks to create, write, generate, or document an SRS, software requirements specification, requirements document, or mentions terms such as "SRS", "software specification", "functional and non-functional requirements", "requirements document", or requests to document a software system/product in a structured way. Also use it when the user provides information about a system and asks to structure it into formal documentation. The skill accepts text descriptions OR spec files, asks targeted clarifying questions to fill information gaps, extracts key requirements, and lets the user review a preview before saving the file with timestamp format at `docs/srs/yyyy-mm-dd-<short-description>.md`
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.1.0"
---

# SRS Generator

Generates SRS documents in Markdown per ISO/IEC/IEEE 29148:2018. Template lives in `references/srs-template.md` — fill it, never freehand a different structure.

## Workflow

| #   | Step         | Action                                                | Gate                                   |
| --- | ------------ | ----------------------------------------------------- | -------------------------------------- |
| 1   | Collect info | Ask elicitation questions below if input is thin      | enough to fill template, gaps marked   |
| 2   | Generate     | Fill `references/srs-template.md` with collected data | placeholders only for undefined fields |
| 3   | Present      | Show draft, ask for section refinements               | user confirms or requests changes      |

## Information Elicitation

Minimum questions when only a system name/description is given:

- **Main objective** of the system
- **Target users**
- **Main functionalities** (3–5 core functions)
- **Relevant technical constraints** (language, database, platform)

Never block generation on incomplete answers — generate with what's available, mark gaps with `> ⚠️ To be defined: [what is missing]`.

## Related Skills

| Skill                           | When                                                                                                                                                                                                                                                                        |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grilling`                      | Input is vague/high-stakes, user wants scope stress-tested. Structures elicitation as rounds with recommended answers. Skip for quick/well-defined requests.                                                                                                                |
| `prd-get-implicit-requirements` | Input is an existing PRD/long spec, before drafting Section 3. Walks 14 gap categories (error handling, empty/loading states, i18n, a11y, security, observability, legal, deployment) to catch missing NFRs/constraints ahead of time, feeding sections 2.4, 3.4, 3.6, 3.8. |

## Generation Rules

- **Requirement IDs**: `FR-XXX` (functional), `NFR-XXX` (non-functional), `UR-XXX` (usability), `PR-XXX` (performance), `DBR-XXX` (database), `INT-XX` (interface).
- **Priority**: `High` / `Medium` / `Low`.
- **Verification Method**: every FR/NFR gets one of `Inspection`, `Analysis`, `Demonstration`, `Test` (ISO/IEC/IEEE 29148 §3.9 table in template). Default `Test`; use `Analysis` when perf/security can't be end-to-end tested cheaply.
- **Gaps**: `> ⚠️ To be defined: [what is missing]` in _italics_ — never invent critical technical info.
- **Language**: formal English, active voice, "The system shall..." for functional requirements.
- **Minimum completeness**: ≥3 functional requirements, ≥1 usability, ≥1 performance, all system attributes filled.
- **Standard references**: always include `ISO/IEC/IEEE 29148:2018`.

## Quality Checklist (ISO/IEC/IEEE 29148 §5)

Each **individual** requirement must be: `Necessary` · `Appropriate` · `Unambiguous` · `Complete` · `Singular` (split "and" clauses) · `Feasible` · `Verifiable` · `Correct` · `Conforming`.

The requirement **set** must be: `Complete` · `Consistent` · `Feasible` · `Comprehensible` · `Able to be validated`.

Flag violations inline: `> ⚠️ Quality issue: [attribute] — [why]` — don't silently fix ambiguous input.

## After Generating

1. Run `python3 skills/srs-generator/scripts/validate_srs.py <path>` — fix any `ERROR` before presenting the draft; review `WARN` lines against the Quality Checklist.
2. Flag items marked `⚠️ To be defined` for review.
3. Ask if user wants to review before saving.
4. Save to `docs/srs/yyyy-mm-dd-<short-description>.md`.

## Reference files

- `references/srs-template.md` — full Markdown template + example functional requirement.
- `scripts/validate_srs.py` — deterministic pass/fail gate for Generation Rules + Quality Checklist (`--strict` promotes warnings to errors).
