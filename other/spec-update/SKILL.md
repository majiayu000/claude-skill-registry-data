---
name: spec-update
description: Make a minimal evidence-backed update to a non-plan product, architecture, API, schema, or behavior contract. Use when implementation or validation cannot determine correctness from the current authoritative contract.
---

# Specification Update

Correct an authoritative semantic contract only when current work depends on it.

## Workflow

1. Identify the missing or incorrect contract, its canonical document and owner, and the current task it blocks.
2. Use `plan-update` for implementation-plan mechanics and `docs-drift-review` for ordinary prose drift.
3. Decide whether the change is a clarification or a new decision. Apply a clarification that code, tests, or other authoritative evidence supports. A new product or architecture decision belongs to the user or the named owner: stop and ask, or use `architecture-refine` when the user is available for it.
4. Confirm authority before editing linked documents outside the repository or requested scope.
5. Apply only the minimum supported correction in the document's existing structure and style.
6. State the downstream acceptance or validation effect, and the compatibility impact when the contract is published to other consumers. Then return to the invoking task.

Do not create speculative features, use specifications as implementation logs, rewrite unrelated sections, or silently invent behavior.

Finish with the changed contract, supporting evidence, concrete decision, downstream impact, and any remaining blocker.
