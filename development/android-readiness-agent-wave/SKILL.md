---
name: android-readiness-agent-wave
description: "Use when asked to make an Android app prod ready by fixing a whole readiness audit at once with parallel agents: R8 + signing, Room migration tests, auto-backup privacy leak, crash journal, monotonic cloud sync, launcher icons, policy docs, manual-only CI."
---

# Android readiness agent wave

Companion to `android-release-readiness-audit` (which *finds* the gaps). This is
how to **close them all concurrently**, plus the defects that show up every time.
Wave mechanics (briefs, build rule, acceptance) are `fixer-wave-orchestration`;
this skill adds the Android slice plan.

## 1. Slice by exclusive file ownership

One agent per slice; no two agents may touch the same file. Paths are Ironvellum's
(`D:/Monarch`, package `com.ironvellum.app`); map them onto the target app.

| Slice | Owns | Slice skill |
|---|---|---|
| BuildRelease | `app/build.gradle.kts`, `gradle/libs.versions.toml`, `app/proguard-rules.pro` | `android-r8-release-verification` |
| MigrationTests | `data/IronvellumDatabase.kt` (the `@Database` class), `app/src/androidTest/**`, new `app/src/test/**/data/**` | `room-migration-data-survival-test`, `kotlin-test-file-overwrite-guard` |
| BackupPrivacy | `AndroidManifest.xml`, `res/xml/**` | `android-backup-exclusion-verify` |
| CrashJournal | new `data/CrashJournal.kt`, `IronvellumApp.kt`, `ui/settings/SettingsScreen.kt` | `android-crash-journal-and-periodic-work-verify` |
| SyncGuard | `data/cloud/CloudSync.kt`, `data/cloud/Dtos.kt` | |
| LauncherIcon | `res/mipmap-*/**` only | `android-adaptive-icon-from-generated-art` |
| PolicyDocs | `PRIVACY.md`, `docs/**`, `README.md` | `play-data-safety-code-audit` |
| CI | `.github/workflows/**`, `workflow_dispatch` triggers only (never push/PR/schedule) | `github-actions-cost-shutdown` |
| SdkScout | read-only research (`scout` agent) | |

Brief every slice per `fixer-wave-orchestration`: Gradle agents run no gradle, lint
or adb, and the parent validates once. Write these cross-slice contracts into the
shared context before dispatch; they always bite:

- The gradle owner must add the androidTest deps, `testInstrumentationRunner`,
  the `room.schemaLocation` KSP arg **and**
  `sourceSets.getByName("androidTest").assets.srcDir("$projectDir/schemas")` —
  without that last line `MigrationTestHelper` fails with "Cannot find schema file".
- The `@Database` owner turns on `exportSchema`, not the gradle owner.
- BuildRelease wires signing to credentials the owner supplies. **Never create the
  release keystore**; generating their signing key is not yours to do.

## 2. Parent work while they run

Take anything touching files nobody owns — typically the lint warning cleanup,
which spans many files and would collide with everyone.

## 3. Integration gate — assume damage

Run the `subagent-damage-repair` probes on every changed `.kt`, import diff first
(dropped imports are the #1 agent failure mode). Then eyeball non-import deletions
for deleted functions/loops:

```bash
git diff -U0 -- "*.kt" | grep "^-" | grep -v "^---" | grep -v "^-import "
```

CRLF: D:/Monarch checks out CRLF (`core.autocrlf=true`); `git show HEAD:` emits LF.
git-bash `grep`/`sed`/`awk` strip the CR, so the probes work as written. ripgrep and
the built-in Grep tool keep it: `$`-anchored patterns miss, and a ripgrep-fed import
diff lists all 83 imports of an unchanged `Repository.kt` as dropped (verified
2026-09-24). Add `tr -d '\r'` around them — a "missing import" the compiler clearly
resolves is the tool, not the file.

## 4. Defects this wave produces (seen every run)

- **Gradle name shadowing**: `val keyAlias = ...` then `create("release") { keyAlias = keyAlias }`
  → `'val' cannot be reassigned`. Rename locals to `keyAliasValue`.
- **Nullable field into non-null param**: `@Volatile var dir: File?` passed to
  `record(dir: File, …)`. Capture a local non-null first.
- **Early-return guards that disable the feature**: e.g.
  `Thread.getDefaultUncaughtExceptionHandler() ?: return` inside `install()` skips
  recording entirely. Install unconditionally, delegate with `previous?.…`.

## 5. Verification order (each gates the next)

Ironvellum's tasks are flavoured; `python tools/gate.py --no-device --backend`
covers steps 1 and 4.

1. `:app:assembleFossDebug :app:testFossDebugUnitTest`
2. `:app:assembleFossRelease` — R8 is the risky change; note the size drop, then
   run the no-device checks in `android-r8-release-verification`.
3. **Negative-test the fail-fast** (reversible procedure: `android-r8-release-verification`).
   Ironvellum's gate is `validateFossReleaseBackend`/`validatePlayReleaseBackend`
   (`supabase.url`, `supabase.key`; play adds `google.webClientId`). Signing is
   deliberately not fail-fast: no credentials, unsigned APK. Blank a key by setting
   it empty in `local.properties` (a deleted key is refilled from the committed
   `cloud-defaults.properties`); `IRONVELLUM_*` env vars beat the file for signing.
4. `:app:lintFossRelease` → triage `app/build/reports/lint-results-fossRelease.sarif`
   with the SARIF script in `android-release-readiness-audit`, not the HTML.
5. Device, **emulator only** (the instrumented suite runs `pm clear`, deletes rows
   and uninstalls, destroying the S25's real training history):
   `python tools/gate.py --serial emulator-5554`, or `:app:connectedFossDebugAndroidTest`
   with `ANDROID_SERIAL=emulator-5554`. Then install a **debug-signed copy of the
   release APK** to smoke R8 at runtime (serialization/ktor break here, not at compile).

## 6. Judgement calls worth repeating

- **Don't blanket-fix lint.** The `UnusedResources`, `ModifierParameter` and
  `NonObservableLocale` calls are in `android-r8-release-verification`;
  non-composable helpers may keep `Locale.getDefault()`.
- **Refuse i18n extraction** unless a second locale is actually needed — hundreds
  of strings, high breakage, no user-visible benefit.
