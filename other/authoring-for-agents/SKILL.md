---
name: authoring-for-agents
description: Use when creating or changing agent instructions or their activation behavior. Skip edits that only correct spelling or formatting.
---

# Authoring for Agents

Write instructions for a named failure, a task-specific contract, or a repository
fact the agent cannot infer reliably. Remove generic advice that adds no behavior.

## Choose the surface

| Need | Owner |
|---|---|
| Policy needed on every task | AGENTS.md |
| Convention needed for particular work | Project document with a conditional AGENTS.md pointer |
| Repeated specialist workflow | Skill |
| Explicit human entrypoint | Manual skill or thin alias |
| Substantial material used by one branch | Conditional reference |
| Deterministic enforcement | Existing hook, check, or script where authorized |

Search for an existing owner before adding another. Keep shared semantics
provider-neutral; runtime configuration owns models, effort, permissions and
integration mechanics. Preserve scope restrictions on which files may change.

## Write

- Put the activation boundary first: positive cases and the nearest misleading
  case to skip. A description should select the skill, not duplicate its steps.
- Inline the common contract; link substantial optional material at the branch
  that needs it. Moving text behind an unconditional read does not save context.
- State outputs, material invariants, authority boundaries and stop conditions.
  Use exact recipes for fragile operations and judgment for routine choices.
- Prefer one effective instruction over repeated prohibitions or ritual steps.
  Treat wording techniques as hypotheses to evaluate, not psychological laws.

For structural choices, consult `references/writing-principles.md`; for skill
metadata, aliases and sidecars, consult `references/skill-anatomy.md`.

## Verify

Inspect the diff for lost contracts and conflicting callers. For descriptions or
routing changes, check a positive case and a nearby trivial/negative case through
the actual discovery surface when available. Scale fresh-context and pressure
trials to behavioral risk; methods are in `references/testing-docs.md`.

Structural checks establish packaging, not model behavior. Report unavailable
behavioral checks as a limit; do not manufacture evidence or bypass runtime
restrictions to run them. Revise the smallest instruction implicated by a failed
case, then recheck that case and its affected neighbors.
