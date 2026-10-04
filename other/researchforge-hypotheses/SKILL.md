---
name: researchforge-hypotheses
description: Generate testable, evidence-linked hypotheses from the research landscape and import them for validation. Use after the landscape exists, when the user wants hypotheses, experiment ideas, or "what should we try?".
---

# Generate hypotheses

Same handshake as the landscape: context out, YAML in, engine validates.

## 1. Re-read the context

`.researchforge/synthesis/context.json` (regenerate with
`researchforge research context --json` if stale) plus the imported
landscape (`researchforge status --json` shows what exists).

## 2. Write hypotheses

Write `.researchforge/synthesis/hypotheses.yaml` conforming to the embedded
schema. Each hypothesis needs:

- a falsifiable `claim` and `rationale`;
- `supporting_paper_ids` / `contradicting_paper_ids` drawn only from stored
  papers (the validator rejects unknown ids);
- an honest `evidence_status` and `novelty_confidence` — mark speculation as
  `speculative`; do not inflate support;
- `limitations` the user should know before spending compute on it;
- a `proposed_experiment` concrete enough to implement later.

## 3. Import (engine validates)

```bash
researchforge hypotheses import .researchforge/synthesis/hypotheses.yaml --json
researchforge hypotheses list --json
```

On validation failure, read the `--json` error payload, fix exactly the
listed fields, and re-import.

Next: for explore-mode projects, `researchforge report build` produces the
citation-backed report. For improve-repository projects, continue with the
researchforge-baseline skill.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
