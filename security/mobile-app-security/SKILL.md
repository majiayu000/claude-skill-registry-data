---
name: mobile-app-security
category: security
description: Use when reviewing iOS (Swift), Android (Kotlin) or Flutter changes - token storage, ATS and cleartext config, TLS trust, exported components, deep links, WebView JavaScript bridges, certificate pinning claims, secrets bundled in the app, Firebase rules
tech_stack: Mobile
source: original; cloudflare/security-audit-skill (MIT) deep-link handoff and device-lifecycle classes, adapted; informed by trailofbits/skills (CC BY-SA 4.0, ideas only, own wording); OWASP MASVS v2 and MASTG cited by name only; Android and Apple platform security documentation cited, not reproduced
---
# Mobile App Security (MASVS)

## Overview

The app binary is public and the device may belong to the attacker. Two consequences shape every mobile finding: anything shipped in the app is readable (a "hidden" server secret is leaked), and any check done only in the app can be skipped (the server is the boundary). What remains for the app is protecting **its user** from other apps, other networks and other web content.

**Core principle:** ask who the attacker is — another app on the device, someone on the network, a web page in a WebView, or the device owner. Findings against the device owner protecting their own data are usually not findings.

## 1. Secrets Shipped in the App (MASVS-CRYPTO, MASVS-CODE)

A server secret in `BuildConfig`, `Info.plist`, a bundled `.env`, `strings.xml`, Dart constants or an obfuscated string is a leaked secret — CRITICAL when live (secrets-and-crypto-review).

Not findings: Firebase `google-services.json` / `GoogleService-Info.plist`, Maps keys restricted by app signature, publishable payment keys. **But** the Firebase rules that protect the data are in scope:

```
// ❌ firestore.rules — every client reads and writes everything
match /{document=**} { allow read, write: if true; }
// ✅
match /users/{uid} { allow read, write: if request.auth != null && request.auth.uid == uid; }
```

## 2. Storage (MASVS-STORAGE)

| ❌ for tokens and credentials | ✅ |
|-------------------------------|----|
| Android `SharedPreferences`, plain files, SQLite, external storage | Keystore-backed encryption (Tink/AndroidX security), DataStore with an encrypted serializer |
| iOS `UserDefaults`, plist files, unencrypted Core Data | Keychain with an appropriate `kSecAttrAccessible…ThisDeviceOnly` class |
| Flutter `shared_preferences`, `Hive` unencrypted | `flutter_secure_storage` |

Severity follows the attacker: world-readable files (`MODE_WORLD_READABLE`, external storage) or data included in backups (`android:allowBackup="true"` without exclusions) → HIGH for credentials; private app storage on a non-rooted device → MEDIUM note. Tokens in `Log.d`/`print`/`NSLog` → readable by logcat tools and crash reporters → MEDIUM to HIGH.

## 3. Network (MASVS-NETWORK)

```xml
<!-- ❌ AndroidManifest / network_security_config: cleartext everywhere, user-installed CAs trusted in release -->
<application android:usesCleartextTraffic="true" …>
<base-config cleartextTrafficPermitted="true"><trust-anchors><certificates src="user"/></trust-anchors></base-config>
```

```xml
<!-- ❌ iOS Info.plist: ATS off for every domain -->
<key>NSAppTransportSecurity</key><dict><key>NSAllowsArbitraryLoads</key><true/></dict>
```

```dart
// ❌ Flutter: any certificate accepted
client.badCertificateCallback = (cert, host, port) => true;
```

Also: a custom `X509TrustManager` or `HostnameVerifier` that accepts all; `URLSession` delegate calling `completionHandler(.useCredential, URLCredential(trust:))` without evaluating the trust. A narrowly scoped exception for a local development host in a debug-only config is not a finding.

**Certificate pinning claims.** Missing pinning is hardening, not a finding. A diff that *claims* to add pinning gets checked: real SPKI hashes for the right hosts, a backup pin, not disabled in release builds, and — the real risk — no "pinning" implementation that replaces normal validation with a weaker check.

## 4. Exported Components and Intents (MASVS-PLATFORM, Android)

```xml
<!-- ❌ any app can start this and pass extras that drive a privileged action -->
<activity android:name=".AdminResetActivity" android:exported="true"/>
<!-- ✅ not exported, or protected by a signature-level permission -->
<activity android:name=".AdminResetActivity" android:exported="false"/>
```

- Activities, services, receivers and providers with `exported="true"` (or an intent filter) and no `android:permission`.
- **Intent redirection:** an exported component that takes an `Intent` from extras and calls `startActivity` on it — reaches the app's private components.
- `PendingIntent` with `FLAG_MUTABLE` wrapping an implicit intent → another app fills in the target.
- `ContentProvider.openFile` building a path from the URI (traversal), `grantUriPermissions` on broad paths.

## 5. Deep Links and URL Handlers (MASVS-PLATFORM)

Android `BROWSABLE` intent filters and App Links, iOS universal links and custom URL schemes (`application(_:open:options:)`, `onOpenURL`), Flutter `go_router`/`app_links` handlers: any web page can fire them. A finding when a link's parameters trigger a privileged action without confirmation (auto-login with a token from the link, changing account settings, initiating payments), or load an arbitrary URL into a privileged WebView.

**Handoffs through links.** Any app can register the same custom scheme, so an OAuth, SSO, magic-link or payment callback delivered over a custom scheme can reach the wrong app. The callback must carry the `state` this app stored for a flow it started, and the code must be useless without this app's PKCE verifier; verified App Links/universal links are the stronger channel. A callback accepted with no pending flow, or applied to whichever account is signed in now, is a finding.

## 6. WebViews and JavaScript Bridges

```kotlin
// ❌ an untrusted page gets a bridge into native code
webView.settings.javaScriptEnabled = true
webView.addJavascriptInterface(NativeBridge(tokenStore), "native")
webView.loadUrl(intent.getStringExtra("url")!!)
// ✅ bridge only for the app's own origin; external links open in the browser
if (Uri.parse(url).host == "app.example.com") webView.loadUrl(url) else openInBrowser(url)
```

- Android: `addJavascriptInterface` with remote content, `setAllowFileAccessFromFileURLs(true)`, `setAllowUniversalAccessFromFileURLs(true)`, `shouldOverrideUrlLoading` allowing `intent://` or `file://`.
- iOS `WKWebView`: a `WKScriptMessageHandler` that acts on messages without checking `message.frameInfo.securityOrigin`; `loadFileURL` with broad `allowingReadAccessTo`.
- Flutter `webview_flutter`: `JavaScriptChannel`s on pages loaded from a user-supplied URL.

## 7. Client-Side Authority (MASVS-AUTH)

- A role, entitlement, price or feature flag decided in the app and trusted by the server — check the server endpoint (access-control-and-idor).
- Biometric unlock implemented as a boolean set in `onAuthenticationSucceeded`/`evaluatePolicy` callback without a Keystore/Keychain key bound to it — bypassable on a compromised device; a MEDIUM note when it gates sensitive data.
- Dynamic code loading: `DexClassLoader` from external storage or downloaded files; JavaScript bundles or Dart code pushed over the air without signature verification.

## 8. Account Switch, Logout and Pending Actions

- Cached API responses, local databases, WebView cookies and storage, widgets or notifications that survive logout and show the previous account's data to the next one.
- A notification action, widget, shortcut or share extension that performs an action for an account other than the one displayed, or after the session that created it ended.
- A biometric or "confirm" prompt that approves one action while a different, queued action executes.

## Not Findings

Missing root/jailbreak detection, missing obfuscation, missing anti-tamper, screenshots in the app switcher, missing pinning, missing authorization checks in client code (judge the server).

## Common Mistakes

- Reporting a Firebase web/app config key as a leaked secret.
- Reporting `allowBackup` on an app that stores no credentials.
- Reporting an ATS exception for a single third-party domain that only serves public media.
- Reporting the device owner reading their own tokens on their own rooted phone.

## Red Flags

- `exported="true"` added to a component that performs account actions.
- `addJavascriptInterface`, `JavaScriptChannel` or a `WKScriptMessageHandler` next to a URL taken from an intent, a deep link or a server response.
- `NSAllowsArbitraryLoads`, `usesCleartextTraffic="true"`, `src="user"` outside debug configs.
- `badCertificateCallback`, trust-all managers, `allow read, write: if true`.
- An auth redirect URI on a custom scheme with no PKCE or no `state` comparison.
- A secret-looking constant in `BuildConfig` or `Info.plist`.

## References (names and links only)

[OWASP MASVS v2](https://mas.owasp.org/MASVS/) — MASVS-STORAGE, -CRYPTO, -AUTH, -NETWORK, -PLATFORM, -CODE · [OWASP MASTG](https://mas.owasp.org/MASTG/) · [Android app security best practices](https://developer.android.com/privacy-and-security/security-tips) · [Apple platform security](https://support.apple.com/guide/security/welcome/web)
