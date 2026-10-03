---
name: android-security
description: Harden Android apps against the platform-specific failure modes. Covers Android Keystore and StrongBox, encrypted local storage, network security config and certificate pinning, WebView hardening, exported components and intent hijacking, backup rules, and Play Integrity with root detection as a signal. Invoke when shipping an Android app that holds credentials or tokens, before Play Store submission, or after a mobile security advisory.
---

# Android App Security

Android gives you app sandboxing, SELinux, and a hardware-backed Keystore for free. The work is around them: keys generated with the right constraints, storage that survives a lost device, components that are not accidentally exported to every other app on the phone, and WebViews that do not hand your session to arbitrary JavaScript.

This skill is for native (Kotlin / Java) Android apps. Flutter and React Native apps inherit the same platform surface — the manifest, Keystore, network security config, exported components, and backup rules all apply identically; only the code that calls them lives behind a plugin boundary.

## When to invoke

- Shipping an Android app that holds credentials, tokens, or sensitive data
- Before Play Store submission (where some checks are enforced; most are not)
- After a mobile-app security advisory affecting your stack
- Reviewing a third-party SDK before integration
- Investigating an in-the-wild abuse report on a mobile app

## Android Keystore — generate keys the OS will defend

Keystore keys are generated inside (and never leave) a hardware-backed environment on modern devices. Use it for the key that encrypts everything else — never hardcode or derive keys in app code.

```kotlin
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import javax.crypto.KeyGenerator

val spec = KeyGenParameterSpec.Builder(
    "vault_master_key",
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setKeySize(256)
    // Require the user to have authenticated recently to use this key:
    .setUserAuthenticationRequired(true)
    .setUserAuthenticationParameters(30, KeyProperties.AUTH_BIOMETRIC_STRONG or KeyProperties.AUTH_DEVICE_CREDENTIAL)
    // Invalidate the key if the user enrolls a new fingerprint/face:
    .setInvalidatedByBiometricEnrollment(true)
    // Prefer the dedicated secure element where available:
    .setIsStrongBoxBacked(true)
    .build()

val generator = KeyGenerator.getInstance(
    KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore"
)
generator.init(spec)
generator.generateKey()
```

The three constraints that matter:

- **`setUserAuthenticationRequired(true)`** — the key is unusable until the user authenticates. Without it, any code running as your app (including injected code on a compromised device) can use the key freely.
- **`setInvalidatedByBiometricEnrollment(true)`** — closes the "attacker enrolls their own fingerprint, then unlocks" hole. The key dies when biometric enrollment changes; handle `KeyPermanentlyInvalidatedException` by re-authenticating the user and re-provisioning.
- **`setIsStrongBoxBacked(true)`** — moves the key into a discrete secure element (Titan M class). Throws `StrongBoxUnavailableException` on devices without one — catch it and fall back to the TEE-backed Keystore, which is still good.

## Local storage — where each thing goes

| Storage | Encrypted? | Right for | Wrong for |
|---|---|---|---|
| Android Keystore | Hardware-backed | Keys only | Anything larger than a key |
| `EncryptedSharedPreferences` / Keystore-wrapped prefs | Yes (key in Keystore) | Tokens, small secrets | Large blobs |
| Plain `SharedPreferences` | No (filesystem crypto only) | UI state, feature flags | Tokens, PII, anything secret |
| Internal storage files | No (filesystem crypto only) | App data, caches | Secrets in plaintext |
| External / shared storage | No, world-influenced | Exports the user asked for | Everything else |

Filesystem-level encryption (file-based encryption on modern Android) protects against a powered-off stolen device, not against anything running on the unlocked device or extracted via backup/debug paths. Treat plain `SharedPreferences` as readable.

Note: the `androidx.security.crypto` library (`EncryptedSharedPreferences`) is deprecated, but the pattern is not — wrap your preference values with a Keystore-held AES-GCM key (as above), or use DataStore with Tink. What you must not do is store tokens in plain `SharedPreferences` because the helper library went unmaintained.

## Network security config — cleartext off, decide on pinning

Declare it once in the manifest and the platform enforces it for every stack that respects it (OkHttp, HttpsURLConnection, WebView):

```xml
<!-- AndroidManifest.xml -->
<application android:networkSecurityConfig="@xml/network_security_config" ...>
```

```xml
<!-- res/xml/network_security_config.xml -->
<network-security-config>
    <base-config cleartextTrafficPermitted="false" />
    <domain-config>
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set expiration="2027-01-01">
            <pin digest="SHA-256">REPLACE_ME_BASE64_SPKI_HASH=</pin>
            <pin digest="SHA-256">REPLACE_ME_BACKUP_PIN_HASH=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

`cleartextTrafficPermitted="false"` is the default since API 28 — set it explicitly anyway so a `usesCleartextTraffic` regression is visible in review.

Pinning tradeoffs are the same as on iOS: it stops MITM via rogue CAs and user-installed roots, but a cert rotation you didn't ship pins for bricks every installed version until users update. **Always ship a backup pin**, pin to the intermediate or a primary+backup SPKI pair rather than a single leaf, and set an `expiration` so a forgotten pin set fails open to normal CA validation instead of bricking the app. Pinning is high-leverage for banking, payments, and identity; lower-stakes apps reasonably skip it.

Native pinning does not cover Flutter's Dart HTTP stack or React Native's networking on all paths — verify where your framework's traffic actually flows before assuming the platform config applies.

## WebView hardening

A WebView is a browser with your app's identity. Default-deny everything and re-enable only what the specific screen needs:

```kotlin
webView.settings.apply {
    javaScriptEnabled = false          // enable only if the page needs it
    allowFileAccess = false            // file:// reads of app-private storage
    allowContentAccess = false
    domStorageEnabled = false
    // setAllowFileAccessFromFileURLs / setAllowUniversalAccessFromFileURLs
    // are false by default on modern APIs — never turn them on
}
```

`addJavascriptInterface` is the classic trap: every method on the bridge object is callable by **any page the WebView ever navigates to**, including a page reached via a redirect or an injected script on a compromised network. If you must expose a bridge:

- Annotate only intentional methods with `@JavascriptInterface` (mandatory since API 17, but audit what you annotated)
- Load only content you control, over HTTPS, and enforce it in `shouldOverrideUrlLoading` — external links go to Custom Tabs, not into your WebView
- Never pass tokens or secrets through the bridge or into URLs; the page is the untrusted side
- Prefer `WebViewCompat.addWebMessageListener` with an allowlisted origin over a raw interface object

## Exported components and intent hijacking

Every `activity`, `service`, `receiver`, and `provider` with an `intent-filter` is exported unless you say otherwise — and since API 31 you must say it explicitly:

```xml
<activity
    android:name=".DeepLinkActivity"
    android:exported="true">        <!-- exported only because it must receive links -->
    <intent-filter android:autoVerify="true">
        ...
    </intent-filter>
</activity>

<service android:name=".SyncService" android:exported="false" />
<provider android:name=".DataProvider" android:exported="false"
    android:grantUriPermissions="true" />
```

Rules of thumb:

- Default `android:exported="false"`; each `true` is a written-down decision with a reason
- Treat every extra arriving in an exported component as attacker input — validate before use, never pass it onward into privileged calls
- Content providers: keep unexported and use `grantUriPermissions` for per-URI, per-recipient access instead of opening the whole provider

`PendingIntent` mutability is the same trap in another shape. A mutable PendingIntent handed to another app (notification, widget, alarm) lets the receiver rewrite the wrapped intent — target, extras, everything — and fire it with **your** app's identity. Use `PendingIntent.FLAG_IMMUTABLE` (mandatory to choose explicitly since API 31) unless a specific API requires mutability, and if it does, fill in an explicit component so the target at least cannot be redirected.

## Backup rules — what leaves the device

`android:allowBackup="true"` (long the default) means app data — including any plaintext `SharedPreferences` — can leave the device via cloud backup or, on older APIs, `adb backup`. Either disable backup or scope it:

```xml
<application
    android:allowBackup="true"
    android:dataExtractionRules="@xml/data_extraction_rules"
    android:fullBackupContent="@xml/backup_rules" ...>
```

```xml
<!-- res/xml/data_extraction_rules.xml (API 31+) -->
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="sharedpref" path="auth_prefs.xml" />
    </cloud-backup>
    <device-transfer>
        <exclude domain="sharedpref" path="auth_prefs.xml" />
    </device-transfer>
</data-extraction-rules>
```

Keystore keys never leave the device, so anything encrypted under them is safe to back up but useless after restore — plan the re-authentication path for restored installs instead of shipping tokens in the backup to avoid it.

## Root detection and Play Integrity — signal, not defense

On-device root/tamper checks (su binaries, Magisk artifacts, debuggable flags, emulator heuristics) can always be bypassed by a determined adversary with Frida or a hiding module. Use them as **signal**: log the result, raise the server-side risk score, require step-up verification for sensitive operations. Do not treat the local check as a security boundary — sensitive logic stays server-side.

The **Play Integrity API** is the stronger version of the same signal: the device attests via Google Play, and your **backend** verifies the verdict (`MEETS_DEVICE_INTEGRITY`, `MEETS_STRONG_INTEGRITY`, app licensing, account details). Rules that keep it honest: verify the token server-side only, bind requests with a nonce you generated, treat a missing/failed verdict as elevated risk rather than a hard block (attestation fails for benign reasons too), and remember it tells you about the device, not about your own code's correctness.

## R8 / ProGuard — obfuscation is not security

Enable R8 in release builds: it shrinks the APK and makes casual reversing more tedious. That is all it does. Renamed classes decompile fine, string encryption is undone at runtime, and any secret in the APK — obfuscated or not — is extractable. No API key, signing secret, or business-critical logic gets protection from obfuscation; secrets belong on the server, and the app gets short-lived, scoped tokens. Keep `mapping.txt` per release so you can read your own crash reports.

## Deep links vs verified App Links

| | Custom scheme (`myapp://`) | App Link (`https://` + verification) |
|---|---|---|
| Who can claim it | Any installed app | Only the app proven to own the domain |
| Hijack risk | High — first/ambiguous claimant wins | Low once `autoVerify` passes |
| Use for | Nothing security-relevant | Auth callbacks, password reset, invites |

Verified App Links need `android:autoVerify="true"` on the intent filter plus an `assetlinks.json` on the domain listing your package name and signing-cert fingerprint. For OAuth, use App Links or Custom Tabs with PKCE — never a plain custom scheme, which any co-installed app can register to intercept the authorization code. Either way, link parameters are untrusted input: validate them, and never grant a session from a link parameter alone.

## Tapjacking / overlay basics

An app with overlay permission can draw on top of yours and trick the user into tapping your sensitive button through an invisible or disguised layer. For confirmation screens (payments, permission grants, destructive actions):

- Set `android:filterTouchesWhenObscured="true"` on the sensitive view, or check `FLAG_WINDOW_IS_OBSCURED` on the touch event and ignore obscured taps
- On API 31+, `setHideOverlayWindows(true)` removes non-system overlays from above your window entirely
- Mark secret-bearing screens with `FLAG_SECURE` to keep them out of screenshots, screen recording, and the recents thumbnail

## Third-party SDK review

Every SDK runs with the app's privileges and appears to the platform as you. Before adopting: what permissions does its manifest merge into yours (check the merged manifest, not the docs)? What does it phone home about? Does it initialize at startup via a `ContentProvider` you never see? Is it version-pinned or riding a `+` range? Has it had advisories? Same threat model as a backend dependency — see [`dependency-supply-chain`](../dependency-supply-chain/SKILL.md).

## Quick checklist

- [ ] Keys live in Android Keystore with `setUserAuthenticationRequired` and biometric-enrollment invalidation; StrongBox where available
- [ ] No tokens or PII in plain `SharedPreferences`; secrets encrypted under a Keystore key
- [ ] Network security config present, `cleartextTrafficPermitted="false"`, pinning decision documented (with backup pin and expiration if pinning)
- [ ] WebViews default-deny: JS and file access off unless required, no secrets across the JS bridge, external URLs escape to Custom Tabs
- [ ] Every component has explicit `android:exported`; each `true` justified; extras validated as untrusted input
- [ ] All `PendingIntent`s `FLAG_IMMUTABLE` unless a documented API requires otherwise
- [ ] Backup rules exclude secret-bearing files; restore path re-authenticates
- [ ] Play Integrity verdicts verified server-side with a nonce; root checks treated as risk signal only
- [ ] R8 enabled, but no secrets in the APK regardless (`apkanalyzer` / `strings` the release build)
- [ ] Security-relevant links are verified App Links; OAuth via Custom Tabs + PKCE
- [ ] Sensitive confirmation views reject obscured touches; secret screens use `FLAG_SECURE`
- [ ] Third-party SDKs reviewed via merged manifest and version-pinned
- [ ] Flutter / React Native: confirmed which layers the platform config actually covers

## What this skill will not do

- Help bypass Play Integrity, SafetyNet, root detection, or signature checks on apps or devices you do not own
- Recommend enabling cleartext traffic or trusting arbitrary certificates in production
- Provide tools or methods for tampering with, repackaging, or hijacking other apps' components or links
