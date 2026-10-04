---
id: angular.upgrade.angular-major-hop-executor
name: Angular Major Hop Executor
description: >
  Executes exactly one Angular major-version hop, applies the bounded dependency and code changes required for that hop, and stops before the next version.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - major hop executor
  - single Angular hop
  - Angular version step
  - upgrade execution
compatibility:
  angular:
    min: "2"
    max: "21"
---

# Angular Major Hop Executor

## Purpose

Use this skill to execute exactly one Angular major-version hop in a controlled way.

This skill applies the bounded dependency and code changes for one hop, then stops. It does not plan the full route and does not begin the next hop automatically.

## When to Use

Use this skill when:

- The route planner has selected the next hop.
- The validation gate is ready to enforce a post-hop check.
- The repository is on a supported Angular major and needs one major step forward.
- The upgrade must remain bounded and reversible.

## When Not to Use This Skill

Do not use this skill when:

- The source Angular major is unknown.
- The route has not been planned.
- The validation gate is unavailable or has already failed.
- The task is AngularJS modernization instead of Angular 2+ upgrades.

## Inputs Expected

- Next hop from the route planner
- Source and target majors for the hop
- Dependency files
- Compatibility constraints
- Validation gate result
- Rollback expectations

## Compatibility by Version

| Hop                   | Strategy recommended                         | Observations                              |
| --------------------- | -------------------------------------------- | ----------------------------------------- |
| Any Angular major hop | Upgrade one major at a time                  | Validate after the hop and stop.          |
| Angular 2-4           | Use the dedicated early-hop rules            | Preserve older compatibility constraints. |
| Angular 5+            | Continue with the next matching hop executor | Do not batch majors.                      |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Read the selected hop.
2. Inspect the repository version evidence.
3. Apply the bounded dependency changes for that single hop.
4. Make the minimal code changes required by the hop.
5. Run the validation gate.
6. Stop immediately after validation.
7. Report the next hop without executing it.

## Do

- Execute exactly one hop.
- Keep dependency changes aligned to the selected version step.
- Apply only the code changes needed by that hop.
- Validate immediately after the hop.
- Preserve rollback clarity.
- Stop before the next hop begins.

## Recommended Patterns

Use this skill as the worker beneath the route planner and validation gate:

```txt
route planner -> hop executor -> validation gate -> stop
```

Keep the hop result explicit:

```md
## Hop Result

- executed hop: 12 -> 13
- validation: pass
- next hop: 13 -> 14
```

## Anti-Patterns

- Executing more than one major hop in a single run.
- Modifying unrelated files during the hop.
- Skipping validation after the hop.
- Planning the next hop before the current one is validated.
- Treating a hop executor as a route planner.

## Do Not

- Do not start the next major hop automatically.
- Do not change AngularJS modernization scope.
- Do not invent commands or dependency versions.
- Do not run commands that do not exist in `package.json`.
- Do not hide validation failures.

## Review Checklist

- [ ] Exactly one hop was executed.
- [ ] Dependency changes match the selected hop.
- [ ] Code changes were bounded to that hop.
- [ ] Validation gate was run or checked.
- [ ] The next hop was not started.
- [ ] Rollback path remains clear.

## Validation Minimum

Use only repository commands that actually exist.

Prefer:

- build
- test
- lint

If validation cannot run, report the blocker and stop.

## Risks

- A hop may require unexpected manual fixes in templates or APIs.
- Dependency alignment can cascade into TypeScript or RxJS constraints.
- Skipping validation can hide breakage until later hops.

## Expected Output

When this skill is used, return:

1. Executed hop.
2. Dependency and code changes applied.
3. Validation gate result.
4. Remaining risks.
5. Next hop to schedule.

## Exit Criteria

This skill is complete only when:

- One hop has been executed.
- Validation has been run or explicitly blocked.
- The next hop has not been started.
