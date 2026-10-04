---
id: core.skill-router
name: Skill Router
description: >
  Selects the smallest useful NgAutoPilot skill based on user goal, affected area, detected stack, compatibility constraints, risk, and expected output.
stack:
  - Angular
  - TypeScript
  - JavaScript
category: core
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - route skill
  - select skill
  - choose micro-skill
  - skill selection
  - task routing
---

# Skill Router

## Purpose

Use this skill to select the smallest applicable NgAutoPilot skill for a task. The goal is to prevent loading broad or unrelated skills and keep the agent focused on the user's outcome.

## When to Use

Use this skill when:

- More than one skill could apply.
- The task spans performance, architecture, RxJS, TypeScript, testing, or quality.
- The user asks for a broad outcome such as "improve this", "make it better", "review this", or "refactor this".
- The selected skill must depend on version or risk.
- The agent needs to avoid applying every available skill.

## When Not to Use

Do not use this skill when:

- The user explicitly names a skill and it applies.
- The task is trivial and no skill is needed.
- A previous routing decision remains valid for the current action.

## Inputs Required

Use these inputs:

```txt
user goal
affected files
detected stack
detected versions
project type
task type: bug, feature, refactor, review, migration, test, documentation
risk level
available skill catalog
```

Read `catalog.json` and match by:

```txt
id
stack
category
status
triggers
path
```

## Version Compatibility

Route version-sensitive work through `core.compatibility-router` before applying a specialized skill.

If a specialized skill has compatibility metadata, prefer it over a generic skill.

## Decision Rules

Route by task intent:

```txt
unknown or broad task -> core.autopilot-orchestrator
repo context needed -> core.project-intake
version-sensitive recommendation -> core.stack-version-detection
API compatibility concern -> core.compatibility-router
large or risky change -> core.risk-assessment
Angular rendering performance -> angular.performance.performance-orchestrator
Angular architecture -> angular.architecture.angular-patterns-senior
Angular dependency injection, providers, tokens, injectors -> angular.dependency-injection
Angular 21 -> 22 upgrade -> skills/angular/upgrades/21-to-22/angular-21-to-22-upgrade-orchestrator/SKILL.md
Angular 22 domain risk -> select the narrow `angular-v22-*` satellite for that domain
TypeScript unsafe typing -> typescript.strict-types.avoid-any
RxJS nested subscriptions -> angular.rxjs.avoid-nested-subscriptions
Observable public contract -> angular.rxjs.observable-contracts
```

Prefer a micro-skill over an umbrella skill when the symptom is specific.

Use umbrella skills only to triage or coordinate.

If `agents/ngautopilot/subagents/` is present, use it only after selecting skills to choose the smallest relevant reviewer or specialist role for the task; do not treat subagent activation as a substitute for skill routing.

## Execution Workflow

Use this workflow:

```txt
1. Parse task goal.
2. Identify affected area.
3. Check catalog triggers.
4. Filter by stack and status.
5. Apply compatibility and risk filters.
6. Select one primary skill.
7. Select secondary skills only if necessary.
8. Explain the routing decision.
```

## Do

Recommended routing pattern:

```txt
Select one primary skill that can produce the requested output with the least context and least risk.
```

## Do Not

Avoid broad routing:

```txt
Load all Angular, TypeScript, performance, architecture, and quality skills for a single component change.
```

Avoid selecting a modern Angular skill when compatibility is unknown.

Avoid selecting an umbrella skill when a precise micro-skill directly matches the task.

## Output Format

Use this format:

```md
## Skill Routing

- Primary skill:
- Secondary skill:
- Reason:
- Compatibility gate:
- Risk gate:
```

## Review Checklist

- [ ] The selected skill matches the user's actual goal.
- [ ] The selected skill is the smallest useful skill.
- [ ] Compatibility-sensitive tasks include version routing.
- [ ] High-risk tasks include risk assessment.
- [ ] Umbrella skills are used only when needed.
- [ ] The routing decision is easy to explain.

## Risks

- Wrong routing can produce irrelevant code.
- Over-routing can create noisy recommendations.
- Under-routing can miss required guardrails.
- Routing without version detection can recommend unsupported APIs.

## Examples

```txt
Task: "This Angular list is slow."
Primary skill: angular.performance.list-rendering-optimization
Secondary skill: core.compatibility-router
```

```txt
Task: "This service does everything."
Primary skill: angular.services.single-responsibility-services
Secondary skill: core.risk-assessment
```

```txt
Task: "Fix this NullInjectorError or provider scope issue."
Primary skill: angular.dependency-injection
Secondary skill: core.compatibility-router
```

## Expected Output

1. Read the catalog.
2. Select one primary skill.
3. Apply compatibility and risk filters.
4. Avoid unrelated skills.
5. Explain the routing decision concisely.
