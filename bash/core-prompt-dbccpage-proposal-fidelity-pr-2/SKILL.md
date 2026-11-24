---
name: core-prompt
description: "Review and type a consequential prompt before sending it (code changes, proof claims, merges, publication)."
status: canonical
operad_source_colours: ["State"]
operad_target_colour: "Contract"
operad_arity: 1
operad_residual: neutral
families: [prompt-civilization, prompt-typing]
---

# core-prompt

`AuthorityEffect: None.` Review and packetize; never send, execute, certify, or promote.

## Workflow

1. Preserve the operator's original prompt as exact UTF-8 bytes. Never overwrite it.
2. Propose the strict structure in [prompt_proposal.md](references/prompt_proposal.md). Treat every model-filled field as untrusted.
3. Run `scripts/core_prompt.py review` with the original file, proposal JSON, and v0 runtime registry. The registry must remain empty until an external admission validator exists.
4. Present the original, typed rewrite, findings, nonclaims, unresolved questions, and requested effects. Do not hide an error finding.
5. If clarification is required, ask for it and repeat review. Do not approve a red bundle.
6. After explicit operator approval, run `approve`. Run `packetize` only when a Symbol Game turn packet is requested.

The CLI intentionally has no `send` operation. A host may suggest this skill for every consequential prompt, but v0 has no host-neutral pre-send enforcement hook.

## Boundaries

- Do not infer truth, hallucination, intent, or authorship from wording.
- Do not flag confidence words, citations, humor, strong language, or foreign languages by syntax alone.
- Do not let a proposed rewrite erase the original prompt or structured fields.
- Do not treat CAS integrity, a signature, a model verdict, or packetization as semantic verification.
- Do not edit `eis/antiskills/admitted/` or its registry from this skill.
- Preserve `AuthorityEffect: None`; operator approval does not grant execution capability.

Use the deterministic runtime for structure and IDs. Use judgment only to propose field contents, and expose uncertainty in `unresolved_questions`.

## Constraints

Required: [EVIDENCE_BASED, NO_HARDCODED_SECRETS, and MAINTAIN_TESTS](../_shared/constraints.md). This skill never self-certifies, bypasses a gate, or grants authority.

## Outputs and Tests

Outputs: `core.prompt.review-bundle.v1`, `core.prompt.approved.v1`, and the existing Symbol Game `packet-envelope.v2` wire.

Verification command:

```bash
python operads/skills/core-prompt/scripts/core_prompt.py review --help
```

## Related Skills

`auto-anti-skill` proposes inert anti-skill candidates. `human-promotion-firewall` owns the separate human-promotion boundary.
