---
name: agent-workflow
description: Use for any non-trivial change in this repository when an agent must discover applicable skills, manage context, select patterns, implement incrementally, test, review, simplify, and verify the result.
license: MIT
---

# Agent Workflow

## Purpose

Provide the repository-local execution contract for agent-assisted Ruby/Rails engineering. This skill adapts the external Agent Skills workflow to this repository's skill, pattern, evaluation, and validation system.

## Activate when

- starting a non-trivial task
- multiple repository skills may apply
- a design pattern or abstraction is being considered
- a cross-file change is planned
- an agent is reviewing or modifying another agent's work
- benchmark/evaluation infrastructure is changing

## Repository inspection

Before implementation, inspect:

- `skill-manifest.yml`
- relevant `skills/*/SKILL.md`
- relevant `patterns/*`
- tests and validators
- runtime/version configuration
- existing repository conventions
- benchmark/evaluation contracts when evaluation infrastructure is involved

## Workflow

```text
discover
  -> inspect
  -> clarify assumptions/conflicts
  -> choose smallest design
  -> implement incrementally
  -> test
  -> review
  -> simplify
  -> verify
```

Do not skip discovery merely because the requested change appears obvious.

## Skill selection

Select the smallest set of skills that covers the task.

Always consider:

- `ruby-clean-code`
- `ruby-tdd-refactoring`
- `stack-minimality`

`stack-minimality` is a cross-cutting modifier, not the owner of the business or framework contract. The focused domain skill remains Primary.

Add focused skills for the actual behavior. For cross-layer Rails changes, include `rails-architecture` and the relevant Rails boundary skill.

Patterns are optional. Select a pattern only when repository evidence or task requirements justify it.

## Routing quality

- Treat activation triggers as signals, not automatic routing verdicts.
- Select a **Primary skill** that owns the dominant engineering boundary.
- Add **Secondary skills** for dependent constraints or additional execution boundaries.
- Do not choose a skill only because a trigger token appears.
- Inspect the repository and consult router/ROUTING.md before resolving overlapping ownership.
- Use router/ROUTING_CASES.yml as adversarial routing guidance for high-risk boundary overlaps. This is the repository's routing quality contract.
- Do not create a new skill merely because a task crosses two existing boundaries.

## Pattern-selection rule

Use this evidence order:

1. explicit task requirement
2. existing repository pattern
3. framework/runtime constraint
4. focused skill guidance
5. repository pattern catalog
6. generic design preference

If the direct implementation is simpler and satisfies the contract, prefer the direct implementation.

## Pre-activation fact gate

Before implementation, classify each task-critical fact as `observed`, `derived`, `inferred`, or `unknown`. Implementation is blocked while any task-critical fact is `inferred` or `unknown`. Load `references/fact-gate.md` for the classes, the manifest format, and the gate rule.

## Implementation loop

When the work is not yet decided or is larger than one session, plan first with the planning layer: `planning-interview` to settle decisions, `planning-spec` to write them up, `planning-tickets` to slice them, and `planning-wayfinder` for multi-session efforts, all through `planning-tracker`. Take one ticket per session.

When a spec, ticket, or agreed plan exists:

1. Agree the test seams (see `ruby-tdd-refactoring`), then work test-first in vertical slices at those seams.
2. Run the single test file after each slice and the repository's linters or type checks regularly.
3. Run the full suite once at the end, not after every slice.
4. Review the diff with `change-review` against the repository's standards and the originating spec before committing.

## Change discipline

- Keep each slice independently verifiable.
- Do not mix unrelated cleanup with feature work.
- Do not create generic Manager/Processor/Service abstractions without a concrete responsibility.
- Keep public interfaces explicit.
- Preserve compatibility unless intentionally changing it.

## Review

Review the implementation across:

- correctness
- readability/simplicity
- architecture
- security
- performance
- scope

Then ask whether every abstraction earns its complexity.

For a diff that is ready to hand off, run `change-review`: it reports repository standards and spec fidelity as two separate axes. Add `stack-minimality-review` when the question is only whether the change can be smaller.

## Reference example

A minimal task-routing decision that mirrors the workflow contract: classify, inspect, then select the smallest covering skill set.

```ruby
# Sketch of the routing decision an agent makes before editing files.
CANDIDATES = {
  "add password reset to a Rails controller" => %w[rails-authentication rails-security rails-test-engineering],
  "extract a service object from a controller" => %w[ruby-service-objects ruby-poro ruby-clean-code],
  "fix a flaky system test" => %w[rails-test-engineering ruby-tdd-refactoring]
}

def select_skills(task)
  CANDIDATES.fetch(task).then { |all| all.take(2) } # smallest covering set
end

task = "fix a flaky system test"
selected = select_skills(task)
raise "primary missing" unless selected.first == "rails-test-engineering"
puts "task: #{task}"
puts "selected: #{selected.join(', ')}"
```

## Agent review checklist

- [ ] applicable skills discovered
- [ ] repository inspected before implementation
- [ ] ambiguity resolved
- [ ] smallest justified pattern selected
- [ ] stack-minimality applied without weakening required guarantees
- [ ] test seams agreed before test-first work
- [ ] focused tests run
- [ ] diff reviewed on both standards and spec axes
- [ ] validators/CI-equivalent checks run
- [ ] final diff reviewed
- [ ] unrun checks disclosed

## Verification

Run:

1. focused tests
2. applicable repository validators
3. affected broader tests/CI-equivalent checks
4. final diff inspection

In a consuming Ruby/Rails project, `ruby bin/verify-change --base <base-ref> --strict` runs RuboCop, tests, Brakeman, bundler-audit, and `zeitwerk:check` as applicable and reports each check's status; report `overall.status`, and treat `incomplete` as not verified. See `docs/VERIFY_CHANGE.md`.

If a check cannot be run, state that instead of inferring success.

## References

Load only when needed; each reference is one level deep.

| Load when | Reference | Covers |
|---|---|---|
| a change depends on repository facts before implementation | [references/fact-gate.md](references/fact-gate.md) | Fact classes, manifest format, and the blocking rule |
| a run may change files outside the working tree, use credentials, run side-effecting commands, or spend a budget | [references/execution-control.md](references/execution-control.md) | Approval, credentials, checkpoints, undo, budgets, and provenance |

## Source foundation

This repository-local workflow is based on the external Agent Skills methodology, adapted to the Ruby/Rails skill library and its existing validation/evaluation architecture. It is workflow guidance rather than source-book content.

The implementation loop (test-first at agreed seams, focused tests per slice, one full-suite run, review before commit) is adapted from the `implement` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock).
