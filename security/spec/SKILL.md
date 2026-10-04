---
name: spec
description: Start spec-driven DegenExus development with explicit source-of-truth, constraints, and verification strategy.
disable-model-invocation: true
argument-hint: "[feature or change request]"
---

# Spec Workflow

Canonical `/spec` workflow. Use this skill for spec-driven development starts and keep command files as shims only.

## Sources of Truth

- Routing contract: `.claude/rules/synergy-contract.yml`
- Evidence schema: `.claude/rules/evidence-schema.yml`
- Edge-case review: `.claude/skills/edge-case-audit/SKILL.md`

## Workflow

1. Clarify objective, users, scope, non-goals, and risk surfaces.
2. Identify source-of-truth state for each behavior.
3. Document commands, project structure, code style, testing strategy, and boundaries.
4. Include security, prompt-safety, risk-gate, data-integrity, and persistence considerations when relevant.
5. Include acceptance criteria, FSV evidence expectations, and at least three edge cases.
6. Confirm with the user before implementation.

If asked to save the spec, use `SPEC.md` or the user-specified path.

## Output

Emit a spec that names affected sources of truth, verification commands, routed specialists, edge cases, and `.claude/rules/evidence-schema.yml` evidence expectations.
