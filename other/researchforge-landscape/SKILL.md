---
name: researchforge-landscape
description: Synthesize stored papers into a research landscape — grouped directions with evidence claims — and import it for validation. Use after papers are stored, when the user wants directions, themes, or a map of the literature.
---

# Build the research landscape

This is a handshake: the engine exports structured context, you write the
synthesis as YAML, the engine validates it field-by-field before anything is
stored. Your synthesis must be grounded in the exported papers only.

## 1. Export context

```bash
researchforge research context --json
```

This writes `.researchforge/synthesis/context.json`: the objective, the
stored papers (id, title, abstract, ranking signals), and — critically — the
embedded JSON Schema the artifact must conform to. Read the whole file.

## 2. Write the landscape

Write `.researchforge/synthesis/landscape.yaml` conforming exactly to the
embedded schema. Requirements the validator will enforce:

- every `cited_paper_ids` entry must be a stored paper id from the context;
- every direction needs evidence claims that distinguish **claims made by a
  paper** from **your interpretation** (`evidence_type`), each with an
  `extraction_confidence`;
- do not cite papers for statements their abstracts cannot support.

## 3. Import (engine validates)

```bash
researchforge research landscape --import .researchforge/synthesis/landscape.yaml --json
```

If validation fails, the `--json` error payload lists field-level errors
(path, message, offending value). Re-read the error payload, fix exactly
those fields in the YAML, and re-import. Never bypass validation by editing
stored files directly.

Next: the researchforge-hypotheses skill turns directions into testable
hypotheses.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
