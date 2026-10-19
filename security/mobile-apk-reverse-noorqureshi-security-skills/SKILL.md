---
name: mobile-apk-reverse
description: >
  Reverse an Android APK end-to-end — jadx/apktool unpacking, manifest and smali analysis,
  rebuild-sign-install patching, and Frida runtime hooks. Load when handed an .apk to understand,
  modify, or instrument: login/signing/risk-control logic, root or SSL-pinning checks, cert
  validation, embedded .so/JNI code. Signals: an APK in scope, "decompile/patch this app",
  smali, AndroidManifest.xml, jadx/apktool/frida/adb, System.loadLibrary, OkHttp/Retrofit.
domain: mobile
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
owasp: [M7:2024-Insufficient-Binary-Protections]
tools: [jadx, apktool, frida, adb, zipalign, apksigner, keytool]
schema_version: 1
---

# APK reversing (unpack → patch → hook)

## When it applies
You have an APK and a device/emulator you're authorized to test (`tradecraft-scope-roe`,
`scope.txt`), and the job is mechanics: read the logic, locate a check, patch and repackage, or
hook the runtime. For the broader *what-to-test* coverage map, work `mobile-android-assessment`
alongside — this skill is the reverse-engineering toolchain it routes into.

## Why it works
An APK is a zip of DEX bytecode plus resources. DEX decompiles to near-readable Java (jadx) and
round-trips losslessly through smali (apktool), so you can read at the Java level but patch at the
smali level and rebuild. Anything the app hides from static reading — decrypted strings, runtime
checks, pinning — yields to Frida instrumentation on a rooted/emulated device.

## Method
> Ready-to-adapt Frida hook recipes (crypto, OkHttp, pinning, root/emulator/anti-debug bypass,
> storage): see [`cheatsheet.md`](cheatsheet.md) next to this file.

1. **Triage — unpack both ways before touching anything.**
   ```bash
   jadx -d jadx_out app.apk            # readable Java view
   apktool d app.apk -o apktool_out    # smali + resources + manifest
   ```
   Read `AndroidManifest.xml` first: package, main activity, exported components, permissions,
   and whether `lib/` ships `.so` files. Grep jadx_out for `login|sign|encrypt|cipher|token|root|
   certificate|trust|okhttp|retrofit|webview`.
2. **Read the Java layer.** Start at `Application` and the launcher activity, then the
   auth/network/crypto classes and third-party SDK init. If jadx output is readable, locate the
   business logic here before going lower.
3. **Drop to smali when jadx is incomplete or you need to patch.** In `apktool_out`: `smali*/`,
   `res/values/strings.xml`, the manifest. Prime patch targets: root-detection return values,
   login/cert-validation branches, debug flags, `android:exported`. jadx failing on a class does
   not mean the logic is unreadable — the smali is always there.
4. **Rebuild, sign, install.**
   ```bash
   apktool b apktool_out -o rebuilt.apk
   zipalign -p 4 rebuilt.apk rebuilt-aligned.apk
   keytool -genkey -v -keystore debug.keystore -alias androiddebugkey \
     -keyalg RSA -keysize 2048 -validity 10000   # once; reuse it
   apksigner sign --ks debug.keystore rebuilt-aligned.apk
   apksigner verify rebuilt-aligned.apk
   adb install -r rebuilt-aligned.apk
   ```
5. **Dynamic hooks when static stalls** (runtime-decrypted strings, pinning, anti-tamper):
   ```bash
   adb devices && frida-ps -U                       # device + process sanity
   frida -U -f com.example.app -l hook.js           # spawn + inject
   frida-trace -U -f com.example.app -j '*!*certificate*'
   ```
   Hook the Java layer first (`javax.crypto.Cipher`, `MessageDigest`, OkHttp, WebView, the
   root/pinning checks); print arguments and returns before you start overriding them. Go to
   native hooks only when the Java layer proves to be a JNI wrapper. Full pinning-bypass technique:
   `mobile-cert-pinning-bypass`.
6. **Split to native when the `.so` carries the real logic** — signals: Java methods are thin JNI
   wrappers, the signing/risk-control logic vanishes after `System.loadLibrary()`, or cert checks
   live in native code. Find JNI entry points (`JNI_OnLoad` for dynamic registration via
   `RegisterNatives`, `Java_<pkg>_<class>_<method>` for static) and continue with
   `reverse-eng-binary-triage` on the extracted `.so`.

## Gotchas
- **Don't patch blind.** Read the manifest and main entry first; never write hooks before you know
  which class/method matters.
- **jadx partial-failure is normal** — it still emits usable output for the rest; switch to smali
  or a second engine (JEB/Ghidra) for the broken classes.
- **Signature scheme v2+ breaks on naive rezipping** — always rebuild with `apktool b` +
  `apksigner`, never by hand-editing inside the zip.
- **The app may detect the emulator/root/frida and refuse to run** — bypass hooks are in
  `cheatsheet.md`; confirm the bypass fired (the check logged) before trusting later observations.
- **Malicious-sample tells** (authorized triage only): transparent/hidden launcher icon,
  `service.d`/`priv-app` persistence, remote `curl|sh` payloads. Record indicators as evidence —
  never execute destructive commands.
- **Clean up** — uninstall patched builds and remove pushed frida-server when done.

## Verify success
You can state: entry components and key classes; whether the critical logic lives in Java, smali,
or a `.so`; every confirmed sensitive point (login, signing, root, SSL, WebView, JNI); exactly
what any patch changed; and which class/method/export each hook covered — with the rebuilt APK
installed and behaving as the patch intended.

## References
jadx & apktool documentation; Frida docs and CodeShare; OWASP MASTG.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
