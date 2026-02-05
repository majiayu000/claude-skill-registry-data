---
name: lcp-wysiwid-spec
description: Write WYSIWID-style design docs (Concepts + Synchronizations) for go-lcpd, keeping terminology consistent with code.
metadata:
  short-description: WYSIWID design doc authoring
---

Use this skill when you are authoring or updating `go-lcpd` design documentation (the “What You See Is What It Does” / WYSIWID pattern).

## References (in-repo)

- `go-lcpd/WhatYouSeeIsWhatItDoes.md` (background and rationale)

## WYSIWID model (summary)

- A **Concept** is an independent capability. Concepts must not depend on each other.
- A **Synchronization** connects Concepts into an end-to-end flow/story.

## Writing rules (must follow)

- Start with invariants (“Security & Architectural Constraints”). Use RFC 2119 language (MUST / MUST NOT) and include brief rationales.
- Keep Concepts dependency-free:
  - A Concept MUST NOT call actions from other Concepts.
  - A Concept MUST NOT reference other Concepts’ types.
  - Cross-Concept coordination belongs only in Synchronizations.
- Keep structure flat and scannable; prefer short lists, signatures, and data-shape bullets over long prose.
- Use a ubiquitous language: keep terminology consistent across docs and Go identifiers where possible.

## Suggested section order (for `spec.md`)

1. Security & Architectural Constraints
2. Concepts
3. Synchronizations

## Example template (shape)

- `### <ConceptName>`
  - Purpose: …
  - Domain Model: `Thing: field, field`
  - Actions: `action(arg) -> out` (include side effects + error cases)

- `### sync <SyncName>`
  - Summary: …
  - Flow: when / where / then (include error branches)

If the flow is complex, add a Mermaid sequence diagram or state chart.

## Validation

- Ensure the doc can be read as the “ubiquitous language” for the relevant code.
- If the doc implies behavior changes, implement them and validate with the module’s normal test/lint flow (see `$lcp-go-lcpd`).
