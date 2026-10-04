---
id: mobile-security
version: "2.0.0"
title: "Mobile Application Security"
description: "Android and iOS hardening on a device you do not control: hardware-backed credential storage, exported components and IPC, verified deep links, transport defaults and pinning rotation, server-side attestation over client-side root detection, screen capture, and release-build hygiene — including React Native and Flutter packaging. Use when generating Android or iOS app code, manifests, or native modules, wiring deep links or WebViews, or deciding what a mobile client is trusted to assert."
category: hardening
severity: high
applies_to:
  - "when generating Android (Kotlin / Java) app code or manifests"
  - "when generating iOS (Swift / Objective-C) app code or Info.plist entries"
  - "when generating React Native or Flutter app code and native modules"
  - "when wiring deep links, WebViews, or inter-app communication"
  - "when deciding what a mobile client may assert to a backend"
languages: ["kotlin", "java", "swift", "objc", "dart", "javascript", "typescript", "xml", "plist"]
token_budget:
  minimal: 1500
  compact: 1900
  full: 2400
rules_path: "checklists/"
related_skills: ["auth-security", "crypto-misuse", "secret-detection", "logging-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP MASVS v2.0"
  - "OWASP Mobile Application Security Testing Guide (MASTG)"
  - "Apple Platform Security Guide"
  - "Android Developers — App Security Best Practices"
  - "CWE-919, CWE-921, CWE-925, CWE-926"
---

# Mobile Application Security

## Rules (for AI agents)

### ALWAYS
- Start from the premise that **the device belongs to whoever is holding it**. The
  app runs on hardware an attacker can root or jailbreak, instrument at runtime, and
  read at rest. Everything shipped in the package is extractable, every client-side
  check is removable, and every local check can be made to return the answer the
  attacker wants. What you actually control is the backend's willingness to act — so
  any decision that matters is made server-side, on evidence the server verified.
- Issue short-lived, device-scoped tokens from a backend rather than shipping an API
  key, signing key, or backend credential in source, resources, `strings.xml`,
  `BuildConfig`, or `Info.plist`. Anyone can download the package and read it.
- Keep credentials in the platform's hardware-backed store: Android Keystore
  (`EncryptedSharedPreferences` with a `MasterKey`), iOS Keychain with a
  `…ThisDeviceOnly` accessibility class — `WhenUnlocked` where the value is never
  needed in the background, `AfterFirstUnlock` where it is. Never
  `SharedPreferences`, `UserDefaults`, a plist, or a file. The store protects a key
  at rest on an uncompromised device; it does not protect against code running inside
  your process, which is why the credential should be short-lived regardless.
- **Android**: give every `<activity>`, `<service>`, `<receiver>` and `<provider>` an
  explicit `android:exported`, defaulting to `false`. Since API 31 the attribute is
  mandatory when an intent filter is present — which forces the question to be asked,
  not answered. An exported component is a public API of your app that any installed
  application can call.
- Treat data crossing an app boundary as untrusted in both directions: validate every
  `Intent` extra and incoming activity payload, send sensitive data with an explicit
  component rather than an implicit intent any app can register for, and create every
  `PendingIntent` as `FLAG_IMMUTABLE` so the recipient cannot rewrite its contents.
- Verify deep links instead of trusting the scheme. A custom scheme (`myapp://`) can
  be claimed by any app that declares it; Android App Links (`android:autoVerify`)
  and iOS Universal Links are bound to a domain you control and are the only form
  carrying an ownership proof. Where the link carries an authentication callback,
  `auth-security` owns the `state` / PKCE check that makes it safe.
- Keep the platform's transport defaults: ATS enabled in `Info.plist`, an Android
  `networkSecurityConfig` that denies cleartext, and any exception scoped to a named
  host rather than the whole app. Where you add **certificate pinning** for a backend
  you own, plan its rotation at the same time — a backup pin for the next
  certificate, a tracked expiry, and a remote kill-switch. A pin that expires bricks
  every installed copy until users take a store update, which takes days.
- Decide sensitive actions on **server-verified attestation** — Play Integrity, App
  Attest, DeviceCheck — rather than a client-side root or jailbreak check. A check
  running on the attacker's device is removable in minutes; an attestation is worth
  something because your server evaluates it. Client-side detection is a speed bump
  worth having on high-risk apps and is never the decision.
- Bind biometric authentication to a cryptographic operation: a Keystore key created
  with `setUserAuthenticationRequired(true)` and used through `BiometricPrompt`, or a
  Keychain item guarded by `kSecAccessControlBiometryCurrentSet`. A boolean returned
  from a "did the user authenticate" API proves nothing — it can be patched to return
  true.
- Protect sensitive screens from capture: `FLAG_SECURE` on Android keeps a view out
  of screenshots and the recents thumbnail; on iOS, cover the window before the app
  is backgrounded, because the system snapshots the screen to render the app
  switcher.
- Strip debug material from release builds — verbose logging, `android:debuggable`,
  development endpoints, test credentials. Shrinking and minification (R8, ProGuard)
  are worth enabling for size and dead-code removal, but treat the renaming as a
  delay for a reverse engineer rather than a control. Nothing in the package is
  secret.
- Consult `logging-security` for what may be logged, with one mobile-specific twist:
  Logcat and oslog are readable from a connected device **without root**, so an HTTP
  logging interceptor left at body level in a release build publishes every request
  and its `Authorization` header to anyone with a cable.

### NEVER
- Ship an app that trusts any certificate: an empty `X509TrustManager`
  implementation, a `URLSessionDelegate` that accepts every challenge, or ATS
  disabled app-wide with `NSAllowsArbitraryLoads`. This is still the most common
  security defect shipped in mobile apps.
- Set `android:allowBackup="true"` on an app holding credentials — the backup is
  readable from a developer machine. Exclude sensitive paths explicitly.
- Load a user-controlled URL into `WebView` or `WKWebView` without scheme validation,
  or enable `setAllowFileAccessFromFileURLs` / `setUniversalAccessFromFileURLs`.
  `frontend-security` owns what executes inside that web view.
- Assume a cross-platform layer has handled any of this. A React Native JavaScript
  bundle sits readable inside the package, a Flutter AOT binary still contains its
  string literals, and plugin storage wrappers differ in whether they reach the
  hardware-backed store at all. The wrapper does not move the trust boundary.

### KNOWN FALSE POSITIVES
- Public identifiers embedded in the binary — an analytics key, a public DSN, a
  Firebase configuration — belong there. The question is whether the backend
  authorizes anything on them.
- `debuggable` on a debug variant is normal; the rule concerns release builds.
- A custom URL scheme for an OAuth callback is expected. The control is `state` or
  PKCE verification plus an App Link or Universal Link where the platform supports
  one — not the absence of the scheme.
- An app that deliberately runs on rooted devices (a developer tool, an emulator
  build) is not failing the attestation rule. That rule is about what the *server*
  decides, and the answer may legitimately be "allow".

## Context (for humans)

Mobile security has one property that reorganises everything else: the attacker owns
the execution environment. On a server you can reason about what an attacker can
reach; on a phone they can attach a debugger to your process, patch a function to
return `true`, dump the keychain on a jailbroken device, and read every string in the
binary. No amount of client-side hardening changes that, which is why obfuscation and
root detection are cost multipliers rather than controls.

The practical consequence is that mobile findings sort into two piles. The first is
"we shipped something we should not have" — a credential in the package, a
`trust-all` certificate handler, an exported component, a body-logging interceptor.
Those are real and fixable. The second is "we trusted the client to tell us the
truth", and the fix is never in the app: it is a backend that verifies an attestation,
issues a scoped short-lived token, and authorizes each request on its own.

Cross-platform stacks deserve their own suspicion. React Native and Flutter move the
code, not the boundary — the bundle and the AOT binary are both inside the package,
and a storage plugin may or may not reach the hardware-backed store depending on
platform and configuration. Check what the plugin actually does rather than what its
name suggests.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/platform-specifics.md` — manifest attributes and accessibility classes,
  pinning configuration per stack, App Link and Universal Link setup, screen-capture
  APIs, and what React Native and Flutter storage plugins actually use
- `checklists/android_manifest.yaml`
- `checklists/ios_keychain_ats.yaml`
- [OWASP MASVS v2.0](https://mas.owasp.org/MASVS/) · [MASTG](https://mas.owasp.org/MASTG/).
- [CWE-919](https://cwe.mitre.org/data/definitions/919.html) — Weaknesses in Mobile Applications.
