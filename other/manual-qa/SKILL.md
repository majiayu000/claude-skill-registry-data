---
name: manual-qa
description: Manual-QA pass over recent changes — files concrete bug reports (blocker/major/minor) for UI, navigation, and cross-feature regressions a tester would catch. Auto-detects the platform (Android, iOS, web) from the changed files and audits against that platform's bar; off-platform changes are judged against existing behavior. Builds and tests the branch first, then optionally drives a device or browser to confirm visual bugs. Read-only; output is a fix list, not a test plan. Triggers on "manual QA", "QA pass", "what's broken", "did this break anything", "find bugs in my diff".
user-invocable: true
argument-hint: "[android|ios|web|general] [staged|last|branch|<file>|<PR#>]"
allowed-tools: Read, Glob, Grep, Agent
---

# Manual QA

Simulate a manual tester reviewing a diff and **file the bugs they would file**. Catch UI edge cases, navigation mistakes, and cross-feature regressions that `/code-review` and unit tests miss. **Read-only** — produces a bug list with severities and fixes. Does not modify code.

This is the standalone version of `/regression`'s phase 2. It shares that skill's platform checklists rather than keeping its own — run `/regression` when you want the code pass too.

Output is a fix list, not a test plan. The user wants to know *what's broken* and *where to fix it*, in the form of a triage-ready bug report. This skill answers: *"if I shipped this right now, what would QA send back?"*

Not a replacement for `/code-review` (correctness/security/perf) or instrumented tests.

## Input

`$ARGUMENTS` may carry a platform token (`android` · `ios` · `web` · `general`), a scope token, or
both, in any order. Anything given explicitly wins — skip detection for it.

Scope (mirrors `/code-review`):

- empty or `staged` → `git diff --cached`
- `last` → `git diff HEAD~1`
- `branch` → `git diff main...HEAD`
- a file path → that file
- a PR number `N` → `git fetch origin pull/N/head:qa-pr-N`, then `git diff $(git merge-base HEAD qa-pr-N)..qa-pr-N`; delete `qa-pr-N` when done (GitHub remotes only)

If the diff is empty, stop and report — nothing to QA. If the working tree is in a half-merged or otherwise broken state, surface that and stop.

## Process

### 1. Map the change and detect the platform

From the diff, classify every touched file:

- **UI** — screen/view/component files, layouts, themes, string and asset resources.
- **Navigation** — route definitions, nav hosts/routers, deep links, guards, manifest entries.
- **Shared / cross-cutting** — design-system components, ViewModels/stores, repositories, use cases,
  theme tokens, `core/`, `common/`, anything used by multiple features.
- **New** — screens, components or routes the diff introduces.

Then detect the platform **from the files in scope**, not from what the repo happens to contain:

| Signal | Platform |
|---|---|
| `*.swift`, `*.xcodeproj`, `Package.swift`, `iosApp/`, `iosMain/` | iOS |
| `AndroidManifest.xml`, `androidMain/`, `build.gradle.kts` with `com.android.*` | Android |
| `package.json`, `*.tsx`/`*.jsx`/`*.vue`/`*.svelte`/`*.css`, `jsMain/`, `wasmJsMain/` | Web |
| `commonMain/` in a KMP module | **every target that module ships to** — audit once per platform |
| None of the above | **general** |

A UI signal only counts when the diff actually touches UI. A repository, a server route, or a
build file inside an Android repo is `general`.

Use the classified map internally to scope steps 2–4. Don't print it. If nothing in any UI / nav /
shared bucket changed, expect few or zero bugs — say so and stop.

### 2. Platform audit

**Read `../regression/references/<platform>.md` and audit against it.** Those files are the
checklist — this skill does not keep its own copy, so there is exactly one platform bar in the
config and both skills stay in step.

- `../regression/references/android.md` — Android/Compose bar; routes to `android-compose`,
  `material-3`, `edge-to-edge`, `navigation-3`.
- `../regression/references/ios.md` — Apple HIG bar, plus the Compose-Multiplatform-on-iOS tells.
- `../regression/references/web.md` — WCAG 2.2 AA, responsive, forms, routing, perf.
- `../regression/references/general.md` — no UI bar, so the bar is the behavior that already
  exists: map the contracts and call sites, then exercise it.

Each file carries a **required build & test step**, an **opt-in "exercise it" step**, a
**navigation audit** and a **UI/UX bar**. Run the required one first — a tester who reports on a
branch that doesn't compile has wasted the pass — then walk the sections the step-1 map says are in
play. Invoke the topic skills it routes to via the Skill tool when a judgement call is needed.

Reach for the opt-in step when a bug needs the app running to confirm: a layout that only breaks at
a large font scale, a back-stack bug, anything visual. **Take the screenshot and read it back** —
that's the tester's eye, and it's the half of this pass a diff can't give you.

**A project-scoped design skill outranks these files.** If the repo has its own `ui` / `ux` /
design-system skill (or a `web-ui`/`web-ux` tier), audit against that
first and use the reference file only for what it doesn't cover.

Multi-platform diffs get audited once per platform. "Correct on Android" is not "correct on iOS".

### 3. Integration / blast-radius pass

For each *shared* symbol changed (design-system component, ViewModel/store, repository function,
use case, string resource, theme token, API DTO, route):

- `Grep` the codebase for usages.
- At each call site ask: does the new shape, behavior, contract, text length, or timing break this
  caller's assumption? If yes → file a finding against the **call site**, not the changed symbol.
- For string and theme-token changes, list every screen that picks up the value and check whether
  the new length / color / shape still fits.

A bug at a call site is a real bug — file it under Findings, not as a "go look at this".

### 4. Triage and write the bug report

Group every finding by severity:

- **Blocker** — visible breakage on the primary path: clipped/missing UI, crash, broken navigation, wrong data shown, hardcoded color in dark mode, unreachable destination.
- **Major** — breaks on a realistic edge case: long localized string, font scale 1.3, RTL, dark mode on a secondary screen, error/empty state missing, back-stack lands in the wrong place.
- **Minor** — polish: missing `contentDescription`, off-by-a-few-dp touch target, inconsistent padding, non-mirrored icon.
- **Needs device verification** — only when the codebase genuinely can't decide (e.g., visual tightness on a 360dp phone, real network latency). Use sparingly — if you can name the file and line, it belongs in Blocker/Major/Minor instead.

Every finding cites `file:line`, names the actual symptom a user would see, and includes a one-line fix. No bare "check X". No padding.

Output inline using the format below. No file is written.

## Output Format

**Be laconic.** A long-read report doesn't get fixed. One line per bug, max two if cause genuinely needs explaining. No Repro/Actual/Cause/Fix sub-headers — fold them into the line. Skip empty severities.

```
## QA — {scope} · {X blocker · Y major · Z minor}

### 🔴 Blocker
- `EditProfileScreen.kt:88` — subtitle clips silently (no `maxLines`, parent height fixed at 120.dp). Add `maxLines = 2, overflow = Ellipsis`.
- `HomeTopBar.kt:42` — calls changed `ProfileHeader`; subtitle row pushes avatar off-screen. Pass `subtitleMaxLines = 1`.

### 🟠 Major
- `SettingsRow.kt:31` — `Color(0xFF222222)` divider invisible in dark mode. Use `colorScheme.outlineVariant`.
- `ProfileGraph.kt:57` — `popUpTo(Login)` should be `popUpTo(Profile)`; back press bounces user to Login.
- `EditProfileScreen.kt:140` — German label truncates in fixed Row. Use `weight(1f)`.

### 🟡 Minor
- `…:line` — symptom → fix.

### ❓ Needs device verification
- `ProfileCard.kt:24` — fixed 360.dp width on tablet landscape; eyeball centering.

Tests: `./gradlew assembleDebug test lint` — builds, 181 passed, lint clean.
Manual: Pixel 9a emulator, edit-profile flow at font_scale 1.3 — screencap confirms the clip above.
```

Format per bug: `` `file:line` `` — symptom, then fix. Symptom and fix together, one sentence each. No prose intro, no closing summary. If the diff is clean, one line: `No bugs found.` and stop.

## Rules

- **Output is a fix list.** Bugs grouped by severity, every one with `file:line`, what the user sees, and a one-line fix. No test plan, no checklist for the dev to execute.
- **Laconic.** One line per bug, two max. No Repro/Actual/Cause/Fix sub-bullets — fold into the line. No prose intro, no closing summary. A long report doesn't get fixed.
- **Read-only.** No edits to the source tree. Building, running the suite and driving the app are all read-only and expected — the fix line in each bug stays a snippet, not an applied change. Don't mutate the user's environment either: reset font scale and rotation, leave no seeded data, run no destructive `adb`/`simctl` command.
- **Real bugs only.** No padding. If you can't name the symptom a user would see, it's not a bug — drop it.
- **File against the actual breakage point.** A change to a shared symbol that breaks 4 call sites is up to 5 bugs (the symbol + each caller), not 1.
- **Specific over generic.** "Check overflow" is useless; `EditProfileScreen.kt:88 — subtitle has no maxLines, parent height fixed at 120.dp, second line clips` is a bug.
- **Defer, don't re-derive.** The platform bar lives in `../regression/references/<platform>.md`; the criteria behind it live in the topic skills that file routes to. Invoke them via the Skill tool when judgement is needed — never restate a checklist here.
- **Platform-correct, not platform-generic.** Judge iOS by the HIG, Android by Material, web by WCAG, everything else by the behavior that already exists — never by whichever one you looked at last.
- **`Needs device verification` is a last resort**, and it is not where you park things because you skipped the opt-in step. If you can name file and line, it's a bug. Use this bucket only when a device would settle a question you could not.
- **Say what you ran.** Close with a `Tests:` line always and a `Manual:` line whenever you exercised the app, each naming the command and its real result. Not run is `not run`, with the reason — an absent line reads as a pass you never earned.
- **Empty diff → stop.** Nothing to QA, say so.
- **Broken tree → stop.** Don't QA a half-merged or otherwise broken working tree.
- **Not /code-review.** This skill doesn't audit logic correctness, security, or performance — it complements `/code-review`, doesn't replace it.
