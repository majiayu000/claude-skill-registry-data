---
name: mobile-ios-assessment
description: >
  Assess an iOS app (static + dynamic). Load when the target is an IPA / iOS app, an iOS bug-bounty
  scope, or "test the iOS app". Signals: .ipa, Info.plist, Swift/Obj-C, Keychain, URL schemes,
  ATS exceptions, Frida/objection on a jailbroken device.
domain: mobile
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: high
owasp: [M1:2024-Improper-Credential-Usage, M9:2024-Insecure-Data-Storage]
cwe: [CWE-919]
tools: [frida, objection, otool, class-dump, mobsf]
schema_version: 1
---

# iOS app assessment

## When it applies
You have an IPA (or an app on a jailbroken test device) and scope covers the iOS client + its
backend. As with Android, most impact is the backend reached through the app, plus local data /
keychain leaks and insecure IPC (URL schemes, universal links).

## Why it works
The app ships its logic and secrets, and trusts its own device. Decryption + class-dump reveal
endpoints and Obj-C/Swift classes; the Keychain and app container often hold tokens; and runtime
instrumentation removes jailbreak/pinning checks the server assumed held.

## Method
1. **Unpack & inspect**: decrypt the app (from a jailbroken device / `frida-ios-dump`), then
   `otool -L`, `class-dump`, and read `Info.plist` for URL schemes, `NSAppTransportSecurity` (ATS)
   exceptions, permissions, and background modes. MobSF for an automated static pass.
2. **Local storage**: inspect the app container — `NSUserDefaults`, plists, sqlite, cached files —
   and the **Keychain** for tokens/PII stored insecurely (`objection` → `ios keychain dump`).
3. **Dynamic**: `objection -g <bundle> explore` — bypass jailbreak detection and SSL pinning
   (→ `mobile-cert-pinning-bypass`), hook methods, then proxy and test the backend (BOLA/mass-assignment).
4. **IPC**: URL schemes / universal links (→ `mobile-deeplink-abuse`), pasteboard leakage, app extensions.

## Gotchas
- Non-jailbroken testing is limited — you usually need a jailbroken device or a re-signed app.
- ATS exceptions (`NSAllowsArbitraryLoads`) signal weakened TLS worth flagging.
- The high-impact bugs are usually server-side reached via the app — proxy and test the API.

## Verify success
Concrete impact: leaked working credential/endpoint, keychain/token exposure, unauthenticated IPC
reach, or a backend bug proven through the app's traffic.

## References
OWASP MASVS/MASTG (iOS); objection & frida-ios-dump; OWASP Mobile Top 10 (2024).
