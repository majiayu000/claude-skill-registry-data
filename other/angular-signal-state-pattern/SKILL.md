---
id: angular.signals.angular-signal-state-pattern
name: Angular Signal State Pattern
description: Model feature state with signals while keeping derived state and effects separated.
stack:
  - Angular
category: signals
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - signal state
  - state pattern
  - signals state
compatibility:
  angular:
    min: "16"
---

# Angular Signal State Pattern

## Purpose

Model feature state with signals while keeping derived state and effects separated.

This skill keeps the signals decision explicit: identify the current state, choose the smallest safe action, document compatibility evidence, and leave a validation path that another agent or maintainer can repeat.

## When to Use

Use this skill when:

- the task mentions angular signal state pattern, signals, computed, effects, RxJS interop, or signal state;
- an Angular codebase needs a scoped signals decision before implementation;
- compatibility, risk, or ownership is unclear and should be made explicit;
- the output must be reusable by another agent, reviewer, or release owner.

## Do

- Inspect the current Angular version, TypeScript version, build tooling, and affected files before recommending changes.
- Keep the change bounded to the requested workflow and preserve separate upgrade, modernization, and cleanup tracks.
- Prefer documented Angular APIs and local project conventions over new abstractions.
- Record assumptions, compatibility evidence, validation commands, and rollback notes.
- Add or update focused tests when the workflow changes runtime behavior.

Recommended workflow:

```txt
1. Identify the affected Angular feature area and version constraints.
2. Classify the change as migration, modernization, architecture, validation, or cleanup.
3. Apply the smallest reversible implementation or write the decision artifact.
4. Validate with the project test, lint, build, or review command that matches the risk.
5. Summarize remaining risks and the next safe checkpoint.
```

## Do Not

- Do not combine this workflow with an unrelated Angular major-version hop.
- Do not invent compatibility data, CLI flags, or framework behavior.
- Do not introduce dependencies unless the local implementation requires them.
- Do not rewrite a complete architecture layer when a targeted boundary or decision is enough.
- Do not mark the work complete without a concrete validation or a clear reason validation could not run.

Avoid:

```txt
Changing framework version, architecture, tests, and cleanup policy in one unreviewable step.
```

## Review Checklist

- [ ] The Angular and tooling versions are known or explicitly called out as unknown.
- [ ] The signals scope is isolated from unrelated work.
- [ ] The recommendation uses documented APIs or existing project patterns.
- [ ] Compatibility evidence is included when version-specific behavior matters.
- [ ] Tests, build, lint, or manual validation steps are listed.
- [ ] Rollback or follow-up notes exist for risky changes.

## Expected Output

1. Summarize the finding in one concise paragraph.
2. List the files, APIs, or project boundaries affected.
3. Provide the smallest safe implementation or decision.
4. Explain compatibility and risk assumptions.
5. Provide validation commands or review checks.
6. Separate follow-up work from the current scope.
