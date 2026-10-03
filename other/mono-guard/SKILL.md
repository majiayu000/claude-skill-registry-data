---
name: mono-guard
description: Validate monorepo lane specs before dispatch and verify integrated changes stay inside declared lane boundaries
type: analysis
version: v0.1
argument-hint: "[--post-integration] [optional: lane-specs.json]"
---

# Mono Guard

Invoke as `$mono-guard`.

Use this skill to validate monorepo pack lane artifacts before parallel dispatch and to audit integrated lane changes after dispatch.

This pack-local `mono-guard` consumes `.agents/lane-specs.json` and `.agents/monorepo.json`. It preserves behavioral compatibility with the base `$mono-guard` contract while using the monorepo pack's JSON artifacts and scripts as the project-local enforcement surface.

## Augmentation Injection Pattern

`mono-guard` is the pack's safety gate for the augmentation injection pattern. `mono-exec` injects it before package-scoped dispatch, and `mono-ship` relies on its post-integration boundary checks before delegating to `$ship`. The skill augments existing run/ship workflows with monorepo lane enforcement rather than replacing their task selection, validation, history, commit, push, or deploy responsibilities.

## Modes

- **Pre-flight (default):** Validate `.agents/lane-specs.json` before `mono-exec` dispatches package-scoped lanes.
- **Post-integration (`--post-integration`):** Verify actual changed files from the integrated diff stay inside declared lane ownership and do not include unsafe shared files.

## Inputs

- `.agents/lane-specs.json`: generated lane plan with lifecycle, cross-cutting steps, lanes, `owns`, `must_not_edit`, `depends_on`, mode, and branch.
- `.agents/monorepo.json`: workspace detection output from `mono-detect`, including packages and internal dependency graph.
- `packs/monorepo/scripts/lane-spec-validate.sh`: schema and boundary validator for lane specs.

If `.agents/monorepo.json` is missing or stale, run `mono-detect` first. If `.agents/lane-specs.json` is missing, stop and recommend generating lane specs through `mono-exec`.

## Pre-Flight Workflow

1. Resolve the lane-spec file:
   - Use the path in `$ARGUMENTS` when provided.
   - Otherwise use `.agents/lane-specs.json`.
2. Run `packs/monorepo/scripts/lane-spec-validate.sh <lane-specs.json>`.
   - This verifies required fields, lifecycle state, disjoint `owns`, required root `must_not_edit` entries, valid `depends_on` references, unique non-primary branches, and duplicate step protection.
   - On failure, report `FAIL` and do not dispatch.
3. Read `.agents/monorepo.json`.
   - If missing, run or recommend `mono-detect`.
   - Use its `packages` and `dependency_graph` to evaluate package-aware safety.
4. Verify every lane's `owns` paths map to declared workspace package paths or clearly root-only serial work.
5. Verify every lane's `must_not_edit` includes lockfiles and shared root config files:
   - `pnpm-lock.yaml`
   - `package.json`
   - `pnpm-workspace.yaml`
   - `turbo.json`
6. Verify dependency ordering:
   - If package X depends on package Y and both packages are owned by different lanes, the lane for X must depend on the lane for Y directly or transitively.
   - Use `.agents/monorepo.json.dependency_graph` for dependency edges.
7. Verify lane dependency graph validity:
   - All `depends_on` references resolve to known cross-cutting step IDs or lane step IDs.
   - No lane dependency cycle exists.
8. Verify branch isolation:
   - Every write lane has a unique non-primary GitHub branch.
   - No lane branch is `main` or `master`.
   - If PR review is required by the execution profile but branch/PR evidence is missing after dispatch, report `FAIL`.
9. Scan lane descriptions, scopes, and modes when present for install/add intent.
   - Fail non-serial package lanes that instruct `pnpm install`, `pnpm add`, `npm install`, `yarn add`, or equivalent lockfile-modifying commands.
   - Warn on natural-language dependency changes such as "add dependency" or "install package".

## Post-Integration Workflow

1. Read `.agents/lane-specs.json` and `.agents/monorepo.json`.
2. Inspect the integrated diff with `git diff --name-only` unless the user supplied a different reviewed diff range.
3. For each changed file:
   - Flag any lockfile modification from a parallel lane as `FAIL`.
   - Flag root config changes as `WARN` unless they are declared in a serial cross-cutting step.
   - Verify the path is inside at least one declared lane `owns` path or an allowed serial cross-cutting/root scope.
   - Flag files outside declared ownership as boundary violations.
4. Verify consolidation/PR review evidence when lane specs record branch-backed dispatch:
   - Every integrated lane must have branch, commit SHA, and PR URL evidence recorded in `tasks/lane-specs.md` or the dispatch report.
   - Missing PR review evidence is `FAIL` because package lanes must not bypass consolidation review.
5. Report violations without reverting, fixing, or editing task files.

## Output

```markdown
### Mono Guard Report

**Mode:** pre-flight | post-integration
**Lane spec:** .agents/lane-specs.json
**Monorepo artifact:** .agents/monorepo.json
**Verdict:** PASS | WARN | FAIL

#### Results

| Check | Verdict | Details |
|---|---|---|
| Lane-spec schema | PASS | lane-spec-validate.sh passed |
| Owns disjointness | PASS | all lane owns paths are disjoint |
| Shared file exclusions | PASS | lockfile and root config paths are in must_not_edit |
| Branch isolation | PASS | each write lane has a unique non-primary GitHub branch |
| Dependency ordering | PASS | package dependency lanes are ordered |
| Integrated diff boundaries | WARN | one root config changed in serial integration |

#### Failures

- List blocking issues with lane IDs, step IDs, paths, and specific fixes.

#### Warnings

- List advisory issues with recommended follow-up.
```

## Verdicts

- **PASS:** Safe to dispatch or ship.
- **WARN:** Advisory issues found; review before proceeding.
- **FAIL:** Dispatch or shipping is blocked until the lane specs or integrated changes are corrected.

## Constraints

- Do not edit task files.
- Do not run package manager install/add commands.
- Do not modify `.agents/lane-specs.json` or `.agents/monorepo.json` except by invoking the designated generation/detection skills when appropriate.
- Do not revert or repair post-integration changes; report violations only.
- Keep behavior compatible with the base `$mono-guard` safety contract.

## Next-Step Routing

- **PASS pre-flight:** `$mono-exec` to dispatch the validated lanes.
- **WARN pre-flight:** Review warnings, then `$mono-exec` if accepted.
- **FAIL pre-flight:** Fix or regenerate `.agents/lane-specs.json`, then rerun `$mono-guard`.
- **PASS post-integration:** `$mono-ship` for package-scoped validation and shipping.
- **WARN/FAIL post-integration:** Resolve boundary issues, then rerun `$mono-guard --post-integration`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
