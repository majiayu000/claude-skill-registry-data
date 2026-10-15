---
name: __SKILL_NAME__
description: "REPLACE — what this skill produces and exactly when to use it. Be specific and slightly pushy to trigger reliably, and add an explicit 'Do NOT use for…' clause to avoid colliding with sibling skills. List the artifacts and the personas/phrases that should invoke it."
---

# __SKILL_NAME__

## What this skill does
REPLACE with a one-paragraph overview of the capability and its artifacts.

## How it works — the unified pipeline
Follow the shared pipeline in `references/method.md`
(`Request → Routing → Protocol Enforcement → Generation → Validation → Quality Gates →
Approval/Certification → Release`). The domain work happens in Generation:
`Analysis → Standards Alignment → Differentiation → Generation`.

- **Standards** — select + cite verifiable standards (`references/` standards material;
  `protocol-layer/standards-verification.md`). Never fabricate a standard.
- **Differentiation** — apply UDL by default, plus tiering / EL / IEP supports as relevant.
- **Quality** — self-check against `references/quality-gates.md`, then hand to `quality-review`.

## Artifacts
See `references/artifact-types.md` for the artifact types this skill produces and their specs.

## Output: always emit the metadata block
Every artifact ends with the metadata block from `protocol-layer/metadata-schema.md`, including the
per-dimension quality scores, the decision, and `human_review_required: true` — outputs are
decision support, not final professional or legal determinations. Use placeholders only; never real
student data.
