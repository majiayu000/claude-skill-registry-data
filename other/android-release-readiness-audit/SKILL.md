---
name: android-release-readiness-audit
description: "Audit an Android/Compose app for production readiness with evidence instead of recall — release-build and signing checks, machine-readable lint triage via the SARIF report, and the four gaps that are almost always missing (Room migration tests, auto-backup privacy leak, crash reporting, silent blank BuildConfig secrets). Use when asked \"what's left before this ships / is it prod ready\", or before a first store release."
---

# Android release-readiness audit

Produce a prioritised, *evidence-backed* gap list. Never answer this question from
recall — every claim below has a one-line command that proves it.

Split the answer into two tiers, because they are different bars:
**Tier 1** = blockers for any real install (even self-hosted); **Tier 2** = blockers
for a public store release. Recommend Tier 1 first, and specifically the items that
can destroy user data.

## 1. Does a release artifact even exist

```bash
java -cp gradle/wrapper/gradle-wrapper.jar org.gradle.wrapper.GradleWrapperMain \
  :app:assembleRelease --console=plain 2>&1 | sed -n '/^e:/p;/FAILED/p;/BUILD/p'
ls -la app/build/outputs/apk/release/
```

`app-release-unsigned.apk` is the tell: **no signing config**. Confirm with
`grep -c "signingConfig" app/build.gradle.kts`. Creating a keystore is the user's
call — it is a credential they should own; flag it, do not generate one.

Note the APK size here. With `isMinifyEnabled = false` and no `proguardFiles`
(grep both), a Compose + Supabase/ktor app lands around 60–70 MB.

## 2. Lint, machine-readable

Do not eyeball the HTML report. Run `:app:lintRelease`, then parse the SARIF. A flavoured app
writes `lint-results-<flavour>Release.sarif` (Ironvellum: `lint-results-fossRelease.sarif`), and a
`lint-results-release.sarif` left from before the flavours still sits there reading as current
(verified 2026-09-24): point the script at the flavoured file.

```python
import json, pathlib, collections
d = json.loads(pathlib.Path("app/build/reports/lint-results-release.sarif").read_text(encoding="utf-8"))
run = d["runs"][0]
rules = {r["id"]: r for r in run["tool"]["driver"].get("rules", [])}
sev, by_rule = collections.Counter(), collections.Counter()
for res in run.get("results", []):
    rid = res.get("ruleId", "?")
    lvl = res.get("level") or rules.get(rid, {}).get("defaultConfiguration", {}).get("level", "warning")
    sev[lvl] += 1; by_rule[(lvl, rid)] += 1
print(dict(sev)); print(by_rule.most_common(15))
```

`IconLauncherShape` + `IconDuplicates` in quantity = placeholder launcher icon
copied across densities. `DefaultLocale` on formatted numbers matters if you ever
localise.

## 3. The four gaps that are almost always missing

**Room migration tests.** `ls app/src/androidTest` — frequently absent entirely.
Check `exportSchema` and whether `fallbackToDestructiveMigration` was removed:

```bash
grep -n "version = \|exportSchema\|fallbackToDestructiveMigration" app/src/main/kotlin/**/Database.kt
grep -c "MIGRATION_" app/src/main/kotlin/**/Database.kt
```

Hand-written migrations + no destructive fallback + no instrumentation tests means
one bad migration is a **crash on launch with no recovery**. This is usually the
single highest-risk item; say so plainly.

**Auto-backup vs the app's own privacy claim.** If the manifest has
`allowBackup="true"` and no `dataExtractionRules`/`fullBackupContent`, the local DB
is uploaded to Google. Grep the UI for privacy copy ("never leave this device",
"stays on your phone") — if any exists, the manifest contradicts it and that is a
real defect, not a nit.

**Crash reporting.** `grep -ciE "crashlytics|sentry|bugsnag" app/build.gradle.kts gradle/libs.versions.toml`
→ 0 means production is blind.

**Silently blank BuildConfig secrets.** Config read from a gitignored
`local.properties` with `getProperty(key, "")` ships a release with empty values
and the feature dead at runtime instead of failing the build. Verify the fallback
default and whether anything fails fast.

## 4. Store-only requirements (Tier 2)

- `targetSdk` must be a **stable** API level; verify against Play's current target
  API policy rather than assuming — a too-new value is rejected.
- Sensitive permission families (Health Connect `health.READ_*`, location,
  background) need a store data-safety declaration **and a hosted privacy policy
  URL**. An in-app rationale activity is necessary but not sufficient.
- OAuth consent screens left in **Testing** only admit listed test users.
- Hardcoded UI strings (only `app_name` in `strings.xml`) block localisation.

## 5. Also check, cheaply

```bash
grep -rn "TODO\|FIXME\|not implemented" app/src/main/kotlin --include=*.kt | head
ls app/src/test/**/ && ls app/src/androidTest 2>/dev/null
```

Tests that cover only `domain/` while `Repository`, DAOs and every screen are
untested is worth stating explicitly — it explains why UI regressions only ever
surface on-device.

## Reporting

Table per tier with a concrete `file:line` for every claim. Mark anything you could
not verify as `[INFERENCE]` with the check that would settle it. Close by naming the
2–3 data-destroying items to do first, and ask before anything requiring a
credential the user should own.
