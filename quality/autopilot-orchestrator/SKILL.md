---
id: core.autopilot-orchestrator
name: Autopilot Orchestrator
description: >
  Defines the main NgAutoPilot workflow for understanding a task, detecting project context, selecting the smallest skill, assessing risk, applying a minimal change, and validating the result.
stack:
  - Angular
  - TypeScript
  - JavaScript
category: core
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - autopilot workflow
  - start task
  - choose skill
  - analyze before coding
  - NgAutoPilot orchestration
---

# Autopilot Orchestrator

## Purpose

Use this skill as the main operating workflow for NgAutoPilot. The goal is to make the agent understand the task, inspect the project, select the smallest useful skill, assess risk, apply the minimum safe change, and validate the result before reporting back.

NgAutoPilot is not a prompt warehouse. It is a technical assistance layer for analyzing, deciding, modifying, and validating changes with version compatibility and risk control.

## When to Use

Use this skill when:

- A development task starts and the correct specialized skill is not obvious.
- The task may affect Angular, TypeScript, JavaScript, RxJS, testing, architecture, or quality.
- The project stack or version is unknown.
- The user asks for an implementation, refactor, review, migration, or diagnosis.
- The work may require multiple smaller decisions before editing code.

## When Not to Use

Do not use this skill when:

- The user asks a simple factual question that does not require repository analysis.
- A more specific skill has already been selected and no routing decision remains.
- The task is purely conversational and no technical action is expected.

## Inputs Required

Collect only the minimum useful context:

```txt
user goal
affected files or area
project type
framework and version
package manager
test and lint commands
existing project instructions
current git status
known constraints or compatibility requirements
```

If an input is missing, infer from repository files before asking the user.

## Version Compatibility

This core workflow is stack-agnostic. For version-sensitive decisions, delegate to `core.stack-version-detection` and `core.compatibility-router`.

For Angular work, never assume the latest Angular version. Detect the version first, then choose compatible patterns.

## Decision Rules

Apply this routing order:

```txt
1. Understand the user's goal.
2. Inspect project context.
3. Detect stack and versions.
4. Select the smallest applicable skill.
5. Assess risk.
6. Plan the smallest reversible change.
7. Implement only the requested scope.
8. Validate with the narrowest useful command.
9. Report changes, risks, and next steps.
```

Prefer one focused skill over multiple broad skills. Add a second skill only when the task clearly crosses boundaries.

## Execution Workflow

Use this workflow:

```txt
Task intake -> project intake -> version detection -> skill routing -> compatibility routing -> risk assessment -> implementation -> validation -> handoff
```

## Subagent Registry

When `agents/ngautopilot/subagents/` is available, treat it as the stable registry for focused reviewer and specialist roles. Invoke only the smallest relevant subagent after skill routing or at handoff; subagents provide oversight and do not replace NgAutoPilot skill selection.

Before editing, state the working assumption internally:

```txt
This task is a bug fix, refactor, migration, review, generation, or documentation task.
The affected area is local, feature-level, app-level, or repository-level.
The risk is low, medium, or high.
The selected skill is enough to proceed.
```

## Do

Recommended operating pattern:

```txt
Select the minimum skill that can solve the task.
Use compatible APIs for the detected stack.
Keep changes small and reversible.
Validate close to the changed area.
Explain residual risk.
```

## Do Not

Avoid broad autopilot behavior:

```txt
Load every skill, rewrite architecture, modernize unrelated code, and run large validations without a reason.
```

Avoid using modern syntax just because it is available globally in the model's knowledge.

Avoid mixing unrelated refactors with the user's requested outcome.

## Output Format

Use this format for non-trivial tasks:

```md
## Diagnosis

- ...

## Selected Skill

- ...

## Change Plan

1. ...

## Validation

- ...

## Risks

- ...
```

## Review Checklist

- [ ] The task goal is clear.
- [ ] Project context was inspected before editing.
- [ ] Stack and version constraints were considered.
- [ ] The smallest applicable skill was selected.
- [ ] Risk was classified before implementation.
- [ ] The change is focused and reversible.
- [ ] Validation was run or a concrete validation command is provided.

## Risks

- Over-routing can waste time and tokens.
- Under-routing can apply the wrong pattern.
- Large automated refactors can create merge risk.
- Version assumptions can produce uncompilable code.

## Examples

```txt
User: Improve this slow Angular table.
Route: project-intake -> stack-version-detection -> skill-router -> compatibility-router -> angular.performance.list-rendering-optimization -> risk-assessment
```

```txt
User: Refactor this component to be more maintainable.
Route: project-intake -> skill-router -> angular.architecture.angular-patterns-senior -> risk-assessment
```

## Expected Output

1. Identify the task type and project context.
2. Select the smallest applicable skill.
3. Apply version and risk guardrails.
4. Execute the smallest safe change.
5. Validate and report the result clearly.
