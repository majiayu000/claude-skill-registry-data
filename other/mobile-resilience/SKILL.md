---
name: mobile-resilience
description: >
  Detects weak reverse engineering and tampering protections in mobile apps (Android/iOS). Trigger on:
  root detection bypass, jailbreak detection bypass, Frida detection, debugger detection, anti-debugging,
  ptrace, sysctl, emulator detection, code obfuscation absent, debug symbols present, get-task-allow,
  ProGuard disabled, R8 disabled, string encryption, integrity check, file tampering, repackaging,
  dynamic instrumentation, runtime hook, Magisk hide, Magisk, frida-server, objection bypass,
  signing verification, apk resign. Covers MASVS-RESILIENCE-1/2/3/4.
license: MIT
compatibility: Designed for Claude Code. Frida, objection, apktool, jadx, Magisk, jadx, apk-mitm recommended.
metadata:
  category: mobile
  version: "0.1"
  source: https://mas.owasp.org/MASTG/
  source_types: framework
  masvs: MASVS-RESILIENCE-1, MASVS-RESILIENCE-2, MASVS-RESILIENCE-3, MASVS-RESILIENCE-4
---

# Mobile Resilience Against Reverse Engineering

## What Is Broken and Why

Resilience controls protect app logic, keys, and business rules from reverse engineering and tampering. Root/jailbreak detection, anti-debugging, and integrity checks create defense-in-depth. Without them, attackers can attach Frida to patch auth checks, repack APKs with modified logic, or extract keys from memory at leisure. Most basic resilience checks are bypassable individually — the value comes from layered controls that raise the cost of attack. Root detection that relies on a single file check (`/system/app/Superuser.apk`) is trivially bypassed; multi-vector detection that checks file system, build properties, and system call behavior is significantly harder.

## Key Signals

- `get-task-allow` entitlement present in iOS app (allows debugger attachment)
- Debug symbols not stripped in release build: `nm libapp.so | grep "T _"` shows function names
- Single-vector root/jailbreak detection: only checks for `/system/xbin/su` or Cydia URL scheme
- No anti-debugging: `ptrace(PT_DENY_ATTACH, 0, 0, 0)` / `sysctl` checks absent in iOS binary
- Debug build shipped to production: `BuildConfig.DEBUG == true`, `android:debuggable="true"`
- No signature/integrity check — APK can be repackaged and re-signed without detection
- Frida/objection successfully attaches without app detecting or exiting
- ProGuard/R8 not applied: decompiled class names match original Java package structure
- Emulator detection absent: app runs on AVD/Simulator with full functionality

## Methodology

**Android:**
1. Check `android:debuggable` in manifest — should be `false` in release build
2. Attach debugger: `adb shell jdwp | xargs` → connect Android Studio debugger → if attaches: no anti-debug
3. Run on emulator (AVD) — does the app detect and exit?
4. Root check bypass: run app on Magisk-rooted device, then apply MagiskHide/Shamiko — does app still detect root?
5. Frida attach: `frida -U -f TARGET_PKG` — if no crash/exit: no Frida detection
6. Repack test: `apktool b app/ -o repack.apk` → sign → install — does app accept repackaged build?
7. Check obfuscation: `jadx decompiled/` — are class/method names meaningful (no obfuscation) or mangled?

**iOS:**
1. Check `get-task-allow` entitlement: `codesign -d --entitlements :- App.ipa`
2. Attach lldb: `lldb -p TARGET_PID` — does app detect and exit?
3. Jailbreak detection: run on jailbroken device — does app behave normally?
4. Check for ptrace calls: `otool -tV App.app/App | grep ptrace`
5. Frida attach: `frida -U TARGET` — detection if app calls `proc_pidinfo` to scan for suspicious process names
6. Check debug symbols: `dsymutil -s App.app/App | head -50` — are symbols present in production?
7. Integrity check: modify a resource file in IPA → re-sign → install — does app detect modification?

## Payloads & Tools

```bash
# Android — check debuggable flag
apktool d app.apk && grep "debuggable" app/AndroidManifest.xml

# Android — Frida bypass root detection (generic)
frida -U -f TARGET_PKG --no-pause -l bypass-root-detection.js
# Common scripts: https://github.com/fridayy/frida-scripts

# Android — objection root bypass
objection --gadget TARGET_PKG explore
android root disable

# Android — check obfuscation
jadx app.apk -d jadx-out/
ls jadx-out/sources/  # readable package names = no obfuscation

# iOS — check entitlements
codesign -d --entitlements :- Payload/App.app/App | grep "get-task-allow"

# iOS — Frida jailbreak bypass
frida -U TARGET -l jailbreak-bypass.js
# Liberty Lite, Shadow (Cydia tweaks) for persistent bypass

# checksec — Android native binary
checksec --file=lib/arm64-v8a/libapp.so
```

```js
// Frida — Android: bypass single root check (file existence)
Java.perform(function() {
  var File = Java.use("java.io.File");
  File.exists.implementation = function() {
    var path = this.getAbsolutePath();
    if (path.indexOf("su") >= 0 || path.indexOf("magisk") >= 0) {
      console.log("[+] Blocked file check:", path);
      return false;
    }
    return this.exists();
  };
});
```

## Bypass Techniques

- **MagiskHide / Shamiko** — hides root from app's file system and build property checks
- **Frida gadget** — embed Frida gadget into APK instead of attaching server, bypasses process-name-based Frida detection
- **objection `android root disable`** — hooks common root detection libraries (RootBeer, SafetyNet check bypass)
- **SafetyNet bypass** — on rooted devices with MagiskHide + Universal SafetyNet Fix module
- **iOS Liberty Lite / Shadow** — jailbreak tweaks that hide jailbreak artifacts from app queries
- **Repackaging with modified entitlements** — add `get-task-allow` to enable debugging on non-jailbroken device
- **Anti-anti-debugging** — hook `ptrace` to return 0 always; hook `sysctl` to clear `P_TRACED` flag

## Exploitation Scenarios

**Scenario 1 — Frida Attach to Extract Business Logic**
Setup: Fintech app has no Frida detection. Logic for calculating fees is in native method `calculateFee()`. → Trigger: `frida -U TARGET -e "Module.findExportByName(null,'calculateFee')"` hooks the method. → Impact: Proprietary fee calculation logic extracted and replicated by competitor.

**Scenario 2 — APK Repackage to Remove Feature Flags**
Setup: App has premium feature gated by boolean check `if (user.isPremium)`. No integrity verification. → Trigger: Decompile APK, patch smali to always return `true`, repack and re-sign. → Impact: Free users access all premium features without payment.

**Scenario 3 — Debug Build in Production**
Setup: App shipped with `android:debuggable="true"` in release. → Trigger: Attacker runs `adb shell run-as TARGET_PKG` to access app's private data directory. → Impact: SQLite databases, SharedPreferences, and cached tokens extracted without root.

## False Positives

- App correctly detects Frida but exits gracefully (expected behavior) — confirm this is a resilience pass, not a bug
- `get-task-allow` present in development provisioning profile only — verify release build entitlements separately
- Debug symbols in debug build — only a finding in production/release builds
- Weak single-vector root check — technically bypassed but may be acceptable risk for non-high-value apps

## Fix Patterns

```kotlin
// Android — multi-vector root detection (raise attack cost)
fun isDeviceRooted(): Boolean {
    return checkSuBinary() || checkBuildTags() || checkDangerousApps() ||
           checkRWPaths() || checkSafetyNetAttestation()
}
// Use Play Integrity API for cryptographic device attestation (replaces SafetyNet)

// Android — prevent debugging in release
// In build.gradle: ensure debuggable is false
buildTypes { release { debuggable false } }
```

```swift
// iOS — ptrace anti-debug
import Darwin
func denyDebugger() {
    var name = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
    var info = kinfo_proc()
    var infoSize = MemoryLayout<kinfo_proc>.size
    sysctl(&name, 4, &info, &infoSize, nil, 0)
    if (info.kp_proc.p_flag & P_TRACED) != 0 { exit(1) }
}
```

- Layer multiple detection vectors — file checks, build props, system calls, app store attestation
- Use Play Integrity API (Android) / DeviceCheck + App Attest (iOS) for server-side verification
- Enable ProGuard/R8 with aggressive obfuscation rules for all release builds
- Strip debug symbols from production native libraries (`-s` linker flag)
- Implement runtime integrity checks: verify APK signature and file hashes match expected values

## Related Skills

[[mobile-auth-bypass]] via Frida hook is the most common exploit that resilience controls defend against — without debugger detection and Frida detection, biometric bypasses are trivially reproducible. [[mobile-insecure-storage]] extraction requires root or jailbreak access that resilience detection is designed to catch. [[mobile-code-quality]] binary hardening (PIE, stack canaries) complements resilience: hardened native code makes memory corruption exploitation harder even when the attacker has successfully bypassed root/jailbreak detection.
