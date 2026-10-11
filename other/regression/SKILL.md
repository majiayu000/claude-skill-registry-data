---
name: regression
description: Post-feature verification gate — phase 1 reviews the code (bugs, pitfalls, code smells), phase 2 plays manual tester — it builds and runs the project's test suite on every platform, walks the blast radius, audits against the platform bar, and optionally drives an emulator, simulator or browser when a finding needs the thing running. Auto-detects the feature from git and the platform or area from the repo, so it works after a context compaction. Read-only report with a ship/fix verdict, then offers to fix. Triggers on "regression", "regression testing", "verify the feature we built", "did we break anything", "review and QA what we just shipped".
user-invocable: true
argument-hint: "[android|ios|web|general|all] [staged|last|last N|branch|<path>|<PR#>]"
allowed-tools: Read, Glob, Grep, Agent, AskUserQuestion
---

# Regression

Run this when a feature is **done** and you want to know whether it's safe to ship. Two phases, one report:

1. **Code** — bugs, pitfalls, code smells in what changed.
2. **Regression session** — build it, run its suite, then find what a manual tester would break and whether the result follows the platform's UI/UX bar. Off-platform work (backend, CLI, library, tooling, data) is judged against the behavior that already exists instead.

Built to be invoked **after a context compaction**: it reconstructs the feature from git, not from the conversation. It never assumes you still remember what was in the diff.

**Read-only until the last step.** The report ends with a verdict and an offer to apply fixes; nothing is edited before you say so. Building, testing and driving the app are part of the pass — none of them edit the source tree.

## Relationship to the other skills

| Want | Use |
|---|---|
| Just the code pass | `/code-review` |
| Just the tester pass | `/manual-qa` |
| Fix duplication / dead code / idioms | `/clean-up` |
| **The full post-feature gate** | **this skill** |

This skill *orchestrates* — it reuses `/code-review`'s correctness checklist and `/manual-qa`'s edge-case engine rather than re-deriving them, and adds the parts neither has: platform routing (iOS, web, and non-UI areas — not just Android), the blast-radius regression walk, and a single verdict. Don't run all three in sequence; run this one.

## 0. Detect scope and platform

`$ARGUMENTS` may carry a platform token (`android` · `ios` · `web` · `general` · `all`), a scope token, or both, in any order. **Anything given explicitly wins — skip detection for it.**

### Scope

If no scope token, detect with one Bash block:

```bash
git branch --show-current
git status --porcelain
git log --oneline -15
git diff --stat HEAD                      # uncommitted (staged + unstaged)
git diff --stat main...HEAD 2>/dev/null   # branch vs main
```

Pick in this order:

1. On a non-`main` branch with commits ahead of `main` → **branch diff** (`git diff main...HEAD`), plus uncommitted changes if any.
2. Uncommitted changes only → **working tree** (`git diff HEAD`).
3. Neither → **the feature's commits**: walk back from `HEAD` and take the run of commits that belong to the same feature (same scope prefix, same touched area, same session day). Stop at an unrelated commit or 10 commits, whichever comes first. If the run is ambiguous, take `HEAD~1..HEAD` and say so.

Explicit scope tokens mirror `/code-review`: `staged` · `last` · `last N` · `branch` · `<path>` · `<PR#>` (`git fetch origin pull/<N>/head:qa-pr-<N>`, then diff from the merge base; delete the branch when done).

### Platform / area

Detect from the **files in scope first**, repo root second — a repo can ship three platforms while the feature only touched one.

| Signal | Platform |
|---|---|
| `*.swift`, `*.xcodeproj`, `*.xcworkspace`, `Package.swift`, `iosApp/`, `iosMain/` | iOS |
| `AndroidManifest.xml`, `androidMain/`, `*/build.gradle.kts` with `com.android.*` | Android |
| `package.json`, `index.html`, `*.tsx`/`*.jsx`/`*.vue`/`*.svelte`/`*.css`, `wasmJsMain/`, `jsMain/` | Web |
| `commonMain/` in a KMP module | **every target that module ships to** |
| None of the above — server, CLI, library, Gradle/build logic, scripts, data, config, infra | **general** |

**A UI signal only counts when the diff actually touches UI.** A change to a repository, a server route, a `build.gradle.kts`, or a script inside an Android repo is `general`, not Android — route by what changed, not by what the repo happens to contain. A feature can be both (`general` for the API, `android` for the screen consuming it); audit each part under its own bar.

Shared code is a multiplier, not a single platform: a change in `commonMain` or in a shared design-system component gets audited once per platform it reaches, because the same code fails differently on each (back gesture, safe areas, font metrics, input model).

### Confirm before running

Print exactly this, then ask once:

```
Feature:  <one line, inferred from commits + diff>
Scope:    <branch main...HEAD · 14 files · 3 commits>
Platform: <Android + iOS (shared :client:notes + androidMain)>   # or: general (:server ktor routes)
```

Ask with `AskUserQuestion`: proceed, or correct the scope/platform. One round-trip, then run. Skip this step entirely when `$ARGUMENTS` gave both scope and platform.

**Stop and report instead of running** if: the diff is empty, the tree is half-merged/conflicted, or the branch has no relationship to `main`.

## Phase 1 — Code

Three buckets. Cite `file:line` for every finding.

### 1A. Bugs — does it work?

Run `/code-review`'s correctness, security, and performance checklist over the scope. Don't restate it here — invoke the built-in `code-review` skill and use its checklist. Findings come back into this report, not a separate one.

### 1B. Pitfalls — does it work the *second* time?

The traps a diff-reading review misses because they only show up on the second run, the slow network, or the unlucky lifecycle. Walk the ones that apply:

- **State survival** — config change, process death, backgrounding, tab restore. Is in-memory-only state reconstructed or silently lost? (`SavedStateHandle`, `@SceneStorage`/state restoration, URL/session storage.)
- **Lifecycle & cancellation** — work started in the wrong scope; a coroutine/Task/effect that outlives its screen; a subscription never torn down; cancellation swallowed as a generic error.
- **Concurrency & re-entrancy** — double-tap fires the action twice; a second request overtakes the first and writes a stale result; no idempotency on retry.
- **Persistence & migration** — schema/format changed without a migration; data written by the previous build no longer parses; cache keys unchanged after the shape changed.
- **Boundaries** — empty list, single item, huge list, null/absent optional field, expired token, denied permission, no network, slow network, server 500. Which of these paths has *never* been executed?
- **Feature interaction** — flags, entitlements, onboarding vs returning user, logged-out, offline-first sync conflict.
- **Platform pitfalls** — read the `Pitfalls` section of the matching `references/<platform>.md` (`general.md` when the area isn't a UI platform).

### 1C. Smells — will it be maintainable?

Detection only — this skill reports, `/clean-up` fixes. Defer every judgement to the topic skill, don't re-derive:

| Smell | Skill |
|---|---|
| Kotlin idioms, null handling, scope-function abuse | `kotlin` |
| Coroutines, Flow, dispatchers, structured concurrency | `kotlin-coroutines` |
| `expect`/`actual`, source-set placement, platform leakage | `kotlin-multiplatform` |
| Compose state, side-effects, stability, recomposition | `android-compose` |
| MVI state/effect shape, logic in the wrong layer | `android-mvi` |
| DI scoping and graph hygiene | `koin`, `android-hilt` |
| Module boundaries, dependency direction | `android-multimodule` |
| HTTP client config, auth, retry, timeouts | `ktor-client` |
| Duplication, dead code, reuse | `clean-up` (its *Reuse pass*) |

Cap this bucket: the three highest-impact smells in the scope. It is a gate, not a lint run.

## Phase 2 — Regression session

Phase 1 asks *is this code right*. Phase 2 asks **what does a tester break, and does it feel right on this platform**.

### 2A. Blast radius

For every symbol the diff changed that is used elsewhere — shared composable/view/component, ViewModel, repository function, use case, string/theme token, API DTO, route:

1. `Grep` for its call sites.
2. At each site ask: does the new shape, behavior, contract, text length, or timing break this caller's assumption?
3. If yes → **file a bug against the call site**, not against the changed symbol. One change that breaks four callers is five findings.

Then walk the **user-visible flows** the feature touches, end to end — entry point → happy path → back out → re-enter. Per flow check: does it survive backgrounding, does back/dismiss land where the user expects, does re-entry show fresh data, does the previous screen still reflect the change, and does the *unchanged* neighbouring feature still work.

### 2B. Platform audit / behavior regression

Read `references/<platform>.md` **for each detected platform or area** and audit against it. Those files are the checklist; this file doesn't repeat them.

Every one of them opens with a **required build & test step and an opt-in "exercise it" step**. Run the required one before auditing — a static pass cannot tell you whether the code compiles, and a pre-existing red test changes what counts as a regression. Reach for the opt-in one when a finding needs the thing running to confirm or refute it.

- `references/android.md` — `./gradlew assembleDebug test lint`; then optionally an emulator or attached device (screencap, font scale, deep links, process death). Routes to `android-compose`, `material-3`, `edge-to-edge`, `navigation-3`.
- `references/ios.md` — `./gradlew allTests` for the KMP half, `xcodebuild build/test`; then optionally a simulator, because the HIG findings there are mostly *feel* — swipe-back, scroll physics, safe areas — which a diff cannot show. Plus the Compose-Multiplatform-on-iOS tells that make an app feel non-native.
- `references/web.md` — `build`, `test`, `tsc --noEmit`, `lint`; then optionally a real browser via Playwright or `webapp-testing`. The web is the cheapest platform to drive, so the bar for skipping is higher here. WCAG 2.2 AA, responsive, forms, focus, perf.
- `references/general.md` — everything else. No UI bar to judge against, so the bar is the **existing behavior**: map what already exists (call sites, existing tests, contracts, docs), run the project's own build and test suite, then **exercise it manually** — CLI invocation, `curl` against a local server, a scratch call into the library, a clean + incremental build.

**Screenshots are read back, not just taken.** Contrast, truncation, overlap and layout breakage are visual defects; capturing an image and never opening it proves nothing.

If a required step can't run here (no toolchain, no simulator, a build that needs a secret), say so in the report and hand over the exact command with its expected result. Silence reads as "it passed".

**A project-scoped design skill outranks these files.** If the repo has its own `ui` / `ux` / design-system skill, audit against *that* and use the reference file only for what it doesn't cover.

Multi-platform features: the same screen gets audited once per platform. "Correct on Android" is not "correct on iOS" — a bottom sheet, a back affordance, and a font scale behave differently.

## Output

One report, inline, no file written. **Laconic — one line per finding, two only when the cause needs explaining.** No Repro/Actual/Fix sub-headers, no prose intro, no closing summary. Skip empty sections.

```
## Regression — <feature> · <platform(s)> · <scope> · 2🔴 4🟠 3🟡

### Phase 1 — Code
🔴 `SyncWorker.kt:74` — retry re-sends the same mutation; server has no idempotency key → duplicate notes. Pass the local ULID as `Idempotency-Key`.
🟠 `NoteRepository.kt:120` — `catch (e: Exception)` swallows `CancellationException`; screen exit logs a fake error. Rethrow it.
🟡 `NoteEditorViewModel.kt:41` — three copies of the same block-mapping loop. Extract or use the existing `Block.toUi()`.

### Phase 2 — Regression
🔴 `HomeScreen.kt:88` — calls the changed `NoteCard(subtitle=)`; two-line subtitle pushes the timestamp out of the fixed 96.dp row. Pass `maxLines = 1`.
🟠 `EditorGraph.kt:57` — `popUpTo(Home)` drops the editor from the back stack; back from Share exits the app.

### Phase 2 — UX · iOS
🟠 `EditorScreen.kt:210` — full-screen editor blocks the interactive swipe-back gesture with no visible back affordance. (HIG: navigation)
🟡 `Toolbar.kt:33` — 36pt icon buttons; iOS minimum is 44pt.

Tests: `./gradlew :client:assembleDebug test` — builds, 181 passed 1 failed (`NoteSyncTest.retryIsIdempotent`); `allTests` iOS target not run, no simulator here.
Manual: Pixel 9a emulator — editor → share → back exits the app (confirms `EditorGraph.kt:57`); screencap at font_scale 1.3 shows the timestamp clipped.

### Verdict
**Fix first** — 2 blockers. Everything else is shippable.
```

Rules for the report:
- Every finding: `` `file:line` `` — the symptom a **user or maintainer actually experiences** — then the fix, one sentence.
- Deduplicate across phases. One root cause = one finding, filed in the phase that catches it first.
- **Every area** ends Phase 2 with a `Tests:` line, and a `Manual:` line whenever you exercised the thing. State the command and its actual result. Nothing executed needs a reason — "not run: no simulator on this machine" is an acceptable line, an absent line is not.
- Verdict is `Ship it` (no blockers), `Fix first — N blockers`, or `Needs a device — <what to check>` when only real hardware (or an environment you don't have) can decide.
- `Needs a device` is a last resort, and it is **not** the verdict for merely having skipped the opt-in step. If you can name the file and line, it's a finding. Reserve it for a question a device would settle that you could not.

## Fix offer

After the report, ask once with `AskUserQuestion`: fix the blockers, fix blockers + majors, fix everything, or nothing. Then apply only what was chosen, run the project's build/tests if a runner exists, and report pass/fail. Findings whose fix isn't behavior-preserving stay unapplied — list them as *proposed* and say why.

## Rules

- **Read-only until the fix offer.** No edits during either phase.
- **Real findings only.** No padding, no "consider reviewing X". If you can't name the symptom, drop it.
- **`file:line` or it doesn't ship.** A finding without a location is a note, and notes don't belong in this report.
- **Defer, don't re-derive.** Invoke `code-review`, `manual-qa`, and the topic skills via the Skill tool. This file owns the *process*; they own the *criteria*.
- **File against the breakage point**, not the change that caused it.
- **Platform-correct, not platform-generic.** Judge iOS by the HIG, Android by Material, web by WCAG, everything else by the behavior that already exists — never by whichever one you looked at last.
- **Reading the diff is half the job — on every platform.** Build it, run its suite, run its linter, whatever the area. Then exercise it when a finding needs the thing running to settle. Running tests edits nothing, so this does not violate read-only.
- **Never report a suite as passing that you didn't run.** Not run is `not run`. This is the one rule with no judgement in it.
- **Exercising is read-only too.** Drive the app, don't mutate the user's environment: no destructive `adb`/`simctl` command, no erased simulator, no seeded data left behind. Reset font scale, rotation and dev servers when you're done.
- **Empty or broken scope → stop** and say so.
- **The verdict is the point.** The user asked one question: can I ship this?
