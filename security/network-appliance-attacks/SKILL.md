---
name: network-appliance-attacks
description: >
  Offensively test perimeter appliances and VPN crypto — IKE/IPsec aggressive mode, transform/DH
  enumeration, safe firmware/version inference for FortiGate / PAN-OS / Cisco ASA / Citrix feeding
  CVE applicability, TLS-version posture, and NTLM Type-2 info leaks. Load when an edge firewall,
  VPN, or load balancer is in scope. Signals: UDP 500/4500, ports 4433/10443/443 on an appliance,
  "SSL-VPN"/"Global Protect"/"Pulse"/"NetScaler" banners, Check Point SIC (18190/18191).
domain: network
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A06:2021-Vulnerable-and-Outdated-Components]
mitre: [T1190, T1133]
cwe: [CWE-1188, CWE-326]
tools: [ike-scan, nmap, openssl, nvd]
schema_version: 1
---

# Perimeter appliance & VPN offensive testing

## When it applies
An internet-facing appliance is in scope — a firewall/SSL-VPN (FortiGate, PAN-OS/GlobalProtect,
Cisco ASA, Citrix NetScaler, Ivanti/Pulse), a Check Point gateway, or a load balancer — and you
must *test the live device*, not just audit its config (`network-service-attacks` covers generic
ports/SMB; `defense-hardening-baseline` is the config-audit counterpart). Edge appliances are today's number-one
initial-access vector, so a version→CVE call has to be precise.

## Why it works
Appliances expose crypto and management surfaces that leak more than they should: IKE aggressive
mode hands out a crackable PSK hash, unauthenticated NTLM challenges leak internal host/domain
names, and login pages/certs disclose enough to pin a firmware version. The trick is discipline:
**infer, don't assume** — a version banner alone never proves a CVE, because banners are
backported and spoofable. Every CVE call is a precondition check, not a blind "vulnerable."

## Method
1. **Fingerprint the appliance.** From the port set, banners, login markers, and cert CN/serial,
   pin vendor + firmware version *with a confidence level*. Low confidence stays `undetermined` —
   do not score CVEs against a guess.
2. **VPN crypto (UDP 500/4500).** Enumerate IKE:
   `ike-scan -A -M <ip>` (`-A` = aggressive mode). Aggressive mode responding with a hash payload
   **is the finding** (offline PSK crack needs explicit authorization — flagging the exposure is
   enough). Enumerate accepted transforms and weak DH groups (1/2/5); decode NAT-T/NOTIFY.
3. **TLS posture.** Report only TLS versions that **complete a handshake**
   (`openssl s_client -connect host:443 -tls1_1`) — a non-zero `openssl` exit or SECLEVEL block is
   *not* proof the version is unsupported. TLS 1.0/1.1 completing is the weak-protocol finding.
4. **Info leaks.** Decode any NTLM Type-2 (CHALLENGE) from an unauthenticated management endpoint
   for NetBIOS/DNS host, domain, forest, and OS build — report as information disclosure; no auth
   attempted.
5. **CVE applicability (precondition-gated).** For each candidate appliance CVE, combine the
   vendor+version (step 1) with the required precondition (e.g. a CVE needing IKEv1 aggressive
   mode is `not_applicable` on an IKEv2-only responder; a Check Point RA CVE applies only if the
   Remote-Access/Mobile-Access marker is present). Mark `applicable` / `undetermined` /
   `not_applicable`; enrich against the NVD. Report `undetermined` as such — never inflate it.

## Gotchas
- **Non-destructive by default.** These are observe/decode/infer steps; do not fire an appliance
  exploit or a DoS-prone probe without explicit written authorization — many edge CVEs are
  memory-corruption and crash the device.
- **Banners lie** — backported patches keep an old version string on a fixed build, and versions
  are spoofable. Gate on the precondition, not the banner.
- **A firewall forges RSTs** — don't assert "live internal host behind the firewall" from a RST
  alone; you need an open-service TTL baseline to discriminate, else it's `undetermined`.
- **IKE PSK cracking is out-of-band** and needs authorization; capturing the aggressive-mode
  exposure is the in-scope finding.

## Verify success
A concrete, precondition-backed statement: e.g. "IKEv1 aggressive mode enabled on UDP 500, PSK
hash returned" or "FortiOS 7.0.x pinned from the login marker + cert serial; CVE-XXXX-YYYY
`applicable`" — with the observation that supports it, not a bare version guess.

## References
`ike-scan` docs; vendor PSIRT advisories; NIST NVD; MITRE ATT&CK T1190 (Exploit Public-Facing
Application), T1133 (External Remote Services). Config-audit counterpart: `defense-hardening-baseline`.
