---
name: ios-security
description: Harden iOS and macOS apps against the platform-specific failure modes. Covers Keychain accessibility tiers, App Transport Security, certificate pinning tradeoffs, file protection classes, biometric authentication, jailbreak detection as a signal rather than a defense, and third-party SDK review. Invoke when shipping a native app that holds credentials, before App Store submission, or after a mobile security advisory.
---

# iOS / macOS App Security

iOS gives you sandboxing, code signing, and Keychain for free. The work is around them: storing the right thing in the right place, validating remote connections, and resisting the runtime tampering that happens once an app is in the hands of someone willing to jailbreak.

This skill is for native (Swift / Objective-C / SwiftUI) iOS and macOS apps. Cross-platform frameworks (React Native, Flutter) share most of the principles but have their own specifics.

## When to invoke

- Shipping a native iOS / macOS app that holds credentials, tokens, or sensitive data
- Before App Store submission (where some checks are enforced; others are not)
- After a mobile-app security advisory affecting your stack
- Reviewing a third-party SDK before integration
- Investigating an in-the-wild abuse report on a mobile app

## Keychain — use it, but understand the tiers

Keychain is the right place for tokens, passwords, refresh tokens, and small secrets. It is not the right place for large data or files. Pick the right accessibility constant for each item.

```swift
import Security

let token = "..."
let data = token.data(using: .utf8)!

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrService as String: "com.example.MyApp",
    kSecAttrAccount as String: "auth_token",
    kSecValueData as String: data,
    // Choose the right accessibility:
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
]

SecItemDelete(query as CFDictionary)
let status = SecItemAdd(query as CFDictionary, nil)
```

Accessibility constants — pick the strictest that works for your flow:

| Constant | When the item is readable |
|---|---|
| `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` | Only while unlocked, never restored to another device. **Default for sensitive items.** |
| `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` | After first unlock since boot — useful for background tasks |
| `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` | Only if user has a device passcode set — strongest |
| `kSecAttrAccessibleWhenUnlocked` | Same as above but restorable to another device via backup — avoid for tokens |
| `kSecAttrAccessibleAlways` | Deprecated — do not use |

The `ThisDeviceOnly` suffix prevents the item from being restored to a different device via iCloud backup. For auth tokens, you usually want this.

## SecAccessControl — biometric or passcode gate per item

For high-value items, require the user to authenticate at access time:

```swift
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    [.biometryCurrentSet, .or, .devicePasscode],
    nil
)!

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrService as String: "com.example.MyApp",
    kSecAttrAccount as String: "vault_master_key",
    kSecValueData as String: secretData,
    kSecAttrAccessControl as String: access,
]
```

`.biometryCurrentSet` invalidates the item if the user adds/removes a biometric enrollment — closes the "attacker enrolls their own fingerprint, then unlocks" hole.

## App Transport Security (ATS)

ATS forces HTTPS with TLS 1.2+. Defaults are good — keep them. **Do not** add `NSAllowsArbitraryLoads = true` to `Info.plist`. Per-domain exceptions exist (`NSExceptionDomains`) but each is a written-down compromise; document why and review periodically.

For domains you control, ATS-compatible TLS is table stakes: TLS 1.2+, modern ciphers, valid cert. ATS will reject your own backend if you ship a misconfigured server (which is a feature).

## Certificate / public-key pinning

Pinning hardcodes the expected server cert or public key into the app. Without pinning, an attacker with a fraudulent (CA-issued or device-installed) cert can MITM the app. With pinning, the app rejects anything not matching the pin.

**Pros**: stops MITM via rogue CAs, stops corporate-proxy interception, stops user-installed root CAs.

**Cons**: if your server cert expires or rotates and you didn't ship an update first, every pinned app version is bricked until users update. Pin rotation is operationally painful.

Pinning is high-leverage for banking, payments, identity, and similar. Lower-stakes apps often don't pin and that's a reasonable choice.

```swift
// Sketch — URLSession delegate pinning to a public-key hash
func urlSession(_ session: URLSession,
                didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
          let serverTrust = challenge.protectionSpace.serverTrust else {
        completionHandler(.cancelAuthenticationChallenge, nil); return
    }

    // Pin to public-key SHA-256 of leaf or intermediate
    if isPinned(serverTrust) {
        completionHandler(.useCredential, URLCredential(trust: serverTrust))
    } else {
        completionHandler(.cancelAuthenticationChallenge, nil)
    }
}
```

**Pin to the intermediate or to a primary+backup leaf key**, not a single leaf. Ship multiple pins so cert rotation is graceful. Have a "kill pin" remote-config switch to disable pinning in an emergency (with logging).

## Data on disk — file protection

iOS encrypts disk at rest, but the encryption-key availability depends on the **Data Protection class** per file. For app-created files, set the class explicitly:

```swift
let url = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    .appendingPathComponent("sensitive.json")

let data: Data = ...
try data.write(to: url, options: [.atomic, .completeFileProtection])
// Equivalent to NSFileProtectionComplete — readable only when device is unlocked
```

Protection classes:

- `.complete` (`NSFileProtectionComplete`) — readable only while device is unlocked. Default for new files in most app templates.
- `.completeUnlessOpen` — file stays readable through a lock if open; otherwise like `.complete`
- `.completeUntilFirstUserAuthentication` — readable after first unlock since boot (good for background tasks)
- `.none` — readable as soon as the device boots — avoid for anything sensitive

Verify by inspecting on a device — there is no compile-time check that you set the right class.

## Jailbreak / tampering detection — and its limits

Jailbreak detection exists, but on a determined adversary's device it can always be bypassed (Frida, Liberty Lite, dynamic-library injection). Use it as **signal**, not as **defense**:

- Log the detection result with your telemetry (privacy-respectingly)
- Adjust risk score on the server (require extra verification for sensitive ops from jailbroken devices)
- Do NOT pretend the local check is a security boundary — sensitive logic stays server-side

Common heuristics (none individually conclusive):

- Existence of paths like `/Applications/Cydia.app`, `/private/var/lib/apt/`, `/usr/sbin/sshd`
- Ability to fork or write outside the sandbox
- Suspicious environment variables (`DYLD_INSERT_LIBRARIES`)
- Modified entitlements / unsigned binaries loaded
- Suspicious symbolic links

Combine 3+ checks and treat as a risk signal, not a binary verdict.

## URL schemes and Universal Links

Custom URL schemes (`myapp://`) are not authenticated — any app can claim them. **Use Universal Links** (`https://example.com/...` opens your app) for security-relevant deep links.

For OAuth callbacks specifically, Apple recommends `ASWebAuthenticationSession` over custom URL schemes. It runs in an ephemeral, isolated browser context and the result is delivered only to the requesting app.

## App Groups and shared containers

If you use App Groups to share data between your main app and extensions (Share, Widget, etc.), remember that **anything in the App Group is visible to every member of the group**. Don't share Keychain items more broadly than needed via `kSecAttrAccessGroup`.

Extensions also have their own attack surface — they receive content from arbitrary apps (Share extension), so validate inputs and don't trust the metadata.

## In-app purchases / receipts

Validate receipts server-side, not in the app. The local receipt format is well-known and forgeable on a jailbroken device. Apple provides the receipt validation endpoint specifically for backend use.

## OTA update integrity (for non-App-Store distributions)

For TestFlight / enterprise / Mac apps shipped outside the App Store:

- **Code-sign with a known certificate**, validate at first run
- **Sparkle** (macOS) update mechanism — use the EdDSA signing flow; HTTP-only feeds are deprecated, use HTTPS + signatures
- **Pin update server's TLS cert** if practical
- **No "auto-download and run" from arbitrary URLs**

App Store and TestFlight handle this for you; for everything else, you build it.

## Third-party SDK review

Every SDK you embed runs with the app's privileges. Before adopting:

- **What permissions does it access?** Camera, location, contacts, photos — each requires user consent and listing in `Info.plist`
- **What does it phone home about?** Analytics SDKs can leak surprising telemetry
- **How is it updated?** Version pin or accept whatever CocoaPods / SPM resolves
- **Has it had advisories?** Search the SDK + "vulnerability"
- **Does it use private APIs?** App Store rejection risk plus uncertain behavior across iOS versions

Same threat model as a backend dependency — see [`dependency-supply-chain`](../dependency-supply-chain/SKILL.md).

## Privacy disclosures (Info.plist + App Privacy)

iOS requires usage strings for each privacy-sensitive API. Wrong or missing strings cause rejections and confused users.

```xml
<key>NSCameraUsageDescription</key>
<string>This lets you scan QR codes for...</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>We use location to show nearby...</string>
```

Plus the App Store **Privacy "Nutrition Label"** must match what the app actually does. Lying here is App Store policy violation territory, plus a regulatory issue under GDPR if you serve EU users.

## Audit checklist before App Store submission

- [ ] Keychain items use `ThisDeviceOnly` accessibility constants
- [ ] Sensitive Keychain items use `SecAccessControl` with biometric/passcode gate
- [ ] No `NSAllowsArbitraryLoads`; per-domain ATS exceptions documented
- [ ] Cert/public-key pinning in place for sensitive flows (or documented decision not to)
- [ ] Files written with `.completeFileProtection` where appropriate
- [ ] No hardcoded API keys in the app bundle (search `strings YourApp.app/YourApp`)
- [ ] OAuth uses `ASWebAuthenticationSession`, not custom URL scheme handlers
- [ ] In-app purchase receipts validated server-side
- [ ] Universal Links used for security-relevant deep links
- [ ] Third-party SDKs reviewed and version-pinned
- [ ] Info.plist privacy strings present, accurate, and match Privacy Nutrition Label
- [ ] Debug symbols stripped from release builds
- [ ] App is signed with the correct provisioning profile (manual / automatic)

## What this skill will not do

- Help bypass iOS code-signing, jailbreak detection, or sandboxing on devices you do not own
- Recommend disabling ATS or trusting arbitrary certs in production
- Provide tools or methods for tampering with apps from the App Store
