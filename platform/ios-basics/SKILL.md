---
name: ios-basics
description: Use when you need to assess an iOS application you are
  authorized to test, such as a client iPhone app on a penetration test or a
  CTF challenge IPA. Covers IPA acquisition and triage, Info.plist and
  entitlement review, binary inspection, Keychain and local storage checks,
  App Transport Security analysis, URL scheme attack surface, and runtime
  instrumentation with Frida 16.x and objection 1.11.0 on a jailbroken test
  device. Use when the engagement scope includes iOS, or when you must
  compare Android and iOS builds of the same app for platform-specific flaws.
version: 1.0.0
domain: mobile
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [android-static, android-dynamic]
tools:
  - name: Frida
    version: 16.5
  - name: objection
    version: 1.11
  - name: Python
    version: "3.12"
  - name: Xcode
    version: 16.x
---

iOS app assessment combines static review of the IPA bundle with runtime
instrumentation on a jailbroken test device. The platform gives you strong
defaults (sandboxing, Keychain, App Transport Security), so iOS findings
usually come from app-level mistakes: insecure storage, broken transport
security exceptions, exposed URL schemes, and missing jailbreak or tamper
detection. This skill covers the authorized workflow from IPA triage
through Info.plist review, binary inspection, storage checks, and Frida
runtime analysis. All testing targets apps you have written permission to
test, on devices you own or are assigned for the engagement.

## Quick Workflow

1. Obtain the IPA through an authorized channel (client build, TestFlight
   build in scope, or CTF file) and record its hash.
2. Unzip the IPA and triage the bundle: Info.plist, embedded frameworks,
   and the main binary.
3. Review Info.plist for URL schemes, ATS exceptions, and privacy
   permission usage.
4. Inspect the Mach-O binary: encryption check, PIE, stack canaries, and
   ARC.
5. Review entitlements and the provisioning profile for excessive
   capabilities.
6. Check local storage: Keychain usage, files in the sandbox, and pasteboard
   or screenshot leaks.
7. On a jailbroken test device, run objection and Frida for runtime
   inspection: Keychain dump, method hooks, and pinning bypass.
8. Record every finding with bundle path and reproduction steps.

## 1. IPA acquisition and triage

An IPA is a zip file. Unzip it and inventory the contents before any deep
review.

```bash
# Record integrity first
sha256sum target.ipa
file target.ipa

# Unzip the bundle
unzip -q target.ipa -d ipa-out
ls ipa-out/Payload/

# Identify the main app bundle and binary
ls ipa-out/Payload/*.app/
plutil -p ipa-out/Payload/Target.app/Info.plist | head -40
```

The `plutil` command (macOS, ships with Xcode) converts the binary plist
to readable form. On Linux, use a Python plist parser instead:

```bash
python3 -c "
import plistlib
with open('ipa-out/Payload/Target.app/Info.plist','rb') as f:
    info = plistlib.load(f)
for k in ['CFBundleIdentifier','CFBundleVersion','CFBundleShortVersionString',
          'MinimumOSVersion','CFBundleURLTypes','NSAppTransportSecurity']:
    if k in info: print(k, '=', info[k])
"
```

## 2. Info.plist review

Info.plist declares the app's URL schemes, transport security policy, and
permission requests. Read it fully.

```bash
# URL schemes (deep link attack surface)
python3 -c "
import plistlib
info = plistlib.load(open('ipa-out/Payload/Target.app/Info.plist','rb'))
for t in info.get('CFBundleURLTypes', []):
    print(t.get('CFBundleURLName'), t.get('CFBundleURLSchemes'))
"

# App Transport Security exceptions (cleartext or weak TLS allowed)
plutil -p ipa-out/Payload/Target.app/Info.plist | grep -A15 NSAppTransportSecurity

# Privacy permissions (camera, location, contacts)
plutil -p ipa-out/Payload/Target.app/Info.plist | grep -E 'NS(Camera|Location|Contacts|Microphone|FaceID)UsageDescription'
```

Flag these:

- `NSAllowsArbitraryLoads` set to true: the app can use cleartext HTTP
  anywhere.
- `NSExceptionDomains` entries that allow insecure loads or weak TLS for
  specific hosts.
- URL schemes that reach sensitive functionality. Note each scheme for
  runtime fuzzing.
- Missing usage descriptions are a rejection risk, not a security
  finding, but overly broad permission requests deserve a question in
  the report.

## 3. Binary inspection

Check whether the binary is encrypted (App Store FairPlay) and which
hardening features the compiler enabled.

```bash
APP=ipa-out/Payload/Target.app/Target

# FairPlay encryption check: cryptid 1 means encrypted, skip static review
otool -l "$APP" | grep -A4 LC_ENCRYPTION_INFO | grep cryptid

# Hardening: PIE, stack canaries, ARC
otool -hv "$APP" | head -5
# Look for the PIE flag in the Mach-O header output
otool -Iv "$APP" | grep -i stack_chk | head -3
```

If `cryptid` is 1, the binary came from the App Store and is encrypted.
You need a decrypted copy from a jailbroken device (dump with frida-ios-dump
or a similar authorized tool) before static analysis. Never redistribute
decrypted binaries; keep them inside the engagement workspace.

List linked frameworks to spot interesting third party SDKs:

```bash
otool -L "$APP" | head -30
ls ipa-out/Payload/Target.app/Frameworks/
```

Strings in the binary reveal endpoints, keys, and debug messages:

```bash
strings "$APP" | grep -E -o 'https?://[^ "]+' | sort -u | head -30
strings "$APP" | grep -i -E 'api[_-]?key|secret|token' | head -20
```

## 4. Entitlements and provisioning

Entitlements define what the app is allowed to do beyond the sandbox.

```bash
# Dump entitlements from the binary
codesign -d --entitlements - ipa-out/Payload/Target.app/ 2>/dev/null

# Read the embedded provisioning profile
security cms -D -i ipa-out/Payload/Target.app/embedded.mobileprovision \
  | plutil -p - | grep -E 'application-identifier|get-task-allow|aps-environment' 
```

`get-task-allow` true means a development build that permits debugging;
fine for a test build, a finding if it ships to production. Push
notification and iCloud entitlements are normal; look for anything the
app's functionality does not justify.

## 5. Local storage review

On a jailbroken test device, inspect the app sandbox directly.

```bash
# App sandbox location (find the bundle identifier directory)
ls /var/mobile/Containers/Data/Application/ | head

# Inside the sandbox: Documents, Library, tmp
SANDBOX=/var/mobile/Containers/Data/Application/<UUID>
ls -la "$SANDBOX/Documents" "$SANDBOX/Library" "$SANDBOX/tmp"

# Plists and databases that may hold sensitive data
find "$SANDBOX" -name '*.plist' -o -name '*.db' -o -name '*.sqlite*' | head -20
```

Use objection to dump the iOS Keychain, where tokens and credentials
should live:

```bash
# Attach with objection on the jailbroken device
objection --gadget com.example.target explore

# Inside the REPL
ios keychain dump
ios plist cat /var/mobile/Containers/Data/Application/<UUID>/Library/Preferences/com.example.target.plist
ios cookies get
```

Findings here are concrete: passwords or session tokens in
NSUserDefaults plists, unencrypted databases in Documents, or Keychain
items with `kSecAttrAccessibleAlways` that survive device lock.

## 6. Runtime instrumentation with Frida

Frida on iOS needs a jailbroken device with frida-server installed, or
a device you can attach to over USB.

```bash
# List processes on the device
frida-ps -U | grep -i target

# Spawn the app with a hook script
frida -U -f com.example.target -l ./ios-hooks.js --no-pause
```

A basic iOS hook script uses Objective-C method interception:

```javascript
// Hook an Objective-C method and log its arguments
if (ObjC.available) {
    var LoginVC = ObjC.classes.LoginViewController;
    Interceptor.attach(LoginVC['- authenticateUser:'].implementation, {
        onEnter: function (args) {
            // args[0] = self, args[1] = selector, args[2] = first parameter
            var user = new ObjC.Object(args[2]);
            console.log('[*] authenticateUser called with: ' + user.toString());
        },
        onLeave: function (retval) {
            console.log('[*] authenticate returned: ' + retval);
        }
    });

    // Dump all methods of an interesting class
    var Crypto = ObjC.classes.CryptoManager;
    Crypto.$ownMethods.forEach(function (m) { console.log(m); });
}
```

Bypass jailbreak detection by hooking the common checks:

```javascript
// Neutralize common jailbreak detection calls
if (ObjC.available) {
    var checks = [
        ['UIDevice', '- isJailbroken'],
        ['JailbreakDetection', '+ isJailbroken']
    ];
    // Pattern: find methods whose names contain jailbreak indicators
    // and force them to return NO (0)
    for (var clsName in ObjC.classes) {
        if (!ObjC.classes.hasOwnProperty(clsName)) continue;
        var cls = ObjC.classes[clsName];
        try {
            cls.$ownMethods.forEach(function (m) {
                if (/jailbreak|jailBroken|cydia|rooted/i.test(m)) {
                    console.log('[*] found check: ' + clsName + ' ' + m);
                }
            });
        } catch (e) {}
    }
}
```

Enumerate first, then write targeted hooks. Blindly disabling every
method with "jailbreak" in its name can crash the app; hook one check
at a time and retest.

## 7. SSL pinning bypass on iOS

iOS apps pin with NSURLSession delegates or libraries. Bypass at runtime:

```bash
# objection one-command bypass (covers the common cases)
# Inside the objection REPL:
ios sslpinning disable
```

For custom pinning, hook the validation callback:

```javascript
// Bypass NSURLSession server trust evaluation
if (ObjC.available) {
    var NSURLSession = ObjC.classes.NSURLSession;
    // Many apps implement URLSession:didReceiveChallenge:completionHandler:
    // Hook the delegate method found during enumeration and call the
    // completion handler with NSURLSessionAuthChallengeUseCredential
    console.log('[*] enumerate the delegate class first, then hook its challenge handler');
}
```

Confirm the bypass by routing the device through Burp (install the Burp
CA profile on the test device) and watching for decrypted API traffic.

## 8. URL scheme fuzzing

URL schemes are reachable from Safari, other apps, and web pages. Fuzz
each scheme from Info.plist.

```bash
# Open a URL scheme from the device shell (simulates an external caller)
uiopen "targetapp://account/transfer?amount=9999"
uiopen "targetapp://debug?enable=1"

# From macOS with a connected device, use Safari or:
xcrun simctl openurl booted "targetapp://test"  # simulator only
```

Watch the device logs while fuzzing for crashes or unauthenticated
navigation to sensitive screens:

```bash
# Stream logs from the device
idevicesyslog 2>/dev/null | grep -i target | head -30
# Or with Frida attached, log method calls on the deep link handler
```

A URL scheme that performs an action (transfer, logout, settings change)
without user confirmation or authentication is a real finding.

## Edge cases

- The IPA is FairPlay encrypted (`cryptid` 1). Static review is
  impossible until you dump a decrypted copy from a jailbroken device.
  Budget time for this on every App Store build.
- No jailbroken device is available. Options shrink to static review,
  simulator testing (no Keychain realism, no push), and API testing
  against the backend. Say so explicitly in the report.
- The app is written in Swift. Frida's ObjC API still works for
  Objective-C bridged methods, but pure Swift methods need the Swift
  demangled names. Use `frida-trace` with Swift symbol patterns or
  hook at the lower C level.
- Bitcode or heavy Swift optimization makes the binary hard to read.
  Focus on strings, Info.plist, and runtime behavior instead of
  fighting the disassembly.
- The app uses React Native or Flutter. The interesting logic is in
  the JS bundle or the Dart snapshot, not the native shell. Extract
  the bundle from the app resources for React Native; for Flutter,
  runtime hooking is more productive than static reading.

## Escalation

- Jailbreak detection blocks every bypass attempt: enumerate the exact
  checks with Frida (file existence checks for /Applications/Cydia.app,
  suspicious URL schemes, fork() behavior), then hook each check
  individually rather than using a blanket bypass.
- Pinning lives in a closed-source SDK: identify the SDK from the
  linked frameworks, check public research for a known bypass, or hook
  below it at the SecureTransport layer.
- Keychain dump shows nothing sensitive: verify the app actually
  stores credentials (log in and re-dump), and check NSUserDefaults
  and files as the fallback locations developers misuse.
- The app refuses to run on a jailbroken device at all: test the API
  surface directly with crafted HTTP requests based on the traffic
  captured from a non-jailbroken device, and report the anti-tamper
  control as effective.
- Time is short: prioritize the Info.plist review, the Keychain dump,
  and the Burp traffic pass. Those three cover the majority of iOS
  findings on business apps.

## Detection and defender view

Defenders protect iOS apps with jailbreak detection, Frida detection
(unexpected listening ports, injected dynamic libraries, altered
memory maps), certificate pinning, Play Integrity style device
attestation where available, and server-side authorization that makes
client tampering worthless. The durable fixes mirror Android: never
trust the client, keep secrets server-side, store credentials only in
the Keychain with appropriate accessibility flags, enforce App
Transport Security without arbitrary-load exceptions, validate deep
link input and require user confirmation for actions, and disable
verbose logging in release builds. Report which controls the app has
and which bypasses succeeded, because the gap between claimed and
actual protection is often the most valuable part of the report.

## Key references

- CWE-312 (Cleartext Storage of Sensitive Information): credentials in
  NSUserDefaults or files.
- CWE-319 (Cleartext Transmission of Sensitive Information): ATS
  exceptions allowing HTTP.
- CWE-295 (Improper Certificate Validation): broken pinning.
- CWE-200 (Exposure of Sensitive Information): verbose logs and
  pasteboard leaks.
- OWASP MASVS: iOS platform and storage requirements.
- OWASP MSTG: iOS static and dynamic testing procedures.
- Apple App Transport Security documentation:
  https://developer.apple.com/documentation/security/preventing-insecure-network-connections
- Frida iOS examples: https://frida.re/docs/ios/
- objection iOS help: https://github.com/sensepost/objection/wiki
