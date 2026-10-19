---
name: design-agent-capabilities
description: Design or review an agent's skills and tools. Use when deciding whether behavior belongs in instructions, deterministic code, a tool or toolset, or an Agent Skill; defining schemas and policies; classifying side effects and retries; or wiring explicit capability allowlists.
---

# Design Agent Capabilities

Turn an agent's responsibilities into a small, governed capability surface.

## Workflow

1. Inventory each behavior the agent needs and the data or side effects it touches.
2. Place each behavior in exactly one primary layer:
   - prompt or policy for compact behavioral constraints;
   - deterministic code for stable computation and validation;
   - tool for a callable operation or external capability;
   - skill for reusable procedural knowledge, examples, and supporting resources.
3. For every tool, define typed inputs and outputs, authorization, timeout, idempotency, retry safety, side effects, observability fields, and user-visible errors.
4. Classify every tool as `read`, `write_reversible`, or `write_consequential`, then document idempotency and approval separately.
5. For every skill, use Agent Skills-compatible packaging: a matching directory name and `SKILL.md` with only `name` and `description` required in YAML frontmatter.
6. Keep the main `SKILL.md` procedural and concise. Put detailed standards and examples in one-level `references/` files. Put executable utilities in `scripts/` and output materials in `assets/` only when needed.
7. Wire capabilities through an explicit per-agent allowlist. Deny undeclared capabilities.
8. Test schemas, authorization, retry semantics, denied paths, and representative skill-triggering prompts.

## Decision Rule

If the model only needs to know **how to reason or work**, use a skill. If it needs to **perform an operation**, use a tool. If behavior must be exact and repeatable, use deterministic code. Keep policy outside all three when it must be centrally governed.

Read [the capability standard](references/standard.md) before adding a skill or tool. Use [the examples](references/examples.md) for packaging and tool contracts.

## Guardrails

- Do not wrap every function as a tool.
- Do not use skills to smuggle credentials or bypass tool authorization.
- Do not mark a non-idempotent write as automatically retryable.
- Do not depend on a skill description to enforce runtime security.
- Do not duplicate a shared capability inside each agent without a documented reason.

## Completion Check

Confirm that each capability has one owner, a narrow contract, a risk classification, explicit consumers, negative-path tests, and traceable usage.
