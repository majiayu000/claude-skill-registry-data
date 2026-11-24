---
name: auto-anti-skill
description: "Use after repeated model mistakes or corrections. Mines dialogue corrections into candidate anti-skills."
invocation: discipline
status: canonical
operad_source_colours: ["State", "Audit"]
operad_target_colour: "Ledger"
operad_arity: 2
operad_residual: "unknown"
families: [prompt-civilization, anti-skills]
---

# auto-anti-skill

`AuthorityEffect: None.` Mine candidates; never admit, execute, or certify them.

## Workflow

1. Preserve the raw dialogue and compute its digest. Do not load the old epistemic-immunity archive as authority.
2. Run `scripts/auto_anti_skill.py segment-dialogue`. Use explicit line bounds when a transcript includes tools or build output.
3. Review correction episodes and add a proposed failure code, invariant, evidence references, protected fields, and at least one clean counterexample to separate annotation data. The model's annotation remains a proposal.
4. Run `mine-candidates`. Identical episode IDs deduplicate; incomplete annotations emit nothing.
5. Write resulting candidates only under `eis/antiskills/ooutwire/`.
6. Record the learning through the existing auto-skill episode/resolve pipeline. Frequency and confidence never grant admission.

Read [admission_boundary.md](references/admission_boundary.md) before recommending promotion.

## Boundaries

- Never edit `eis/antiskills/admitted/`, the compiled registry, validators, fixtures, or evaluation receipts.
- Never convert a phrase pattern, scalar score, density matrix, or recurrence count into a truth verdict.
- Require distinct context keys and held-out negative controls before human admission review.
- Treat detector, repair proposal, verification, and packetization as separate typed operations.
- Treat learning and promotion as directed refinement, never an invertible equivalence.
- Refuse unsupported transcript formats rather than guessing speaker or tool boundaries.

## Constraints

Required: [EVIDENCE_BASED, NO_HARDCODED_SECRETS, and MAINTAIN_TESTS](../_shared/constraints.md). This skill never self-certifies or bypasses admission and Git gates.

## Outputs and Tests

Outputs: `core.antiskill.segmented-dialogue.v1` and `core.antiskill.candidate-set.v1`. Both are inert proposal records with `AuthorityEffect: None`.

Verification command:

```bash
python operads/skills/auto-anti-skill/scripts/auto_anti_skill.py segment-dialogue --output eis/antiskills/ooutwire/test_segment.jsonl
```

## Related Skills

`core-prompt` reviews and types consequential prompts. `auto-skill` records learning episodes; `lib-skill-admission-hygiene` governs admission review.
