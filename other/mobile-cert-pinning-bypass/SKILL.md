---
name: mobile-cert-pinning-bypass
description: >
  Bypass TLS certificate pinning so you can proxy a mobile app's traffic. Load when a proxy
  shows no/broken traffic, you see SSL handshake failures in logs, OkHttp CertificatePinner,
  TrustKit, or "the app won't connect through Burp". Android/iOS.
domain: mobile
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
cwe: [CWE-295]
tools: [frida, objection, mitmproxy, apktool]
schema_version: 1
---

# Certificate pinning bypass

## When it applies
The app pins its server cert, so a normal MITM proxy (Burp/mitmproxy) can't decrypt its
traffic — you get handshake errors and empty history. You need to test the backend, so the pin
has to go.

## Why it works
Pinning is enforced in the client you control. At runtime you can replace/neutralize the
verification routine; statically you can patch it out. Either way the app then trusts your
proxy's CA.

## Method
1. **Install your CA** first: add Burp/mitmproxy CA to the device (Android 7+ needs it as a
   *system* cert, or use a `network_security_config` on a repackaged app).
2. **Runtime (fastest)**: `objection -g <pkg> explore` then `android sslpinning disable`
   (iOS: `ios sslpinning disable`), or a Frida script (`frida-multiple-unpinning`).
3. **Static patch** (when Frida is blocked): `apktool d`, remove/patch the `CertificatePinner`
   / TrustManager checks or swap `network_security_config` to trust user CAs, rebuild + resign
   (`apktool b`, `uber-apk-signer`).
4. **Confirm**: traffic now appears decrypted in the proxy; proceed to backend testing.

## Gotchas
- No traffic at all (not just pinning) can mean the app uses a non-HTTP protocol or a VPN — check.
- Some apps double-pin or detect Frida/root — combine root-detection bypass, or use static patching.
- iOS on a non-jailbroken device needs a repackaged/sideloaded app or a jailbroken test device.

## Verify success
The proxy shows plaintext requests/responses from the app; you can now replay/modify them.

## References
OWASP MASTG (network); objection & frida-multiple-unpinning; TrustKit/OkHttp docs.
