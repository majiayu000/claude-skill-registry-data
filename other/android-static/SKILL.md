---
name: android-static
description: Use when you need to reverse engineer an Android APK you are
  authorized to test, such as a client mobile application on a penetration
  test or a CTF challenge APK. Covers APK triage and acquisition, decompiling
  to readable Java with jadx 1.5.1, decoding resources and smali with apktool
  2.11.0, AndroidManifest analysis, exported component and permission review,
  hardcoded secret and API key hunting, WebView and deep link attack surface
  mapping, and insecure storage patterns. Use when static analysis must come
  before dynamic testing, or when you cannot run the app and must read it.
version: 1.0.0
domain: mobile
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [android-dynamic, ios-basics]
tools:
  - name: jadx
    version: 1.5.1
  - name: apktool
    version: 2.11.0
  - name: Python
    version: "3.12"
  - name: adb
    version: 35.0
---

Android static analysis is reading an APK without running it: decompiling
the Dalvik bytecode back to Java, decoding the manifest and resources, and
hunting for secrets, misconfigurations, and dangerous code patterns. It is
the cheapest way to map an app's attack surface and it works even when you
have no device or emulator. This skill covers the full authorized
methodology from APK acquisition through jadx decompilation, apktool
resource decoding, manifest review, secret hunting, and insecure code
pattern detection. All testing targets apps you have written permission to
test, such as a client app in scope or a CTF challenge APK.

## Quick Workflow

1. Acquire the APK legally (from the test device with adb, or the file
   provided in scope) and record its hash for the report.
2. Triage the APK: package name, version, target SDK, and certificate
   details, without decompiling yet.
3. Decompile to Java with jadx for readable source review.
4. Decode resources and smali with apktool for the manifest, layouts, and
   exact bytecode.
5. Review AndroidManifest.xml: permissions, exported components, deep
   links, backup flags, and debuggable flags.
6. Hunt for hardcoded secrets: API keys, tokens, URLs, and crypto keys.
7. Review code for dangerous patterns: WebViews, insecure crypto, cleartext
   storage, and custom trust managers.
8. Map every finding to a file and line number so dynamic testing can
   confirm it later.

## 1. Acquire and triage the APK

Pull the APK from the authorized test device, or use the APK file supplied
in the engagement scope. Never download APKs from third party sites for a
client test; the hash must match what the client gave you.

```bash
# List installed packages and find the target
adb shell pm list packages | grep -i target

# Find the APK path on the device, then pull it
adb shell pm path com.example.target
adb pull /data/app/com.example.target-1/base.apk ./target.apk

# Record integrity for the report
sha256sum target.apk
file target.apk

# Quick triage: package name, version, SDK levels
aapt dump badging target.apk 2>/dev/null | head -5
# If aapt is missing, unzip the listing instead
unzip -l target.apk | head -30
```

Check the signing certificate. A debug certificate on a production app is a
finding by itself.

```bash
# List the APK signature (apksigner ships with Android build-tools)
apksigner verify --print-certs target.apk | grep -E 'Signer|SHA-256'

# Or inspect the raw signature block with keytool
unzip -p target.apk META-INF/*.RSA > /tmp/cert.rsa
keytool -printcert -file /tmp/cert.rsa | head -20
```

Split APKs (base.apk plus config splits) are common. Pull every split or
the decompiled view will miss code and resources.

```bash
adb shell pm path com.example.target
# Pull each listed split: base.apk, split_config.arm64_v8a.apk, ...
for p in $(adb shell pm path com.example.target | cut -d: -f2); do
  adb pull "$p" "./splits/$(basename $p)"
done
```

## 2. Decompile with jadx

jadx converts classes.dex back into readable Java. It is the primary
reading tool for static review.

```bash
# Decompile to a source tree
jadx -d ./jadx-out target.apk

# Decompile with debug info and deobfuscation helpers
jadx -d ./jadx-out --show-bad-code --deobf target.apk

# GUI for interactive review (slower on huge APKs, use CLI first)
jadx-gui target.apk
```

Navigate the output like a source tree:

```bash
cd jadx-out
# Find the main application classes (skip android/ and androidx/ noise)
find sources -name '*.java' | grep -v -E 'androidx?/|com/google/' | head -40

# Locate the main activity and entry points
grep -rl 'extends Activity\|extends Application' sources/com/example/ | head
```

jadx output is an approximation. When a method looks wrong (bad casts,
impossible control flow), cross-check the smali from apktool before
reporting a vulnerability.

## 3. Decode resources with apktool

apktool decodes AndroidManifest.xml, layouts, and resources to readable
XML, and disassembles dex to smali.

```bash
# Decode the APK
apktool d target.apk -o ./apktool-out

# The manifest is now readable XML
head -80 apktool-out/AndroidManifest.xml
```

Use apktool output for anything the decompiler hides: resource values,
manifest flags, native library names, and the exact smali when jadx
produces suspicious code.

```bash
# List native libraries shipped with the app
find apktool-out/lib -type f | head

# Find smali files for a class jadx rendered badly
find apktool-out/smali -name 'LoginActivity.smali'
```

## 4. Manifest and component analysis

The manifest is the app's contract with Android. Read it top to bottom.

```bash
# Permissions requested
grep -o 'android:name="android.permission[^"]*"' apktool-out/AndroidManifest.xml | sort -u

# Exported components (the external attack surface)
grep -B2 -A2 'android:exported="true"' apktool-out/AndroidManifest.xml | head -60

# Deep links and URL schemes
grep -B5 -A10 'android.intent.action.VIEW' apktool-out/AndroidManifest.xml | head -80

# Dangerous global flags
grep -E 'debuggable|allowBackup|usesCleartextTraffic|networkSecurityConfig' \
  apktool-out/AndroidManifest.xml
```

Flag these immediately:

- `android:debuggable="true"` in a release build.
- `android:allowBackup="true"` (default true on old target SDKs):
  backup abuse reads app-private data via adb.
- Exported activities, services, receivers, or providers with no
  permission guard.
- Exported `ContentProvider` with `grantUriPermissions` or path
  traversal in query handling.
- `android:usesCleartextTraffic="true"` or a network security config
  that trusts user CAs in release builds.
- Deep links (`VIEW` intents with `BROWSABLE`) that reach sensitive
  screens without authentication checks.

Check the network security configuration file if one is referenced:

```bash
grep -r 'networkSecurityConfig' apktool-out/AndroidManifest.xml
# Then read the referenced XML, e.g. res/xml/network_security_config.xml
find apktool-out/res -name '*network_security*'
cat apktool-out/res/xml/network_security_config.xml
```

A config that sets `<certificates src="user" />` in the base config means
your Burp CA will be trusted, which simplifies dynamic testing but is a
finding on a production app.

## 5. Secret and API key hunting

Search the decompiled sources and resources for hardcoded credentials.
This is the highest hit-rate static activity on real apps.

```bash
cd jadx-out
# Broad secret-shaped patterns
grep -rn -i -E 'api[_-]?key|secret|password|passwd|pwd|token|aws_|sk_live|AIza' \
  sources/ resources/ 2>/dev/null | grep -v -E 'androidx?/|R\.java' | head -40

# High-entropy strings that look generated (possible keys)
grep -rn -E '"[A-Za-z0-9+/=]{32,}"' sources/com/example/ | head -20

# URLs and endpoints (map the backend attack surface)
grep -rho -E 'https?://[A-Za-z0-9._:/?=&%-]+' sources/com/example/ \
  | sort -u | head -40
```

Also check the places developers hide keys outside Java code:

```bash
# String resources
grep -rn -i -E 'key|secret|token|password' apktool-out/res/values/strings.xml | head -20

# Build config fields (BuildConfig.java)
find jadx-out/sources -name 'BuildConfig.java' -exec cat {} \;

# Assets and raw resources
ls apktool-out/assets/ 2>/dev/null
grep -rn -i -E 'api[_-]?key|secret' apktool-out/assets/ 2>/dev/null | head
```

Validate before reporting: a string named `API_KEY` with the value
`"YOUR_API_KEY_HERE"` is a placeholder, not a finding. Confirm a key is
real by checking its format (for example `AIza` prefix for Google keys)
or, only with client permission, by testing it against the provider.

## 6. Dangerous code patterns

Search for the code patterns that most often become findings.

```bash
# WebViews: JavaScript enabled, file access, and JS bridges
grep -rn 'setJavaScriptEnabled(true)' sources/com/example/ | head
grep -rn 'addJavascriptInterface' sources/com/example/ | head
grep -rn 'setAllowFileAccess(true)\|setAllowUniversalAccessFromFileURLs' sources/com/example/ | head

# Insecure crypto: ECB mode, hardcoded IVs, weak hashes for passwords
grep -rn -E 'AES/ECB|DES/|MD5|SHA1\(' sources/com/example/ | head -20
grep -rn 'IvParameterSpec\|SecretKeySpec' sources/com/example/ | head

# Custom trust managers that accept any certificate (pinning bypass target)
grep -rn -E 'X509TrustManager|checkServerTrusted|ALLOW_ALL_HOSTNAME_VERIFIER' \
  sources/com/example/ | head

# Insecure storage: world-readable files, cleartext SharedPreferences
grep -rn -E 'MODE_WORLD_READABLE|MODE_WORLD_WRITEABLE' sources/com/example/ | head
grep -rn 'getSharedPreferences' sources/com/example/ | head -20

# SQL: raw queries with string concatenation
grep -rn -E 'rawQuery\(|execSQL\(' sources/com/example/ | head

# Logging of sensitive data
grep -rn -E 'Log\.[divw]\(.*(password|token|key)' sources/com/example/ | head
```

Each pattern needs a read of the surrounding method before it becomes a
finding. `setJavaScriptEnabled(true)` on a WebView that only loads a local
asset is low risk; the same call on a WebView loading remote URLs with an
`addJavascriptInterface` bridge is a real attack surface.

## 7. Native libraries

Apps with `.so` files hide logic from jadx. List them and decide whether
deeper binary analysis is worth the time.

```bash
# Architectures and library names
find apktool-out/lib -name '*.so' | head -20

# Check which libraries are third party SDKs vs app code
for f in $(find apktool-out/lib/arm64-v8a -name '*.so' | head); do
  echo "== $f"; strings "$f" | grep -i -m3 -E 'version|copyright'
done
```

Hand interesting native libraries to the ghidra-basics skill for
deeper review, especially ones referenced from JNI entry points in the
Java code (`System.loadLibrary` calls and `native` method declarations).

## 8. Assemble findings

Record every finding with file, line, and the exact snippet. Static
findings are hypotheses until dynamic testing confirms them.

```bash
# Example evidence line for the report
grep -n 'setJavaScriptEnabled(true)' \
  jadx-out/sources/com/example/target/WebActivity.java
```

Typical static report items: hardcoded API keys, debuggable or backup
flags, exported components without permission guards, cleartext traffic
allowed, weak crypto modes, sensitive data in logs, and deep links into
authenticated areas.

## Edge cases

- The APK is heavily obfuscated (ProGuard or R8 with full renaming).
  Class names become `a.b.c`. Follow the flow from the manifest entry
  points and string constants instead of class names.
- String encryption hides API keys from grep. Look for a decryption
  routine called at startup, or pivot to dynamic analysis with Frida to
  read the decrypted values at runtime.
- Native code holds the real logic. jadx shows only JNI stubs. Budget
  time for Ghidra on the `.so` files or the finding stays unconfirmed.
- Multi-dex apps (`classes2.dex`, `classes3.dex`). jadx handles these
  automatically, but a manual `dexdump` triage can miss them. Always
  confirm jadx processed every dex file.
- The app uses a commercial packer or protector. Decompilation output
  is garbage. Note the packer as a limitation and move to dynamic
  analysis; do not guess at findings from corrupted output.
- Resources are split across configuration APKs. If layouts look
  missing, you pulled only base.apk. Pull every split from the device.

## Escalation

- jadx fails or produces empty output: try `jadx --no-res` to skip
  resource decoding, update jadx to the latest release, or fall back to
  `dex2jar` plus a Java decompiler such as CFR.
- apktool fails to decode: the APK may use a newer resource format.
  Update apktool, or read the manifest with `aapt dump xmltree`
  instead of full decoding.
- Grep finds nothing because of string encryption or reflection-heavy
  code: switch to dynamic analysis (android-dynamic skill) and hook
  the crypto and network APIs at runtime.
- The app is a game or Flutter/React Native app: the Java layer is a
  thin wrapper. For Flutter, look at `libapp.so` and Dart snapshot
  analysis; for React Native, read the JS bundle in assets.
- You suspect a vulnerability in a third party SDK: isolate the SDK
  package, review its version against public advisories, and test the
  SDK's behavior rather than auditing its entire codebase.

## Detection and defender view

Defenders and app owners see static analysis as APK extraction and
decompilation, which leaves no trace on their servers, so detection is
not the point. The defender view is about making static analysis
unproductive: enable R8 full mode with obfuscation and string encryption
for sensitive constants, never hardcode secrets (fetch them from the
backend after authentication), set `allowBackup="false"`, keep
`debuggable` false in release builds, minimize exported components and
guard each with a signature-level permission, enforce HTTPS with a strict
network security config, and add root and tamper detection so static
findings cannot be trivially confirmed at runtime. None of these stop a
determined analyst; they raise the cost and shrink the findings list.

## Key references

- CWE-312 (Cleartext Storage of Sensitive Information): hardcoded keys
  and tokens.
- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): ECB mode,
  MD5, DES.
- CWE-276 (Incorrect Default Permissions): exported components without
  guards.
- CWE-319 (Cleartext Transmission of Sensitive Information):
  usesCleartextTraffic.
- CWE-532 (Insertion of Sensitive Information into Log File).
- CWE-749 (Exposed Dangerous Method or Function): JavascriptInterface
  bridges.
- OWASP MASVS (Mobile Application Security Verification Standard):
  storage, crypto, and platform interaction requirements.
- OWASP MSTG (Mobile Security Testing Guide): Android static testing
  procedures.
- jadx documentation: https://github.com/skylot/jadx
- apktool documentation: https://apktool.org/documentation/
