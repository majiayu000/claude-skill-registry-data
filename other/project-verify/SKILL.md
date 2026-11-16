---
name: project-verify
description: "Create or maintain a project-local verification harness and feature map for a real app, CLI, or service."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-11-01"
  sources: "cursor/plugins 4dd1d05818d19792e7cd6e818f1667f95f7e1dbe pstack/skills/create-verification-skill/SKILL.md, pstack/skills/maintain-verification-skill/SKILL.md (adapted)"
---

# Project verification

Turn a project's real user journeys into a reusable harness. `verify` owns the proof standard; this skill supplies the app-specific commands and maintained feature map. Use `qa` for browser tool selection and browser evidence.

| Ask | Branch |
|---|---|
| Create a verification/control skill for this project | Create |
| Audit, refresh, or maintain an existing harness or feature map | Maintain |
| Run an existing journey without changing the harness | Read the project's verification skill, then use `verify` or `qa` |

## Locate the target

Find existing verification skills and harnesses before choosing a path: project instructions, `.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, scripts and test directories. Reuse the project's documented convention. Otherwise write `.agents/skills/verify-<app>/`; use a short app name derived from the repository. If several apps or harnesses fit and the request does not select one, ask which target rather than merging their launch models.

Use one canonical directory. If the active host does not discover that directory, point its project instructions to the canonical `SKILL.md` for explicit reading; do not create independent copies that drift. Add that pointer only when editing project instructions is within scope. Otherwise report the explicit read path.

Done when: the target app, canonical directory, and active host's way to reach it are known.

## Create

### 1. Discover the actual app

Read the existing run scripts, tests, configuration and user entry points. Record:

- Surface: browser, desktop/mobile UI, CLI/TUI, API, library, or a combination; identify the primary journey.
- Launch: the project's exact command, version/build, readiness signal, ports, auth and seed prerequisites.
- Drive: existing tests or control adapters first; real selectors, CLI commands or public API requests from this repo.
- Observe: the visible result plus consequential files, responses, logs or stored data.
- Ownership: existing shared instances, whether a second instance is supported, and isolated ports/data/profile paths when available.

Check the prerequisites read-only before launching. Reuse a healthy shared development stack when appropriate; do not restore/reset its database, change its ports, or replace its seed data to make the recipe pass. If a prerequisite is missing, record it and the attempted check. A blocked launch leaves a draft, not invented commands or a ready harness. Product fixes go through `debug` separately when authorized.

Done when: every launch/drive command and prerequisite has a repository source, and the target can be used safely or the exact blocker is recorded.

### 2. Write the harness contract

Create the canonical `SKILL.md`, `agents/openai.yaml` with `policy.allow_implicit_invocation: false`, and only the helpers this app needs. The generated skill is user-invoked and contains:

| Section | Required content |
|---|---|
| Launch | Exact command and usable readiness check; auth/migration/seed prerequisites; reusable shared-instance path or isolated-instance path |
| Doctor | Read-only check of identity/build, process/port ownership, readiness and auth; run before the first drive and after a surprising result |
| Drive | Real user path using stable accessible selectors, commands or public interfaces; no internal state setters or test-only shortcuts |
| Evidence | Action, expected observable result, actual result and side effects; evidence directory outside disposable run state |
| Cleanup | Exact owned process/session identifiers and scratch paths; stop only what the run started; preserve shared services, user data and evidence |
| Helpers | Invocation through the helper's interpreter, dependencies and exit-status meaning; make directly invoked helpers executable |

A long-running service may use one instance and serial drives. A short-lived CLI gets a fresh isolated process/session per journey. Record which model applies. Never use process-name-wide kills. A PID alone can be reused: verify its recorded command/start identity before stopping it. For a reused instance, cleanup removes only state created by the verification run.

For a dry-run/test mode, verify what actually changed in files, network or refs; do not infer safety from the option name. For external effects, use the existing production boundary's sandbox/test facility and state what remains unverified.

Done when: another agent can launch, diagnose, drive, observe and clean up from the written instructions without guessing a command, selector or ownership boundary.

### 3. Seed the feature map

Read [references/feature-map.md](references/feature-map.md). Create `features/README.md` and a feature file for each of the first three to five important user journeys, or all journeys if fewer exist. Derive them from actual routes, commands, menus or public interfaces. The index explicitly lists known uncovered features; a small seed map is not full product coverage.

Done when: each indexed feature has a real entry point, prerequisites, observable assertions and a stable file; the index names uncovered scope.

### 4. Execute the written recipe

Follow the generated instructions without substituting remembered setup steps: launch or reuse, doctor, drive one mapped feature, capture evidence, cleanup, then confirm the evidence remains readable. Clean owned residue after failed attempts too. Correct harness errors and repeat the same journey. If only a stand-in was available, list every extra setup step and difference from the real target.

Done when: one full journey passed using the generated recipe and its evidence survived cleanup, or the harness is explicitly `draft` with the failed step and prerequisite. Do not call a never-executed harness ready.

Report the canonical path, exercised feature, evidence location, uncovered scope and `ready` or `draft`. Point to the Maintain branch for subsequent refreshes; do not invent a recurring schedule.

## Maintain

Maintenance edits only the canonical harness directory: its skill, feature files and owned helpers. An app regression is a finding for `debug`; changing the product or weakening a correct expected result to get a green harness is outside this branch.

1. **Inventory.** Read the feature index and all sibling feature files. Reconcile missing, duplicate and dead entries. Look through recent source changes for real user-facing features absent from the map. If no harness exists, use Create. Done when: the index matches the files and missing product scope is explicit.
2. **Trace source.** For every mapped feature, identify current entry points, behavior and one live verification recipe. Read-only feature readers may help when available; otherwise trace serially. Keep actual driving with one coordinator to avoid competing for the same app state. Done when: every feature has source coverage and a recipe, with likely drift cited.
3. **Drive live.** Run Doctor, then exercise every mapped feature using its launch model. Doctor again after failures; if the process is healthy but UI state is wedged, reset owned state or relaunch an owned instance before continuing. Preserve evidence after every cleanup. Done when: each feature has a live result, not merely a source inspection.
4. **Classify and repair.** Fix doc drift or a harness gap inside the canonical directory, then re-drive every affected journey. Record product regressions without editing product code. Use `verified-unreachable` only when the prerequisite and attempted route are evidenced; unknown access or an unattempted journey is `unverified`. Neither status is a passing journey. Done when: every correction has a live recheck and every incomplete journey has its concrete reason.
5. **Finish.** Tear down remaining owned instances and verify retained evidence. Report `clean` (all mapped journeys pass, no edits), `changed` (proven harness corrections, all mapped journeys pass), or `blocked` (any failed/unverified/unreachable journey), alongside source/live coverage and uncovered product scope. Use `ship` only if requested. Done when: no owned process or disposable state outlives the run, and every mapped feature's result is accounted for.
