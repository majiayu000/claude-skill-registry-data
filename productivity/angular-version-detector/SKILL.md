---
id: angular.upgrade.angular-version-detector
name: Angular Version Detector
description: >
  Detects the installed Angular major and related compatibility evidence from the repository so upgrade planning can choose the correct next hop.
stack:
  - Angular
  - TypeScript
  - RxJS
category: upgrades
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular version detection
  - package version scan
  - compatibility check
  - source version evidence
compatibility:
  angular:
    min: "2"
    max: "21"
---

# Angular Version Detector

## Purpose

Use this skill to detect the installed Angular major and the compatibility evidence needed for upgrade planning.

This skill only gathers version facts. It does not plan hops, change code, or run migrations.

## When to Use

Use this skill when:

- The Angular major is unknown or needs confirmation.
- The upgrade orchestrator needs version evidence.
- You must inspect dependency compatibility before selecting the next hop.
- The repository may contain Angular, TypeScript, RxJS, or zone.js constraints.

## When Not to Use This Skill

Do not use this skill when:

- The source Angular major is already known and confirmed.
- The task is a bounded hop or code migration.
- The repository is AngularJS-only and needs legacy modernization instead.
- The user wants implementation rather than version evidence.

## Inputs Expected

- `package.json`
- lockfile
- Angular package versions
- TypeScript version
- RxJS version
- zone.js version
- Angular CLI or workspace config
- build scripts if relevant

## Compatibility by Version

| Evidence area    | Strategy recommended                                            | Observations                                           |
| ---------------- | --------------------------------------------------------------- | ------------------------------------------------------ |
| Angular packages | Read installed versions from project files                      | Use the exact major from the repository, not memory.   |
| TypeScript       | Record the installed version and compare against the target hop | Do not guess the supported range.                      |
| RxJS             | Record the installed version and compare against the target hop | Upgrades may require compatible operator usage.        |
| zone.js          | Record the installed version if present                         | Some major hops require matching runtime expectations. |

If a version cannot be confirmed from the project files, mark it as `verify in project`.

## Procedure

1. Read `package.json`.
2. Read the lockfile if present.
3. Extract Angular package versions.
4. Extract TypeScript, RxJS, and zone.js versions.
5. Check workspace or CLI config if needed.
6. Summarize the detected source major.
7. Pass the result to the orchestrator or route planner.

## Do

- Capture exact version evidence from the repository.
- Distinguish confirmed versions from inferred versions.
- Record whether Angular packages are aligned or mixed.
- Note if the project uses Angular CLI, Nx, or a custom workspace.
- Keep the output factual and minimal.

## Recommended Patterns

Return a compact evidence table:

| Package         | Version | Status                         |
| --------------- | ------- | ------------------------------ |
| `@angular/core` | `x.y.z` | confirmed                      |
| `typescript`    | `x.y.z` | confirmed                      |
| `rxjs`          | `x.y.z` | confirmed                      |
| `zone.js`       | `x.y.z` | confirmed or verify in project |

Add a compatibility note:

```txt
source major = 12
target planning must continue hop-by-hop
```

## Anti-Patterns

- Guessing the version from app behavior.
- Using the latest Angular release as the assumed source.
- Treating partial evidence as confirmed.
- Mixing detection with dependency changes.
- Returning upgrade advice before version facts are collected.

## Do Not

- Do not modify dependency files.
- Do not install packages.
- Do not plan the next hop here.
- Do not run commands that do not exist in `package.json`.
- Do not claim version certainty without repository evidence.

## Review Checklist

- [ ] `package.json` was read.
- [ ] Lockfile evidence was checked when available.
- [ ] Angular major was identified or marked verify in project.
- [ ] TypeScript, RxJS, and zone.js were recorded.
- [ ] Workspace or CLI context was noted.
- [ ] No code was changed.

## Validation Minimum

Use only repository commands that actually exist.

Prefer:

- build
- test
- lint

If validation cannot run, report the blocker and the safest next step.

## Risks

- Mixed Angular versions can make the detected source major ambiguous.
- Missing lockfiles can hide the actual installed versions.
- A workspace can contain multiple Angular projects with different versions.

## Expected Output

When this skill is used, return:

1. Detected Angular major.
2. TypeScript, RxJS, and zone.js versions.
3. Evidence source.
4. Compatibility notes.
5. Next skill to use.

## Exit Criteria

This skill is complete only when:

- The source Angular major is identified or marked verify in project.
- Compatibility versions are recorded.
- No dependency or code changes have been made.
