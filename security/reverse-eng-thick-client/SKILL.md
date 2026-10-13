---
name: reverse-eng-thick-client
description: >
  Security-test a desktop thick client end to end: map its trust boundaries, then work the
  local attack surface (config files, credential storage, IPC, update channel) and the network
  surface (proxying, certificate pinning, hidden APIs). Load for a C/S desktop app in scope —
  Electron, Qt, .NET WinForms/WPF, or native — an installer to audit, local config/credential
  storage to assess, named pipes or loopback IPC, an auto-update channel, or a client that
  hides admin-only API calls.
domain: reverse-engineering
type: methodology
stability: learning
modes: [pentest, bugbounty]
severity: high
cwe: [CWE-798, CWE-312, CWE-426, CWE-319]
tools: [procmon, sysinternals, burp, mitmproxy, dnspy, ghidra, asar, frida]
schema_version: 1
---

# Thick client security testing

## When it applies
The engagement includes a desktop application — a client-server (C/S) client built on
Electron, Qt, .NET WinForms/WPF, or native code — rather than a pure web app. Typical triggers:
an installer in scope, credentials cached locally, an auto-updater, a loopback port or named
pipe, or API calls the UI never exposes. Record the installer source and the test accounts in
`scope.txt` (`tradecraft-scope-roe`); test only machines and accounts you're authorized for.

## Why it works
A thick client is a server-side trust boundary shipped to an attacker-controlled machine:
everything it stores, every check it enforces locally, and every API it knows how to call is
yours to read. The client cannot keep secrets from its operator — so hardcoded keys, hidden
admin endpoints, and client-enforced validation are structural findings, not luck.

## Method
Work boundary → local surface → network surface → reverse-engineering confirmation.

1. **Map the trust boundary.** Enumerate the process tree and child processes, any services or
   drivers it installs, listening ports (a loopback socket bound to `0.0.0.0` is an instant
   finding), outbound domains, and the sensitive paths it touches: `%APPDATA%`, Keychain,
   registry hives. Process Monitor and TCPView (Sysinternals) get you this in minutes.
2. **Work the local attack surface.** Look for plaintext config and logs, hardcoded keys,
   leftover debug switches and hidden menus, SQLite databases (permissions and encryption),
   credential storage (DPAPI / Keychain / plaintext), autostart entries, install/uninstall
   residue and file permissions, and on Windows DLL search-order hijacking. Check IPC: who can
   connect to the named pipe / loopback port, and is there any authentication?
3. **Work the network surface.** Determine whether the app honors the system proxy or uses
   custom TLS; force it through Burp/mitmproxy. Certificate pinning → the usual bypasses
   (`mobile-cert-pinning-bypass` techniques, or Frida on the desktop process). Once traffic is
   visible, hunt client-hidden API surface: admin functions the UI gates but the server may
   not — feed the recovered endpoints into `api-testing-checklist` / `api-bola`.
4. **Reverse to confirm.** .NET → dnSpy/ILSpy (deobfuscate with de4dot if needed). Native →
   `reverse-eng-binary-triage`. Electron → extract `app.asar` (`npx asar extract app.asar out/`)
   and treat it as front-end JS (`reverse-eng-js`). Verify how licenses, signatures, and
   integrity checks are enforced — anything checked only client-side is bypassable by design.
5. **Update channel & supply chain.** Check the update URL (HTTP vs HTTPS), whether the update
   package is signature-verified, and whether the check itself runs client-side. A confirmed
   weak update channel is high-impact — document, don't weaponize, without explicit scope.

## Gotchas
- **Electron apps are web apps in a trench coat** — don't start with a disassembler; the
  `asar` plus DevTools answers most questions in minutes.
- **.NET obfuscation** makes dnSpy output noisy — run de4dot first, and prefer runtime
  inspection (dnSpy debugger) over static reading for the interesting checks.
- **"Server validates too" assumption** — never report client-side-only checks without testing
  the server's response to a tampered request; some are genuinely enforced server-side.
- **Clean up your artifacts** — remove planted DLLs, proxy certificates, patched binaries, and
  test accounts when done (house rule: minimize footprint).

## Verify success
You have a trust-boundary diagram (processes, ports, files, servers), both local and network
surfaces covered, and at least one concrete, demonstrated finding class — e.g. a recovered
secret, a server-accepted tampered request, or an unauthenticated IPC connection — validated
per `reporting-triage-validation`.

## References
OWASP Desktop Application Security Top 10; Sysinternals suite; dnSpy docs; `reverse-eng-js`,
`reverse-eng-binary-triage`, `mobile-cert-pinning-bypass` in this library.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
