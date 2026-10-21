---
name: skill-authoring
description: Improve skills using concise instructions, portable resources and real evaluation. Triggers on "write a skill", "写技能".
---

# Skill Authoring

## When to use

- Improve skills using concise instructions, portable resources and real evaluation.

**Not for:** using-skills for routing; spec for product requirements.

## Steps

1. Read the anatomy, identify a demonstrated gap and compare relevant real skills; select positive and adjacent negative tasks.

2. Write concise intent metadata, task-specific steps and evidence checks; keep generic knowledge and platform mechanics out of the runtime core.

3. Verify resource portability and approved outputs, update discovery surfaces, generate adapters and run structure and installation checks.

4. Run representative model tasks when available and compare quality, failures and extra work against baseline; report harness, references and unrun checks.

## Verify

- Metadata, resources and installed behavior agree; static checks are not presented as incremental model benefit.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [skill-anatomy.md](../../../references/skill-anatomy.md) — the anatomy this skill enforces: folder layout, frontmatter, four sections, Output convention, progressive disclosure, description hybrid format, superset-of-official-spec note.
- [references/eval-tiers.md](references/eval-tiers.md) — the three eval tiers (structural / trigger-routing / behavioral) in detail, with the prompt-template for routing eval.
