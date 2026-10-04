---
id: core.risk-assessment
name: Risk Assessment
description: >
  Classifies change risk before code edits and forces small, reversible implementation plans for refactors, architecture changes, migrations, dependencies, routing, build, state, and public APIs.
stack:
  - Angular
  - TypeScript
  - JavaScript
category: core
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - assess risk
  - change risk
  - risky refactor
  - architecture change
  - migration risk
  - safe change plan
---

# Risk Assessment

## Purpose

Use this skill to classify risk before editing code. The goal is to keep changes small, reversible, testable, and aligned with the user's actual request.

## When to Use

Use this skill when:

- The change touches architecture, state management, routing, bootstrap, build, dependencies, public APIs, generated code, or shared libraries.
- The user asks for a broad refactor.
- The implementation may affect many files.
- Tests are missing or unclear.
- The task could introduce behavior changes.
- The agent is tempted to modernize unrelated code.

## When Not to Use

Do not use this skill when:

- The change is a small documentation edit.
- The task is a localized typo, copy, or metadata update.
- The risk has already been assessed and no scope changed.

## Inputs Required

Collect:

```txt
files affected
runtime behavior affected
public API affected
test coverage nearby
build or dependency impact
state ownership impact
version compatibility impact
rollback path
user-requested scope
```

## Version Compatibility

Use `core.compatibility-router` when risk depends on framework or tooling version.

Version-sensitive changes are at least medium risk unless they are documentation-only.

## Subagent Review Triggers

When `agents/ngautopilot/subagents/` is available, use subagents only as targeted reviewers for the risk that was actually detected. For example, use the Spartan Contrarian Developer for broad implementation risk, the Compatibility Gatekeeper for version or dependency risk, the Testing Hoplite for test stability risk, and the Roman Consolidator only for final delivery consolidation.

## Decision Rules

Classify risk:

```txt
Low:
  documentation-only
  isolated skill content
  small local code change with no behavior impact
  catalog regeneration

Medium:
  local refactor with tests
  component or service behavior change
  RxJS operator change
  new tests or test strategy adjustment
  local architecture split

High:
  routing, bootstrap, build, dependency, or package manager changes
  public API changes
  shared library contracts
  state management model changes
  migrations across Angular versions
  broad formatting or codemod changes
  security-sensitive changes
```

Escalate risk when:

```txt
tests are missing
the change touches many files
the change affects shared packages
the behavior is hard to observe locally
version compatibility is uncertain
rollback is unclear
```

## Execution Workflow

Use this workflow:

```txt
1. Identify affected scope.
2. Classify risk.
3. Define smallest reversible change.
4. Define validation command.
5. Identify rollback path.
6. Implement only within approved scope.
7. Report residual risk.
```

## Do

Recommended risk pattern:

```txt
Split broad refactors into small commits or PRs.
Prefer local behavior-preserving changes.
Validate with the narrowest relevant test first.
Flag when a safer staged plan is better than a single large change.
```

## Do Not

Avoid high-risk autopilot behavior:

```txt
Replace the state model, routing, build system, and component architecture in one change.
```

Avoid "while here" refactors.

Avoid changing public APIs without calling out consumer impact.

Avoid dependency upgrades as part of unrelated implementation work.

## Output Format

Use this format:

```md
## Risk Assessment

- Risk level:
- Scope:
- Behavior impact:
- Compatibility impact:
- Test coverage:
- Rollback path:

## Safe Plan

1. ...

## Validation

- ...

## Residual Risks

- ...
```

## Review Checklist

- [ ] Risk level is classified before implementation.
- [ ] The proposed change is the smallest useful change.
- [ ] Public API and shared library impact are considered.
- [ ] Version compatibility is considered.
- [ ] Tests or validation commands are identified.
- [ ] Rollback path is clear.
- [ ] Unrelated refactors are avoided.

## Risks

- Underestimating risk can break consumers or deployment.
- Overestimating risk can block useful small improvements.
- Missing tests increase uncertainty.
- Broad changes create review and merge risk.

## Examples

```txt
Low risk:
Add a new markdown skill and regenerate catalog.
```

```txt
Medium risk:
Refactor one Angular component into container and presentational components with tests.
```

```txt
High risk:
Replace shared RxJS state service with Signals in a library consumed by unknown Angular versions.
```

## Expected Output

1. Classify the change risk.
2. Propose a small reversible plan.
3. Identify validation steps.
4. Avoid unrelated or high-risk expansion.
5. Report residual risk clearly.
