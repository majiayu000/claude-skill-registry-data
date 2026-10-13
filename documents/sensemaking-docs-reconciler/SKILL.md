---
name: sensemaking-docs-reconciler
description: challenge the sensemaking repository's architecture against its documentation, registries, templates, and examples. update CONTEXT.md glossary, registries, or contracts only after the user approves the resolution. use to resolve vocabulary drift, out-of-sync registries, or stale artifact contracts.
---
# sensemaking-docs-reconciler

Ensures that the stable domain language and technical contracts of the sensemaking ecosystem remain in sync with the actual implementation.

## Workflow
1. **Audit**: Compare `CONTEXT.md` (Glossary), `skill-registry.yaml`, `artifact-contracts.yaml`, and `README.md`.
2. **Challenge**: Identify "Vocabulary Drift" (e.g., a skill is renamed but the glossary uses the old name) or "Contract Drift" (e.g., a template has 13 sections but the PRD says 11).
3. **Resolve**: Present the mismatch to the user and suggest a canonical resolution.
4. **Mutate**:
    - Update `CONTEXT.md` for domain language alignment.
    - Update registries/contracts for technical alignment.
    - Create ADRs for significant architectural changes.

## Mutate Rules
- **Glossary Only**: Casual updates are only permitted for `CONTEXT.md` glossary terms.
- **Contract Approval**: Registry or contract changes require explicit user confirmation of the new schema.
- **No Side Effects**: This skill must not modify skill logic, implementation code, or workflow execution behavior.

## Domain Language Focus
- fog, problem frame, unknowns map, weakest boundary, artifact contract, execution mode, approval gate, handoff failure.

## References
- [CONTEXT.md](../../CONTEXT.md)
- [Artifact Contracts](../../skills/workflow-orchestrator/references/artifact-contracts.yaml)
- [Skill Registry](../../skills/workflow-orchestrator/references/skill-registry.yaml)
