---
name: mobile-android-assessment
description: >
  Assess an Android app (static + dynamic). Load when the target is an APK/AAB, a mobile
  bug-bounty scope, or "test the android app". Signals: .apk file, Java/Kotlin/Smali,
  AndroidManifest.xml, exported components, WebViews, hardcoded secrets, Frida/objection.
domain: mobile
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [M1:2024-Improper-Credential-Usage, M8:2024-Security-Misconfiguration]
cwe: [CWE-919]
tools: [jadx, apktool, frida, objection, mobsf, adb]
schema_version: 1
---

# Android app assessment

## When it applies
You have an APK (or a device/emulator running the app) and program scope covers the mobile
client + its backend. Most impactful mobile bugs are really API bugs the app exposes, plus
local data/secret leaks.

## Why it works
Client apps ship their logic and often their secrets. Decompilation reveals endpoints, keys,
and auth flows; exported components and WebViews expose attack surface; and the app trusts its
own device, so runtime instrumentation removes checks the server assumed were enforced.

## Method
1. **Unpack & triage**: `apktool d app.apk` (resources/manifest) and `jadx-gui app.apk`
   (readable Java). Read `AndroidManifest.xml` for `exported=true` activities/services/
   receivers/providers, `android:debuggable`, custom URL schemes, and `usesCleartextTraffic`.
2. **Hunt secrets & endpoints**: grep decompiled code + `res/` + `strings.xml` for API keys,
   base URLs, firebase configs, tokens (`grep -rniE "api[_-]?key|secret|https?://"`).
3. **Local storage review**: after use, pull `/data/data/<pkg>/` (shared_prefs, sqlite, files)
   for tokens/PII stored in cleartext.
4. **Dynamic**: run under Frida/objection — `objection -g <pkg> explore` to dump keystore,
   bypass root/emulator checks, and hook methods. Proxy traffic (Burp) to test the backend.
5. **Exported components**: invoke exported activities/providers via `adb shell am start`/
   `content query` to reach functionality without auth.

## Gotchas
- Cleartext-secret finding needs impact — a key with no privilege is informational; tie it to an action.
- Cert pinning blocks proxying → see `mobile-cert-pinning-bypass` before concluding "no traffic".
- The real bugs are usually server-side (BOLA/mass-assignment) reached via the app — proxy and test the API.

## Verify success
A concrete impact: leaked working credential/endpoint, unauthenticated reach into an exported
component, or a backend bug proven through the app's traffic.

## References
OWASP MASVS/MASTG; OWASP Mobile Top 10 (2024); jadx/objection docs.
