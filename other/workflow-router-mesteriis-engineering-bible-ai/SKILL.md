---
name: workflow-router
description: "Routes ambiguous or multi-domain engineering requests to the smallest ordered skill set. Do not use for clear single-skill work or same-task follow-ups."
---

# Workflow Router

Use this router only when the request is genuinely ambiguous, spans multiple
engineering domains, or needs an ordered handoff between workflows. A directly
requested leaf skill takes precedence.

## Fast Path

- Clear single-domain request: choose the narrowest leaf skill directly and do
  not use this router.
- Same-task follow-up: reuse the active route. Do not reread an unchanged
  `SKILL.md` already available in the conversation.
- Changed domain, risk class, external system, or requested workflow: route only
  the changed portion.

## Workflow

1. Classify the request by concrete deliverable and mutation risk.
2. Select one primary skill and at most one supporting skill by default.
3. Add another skill only when it contributes a distinct required procedure or
   evidence type.
4. Read only selected skills whose instructions are not already available.
5. Order mixed work by dependency, usually evidence or design before mutation,
   then validation.
6. If the common routes below are insufficient, read
   `references/routes.md` for the exhaustive route table.

## Author-Maintained Providers

Keep owner rules and route policy separate from the author's workflow. For a
catalog intent, `be skills route INTENT --json` resolves the reviewed provider
and its local dependency state without installation or an author update check.
Use an explicitly named, current-session skill first. Otherwise load the actual
compatible upstream instructions only when exposed by the host; files alone
mean exposure is unverified. Report missing providers, setup, or a pending reload.

Install missing reviewed dependencies through the selected profile's lifecycle;
reuse compatible native providers. Updates use a separate, explicitly selected
reviewed pin. Preserve the complete author tree and dependencies; never replace
it with a summary or silently bypass conflicting steps. Keep personal policy
separate, same-task routes stable and avoid per-turn lifecycle probes.

## Common Routes

- Bug or failure investigation: `superpowers.systematic-debugging` plus the
  relevant ecosystem skill.
- Behavior implementation: relevant ecosystem skill; add
  `superpowers.test-driven-development` when behavior coverage is required.
- Explicit review: `superpowers.requesting-code-review`; use `security-router`
  or `ui-router` when that domain is central.
- Refactor without behavior change: `refactoring` plus the ecosystem skill.
- Performance investigation: `performance` plus the ecosystem skill.
- Migration, architecture, multi-agent, external pack, durable memory, or
  runtime-capability selection: use the matching specialist route in the
  reference table.

`debugging`, `testing-tdd` and `code-review` are compatibility aliases that load
these original providers. They contain no author procedure.

## Output

Do not emit a routing preamble for an obvious route. Briefly state the route only
when the choice is ambiguous, the request needs multiple stages, or a limitation
changes the result.

## Healthcheck

When asked to verify installed routing, run:

```bash
bash ~/.codex/skills/workflow-router/scripts/validate-routing.sh
```
