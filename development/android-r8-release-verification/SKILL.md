---
name: android-r8-release-verification
description: "Verify a minified Android release build (R8 + resource shrinking) when no device is attached — dex probing for stripped serializers, the ktor/supabase ServiceLoader engine trap that only breaks in release, proving a release-credential gate actually fires, and the androidTest-never-compiled blind spot. Use after enabling minification, before claiming a release build works, or when a cloud/serialization feature works in debug but is suspected in release."
---

# Verifying a minified Android release without a device

`assembleRelease` exiting 0 proves almost nothing. R8 failures are runtime
failures, and the debug build can never reveal them. These checks all run with
no device attached.

## 1. The ServiceLoader engine trap (highest value)

Libraries that resolve an implementation via `ServiceLoader` break under R8
because the `META-INF/services/*` entries get renamed. Symptom: works in every
debug build, the whole feature dies in release.

Check what the APK actually contains:

```bash
python - <<'PY'
import zipfile
z = zipfile.ZipFile("app/build/outputs/apk/release/app-release-unsigned.apk")
print([n for n in z.namelist() if "META-INF/services" in n])
PY
```

Renamed entries (`META-INF/services/ad0`, `an1`, …) mean discovery is in play.

**Fix by removing the discovery, not by adding keep rules.** For supabase-kt,
the ktor engine is discovered unless named explicitly:

```kotlin
createSupabaseClient(url, key) {
    install(Auth); install(Postgrest)
    httpEngine = OkHttp.create()   // compile-time reference; R8 cannot lose it
}
```

The engine artifact (`io.ktor:ktor-client-okhttp`) is usually already a
dependency — check before adding one.

## 2. Dex probing: did R8 strip what the app needs?

Concatenate the dex files and grep for names that MUST survive:

```bash
python - <<'PY'
import zipfile
z = zipfile.ZipFile("app/build/outputs/apk/release/app-release-unsigned.apk")
dex = b"".join(z.read(n) for n in z.namelist() if n.endswith(".dex"))
for p in [b"$$serializer", b"YourDto", b"okhttp3", b"OkHttpEngine", b"YourDatabase_Impl"]:
    print(p.decode(), "KEPT" if p in dex else "MISSING", dex.count(p))
PY
```

Interpretation matters:
- `@Serializable` DTOs and `$$serializer` classes **must** appear — kotlinx
  keep rules preserve those names. Absent = decoding will fail at runtime.
- A **missing ordinary class name is not evidence of removal** — R8 renames
  everything not covered by a keep rule. Only conclude "stripped" for names
  that a keep rule was supposed to preserve.

## 3. Keep rules: source them, don't invent them

Most libraries ship consumer rules inside the artifact; read them instead of
guessing:

```bash
unzip -p ~/.gradle/**/kotlinx-serialization-core-jvm-*.jar 'META-INF/proguard/*'
unzip -p ~/.gradle/**/ktor-utils-jvm-*.jar 'META-INF/proguard/*'
```

If a library ships none (supabase-kt does not), it usually relies on another
library's rules — scope your own rule to your package rather than writing
`-keep class ** { *; }`, which silently disables shrinking.

## 4. Prove the release credential gate fires

A release that ships blank backend keys "works" and is dead at runtime. If you
add a fail-fast gate, test the **negative** case, reversibly:

```bash
cp local.properties /tmp/lp.bak
# blank the keys, then:
./gradlew :app:assembleRelease   # expect failure with your message
cp /tmp/lp.bak local.properties  # restore, then verify the keys are back
```

Always verify restoration — a missed restore silently breaks later builds.

## 5. The androidTest blind spot

`assembleDebug` does **not** compile `src/androidTest`. Instrumented tests
written by anyone (including an agent) can be committed broken and unnoticed:

```bash
./gradlew :app:assembleDebugAndroidTest   # compiles + packages, no device needed
```

Also build the store artifact, which exercises a different path from the APK:
`./gradlew :app:bundleRelease`.

## 6. Lint triage via SARIF, not the HTML report

Run `./gradlew :app:lintRelease` (a flavoured app runs `:app:lint<Flavour>Release` and writes
`lint-results-<flavour>Release.sarif`) and triage the SARIF with the script in
`android-release-readiness-audit` section 2, never the HTML report.

Judgement calls worth keeping:
- `UnusedResources` on hand-made art is usually a **feature gap** (assets built,
  never wired), not dead weight. Wire it or report it; don't delete silently.
- `ModifierParameter` "should be the first optional parameter" is pure
  convention when all call sites use named arguments — low value, real churn.
- Lint objecting to a **documented, deliberate** non-plain `Modifier` default
  (e.g. a scroll container that must not receive infinite height) should be
  left alone; changing it alters layout at every call site.
- Fixing `DefaultLocale` with `Locale.getDefault()` **inside a `@Composable`**
  trades a warning for the `NonObservableLocale` *error*. Use Compose's
  observable locale instead, after confirming the API exists in the pinned
  artifact:
  `androidx.compose.ui.text.intl.Locale.current.platformLocale`.

## What still needs a device

Nothing above proves the app runs. After the checks pass, still require:
`connectedDebugAndroidTest`, and installing a debug-signed copy of the release
APK to exercise the network/serialization paths. Say so plainly rather than
implying the release is verified.
