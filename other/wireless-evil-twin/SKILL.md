---
name: wireless-evil-twin
description: >
  Stand up a rogue/evil-twin access point to harvest credentials — WPA2-Enterprise PEAP-MSCHAPv2
  challenge/response and captive-portal capture. Load on an authorized wireless engagement targeting
  WPA-Enterprise (802.1X) or a portal-based network. Signals: PEAP/EAP/802.1X, RADIUS, "enterprise
  Wi-Fi", eaphammer/hostapd-wpe in play, a captive portal, corporate SSID with per-user logins.
domain: wireless
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1557, T1556]
cwe: [CWE-290, CWE-522]
tools: [eaphammer, hostapd-wpe, hashcat, asleap]
schema_version: 1
---

# Evil-twin / rogue AP (enterprise credential harvesting)

## When it applies
An authorized assessment of a WPA2-**Enterprise** (802.1X) network, or a captive-portal Wi-Fi, where
clients can be lured to a look-alike AP. `pentest`-only, in-scope SSIDs recorded in `scope.txt`, and
coordinated so you only capture *test/consenting* users' credentials per RoE.

## Why it works
WPA2-Enterprise authenticates users to a RADIUS server, but many clients don't properly validate the
RADIUS server's certificate. A rogue AP advertising the same SSID can complete enough of the
PEAP-MSCHAPv2 exchange to capture each user's username + MSCHAPv2 challenge/response, which cracks
offline to the domain password. Captive portals simply hand you the credentials the user types.

## Method
1. **Profile the target** (`wireless-wpa2-attacks` recon): SSID, the EAP type (PEAP/EAP-TTLS), and
   whether clients validate the server cert (they often don't).
2. **Stand up the evil twin.** `eaphammer` (or `hostapd-wpe`):
   `eaphammer --cert-wizard` then
   `eaphammer -i wlan0 --essid <SSID> --creds` — advertises the SSID and runs a rogue RADIUS that
   logs credentials.
3. **Lure clients** — same SSID (and, per RoE, a stronger signal / brief targeted deauth of the real
   AP to prompt roaming). Keep disruption minimal and in-scope.
4. **Capture & crack** the PEAP-MSCHAPv2 username + challenge/response:
   `hashcat -m 5500 netntlm.txt wordlist` (or `asleap`) → domain password.
5. **Captive-portal variant** — clone the portal page on the rogue AP to capture typed creds
   directly; disclose per the SE guardrails in `social-eng-methodology`.
6. **Pivot** — validated creds feed `network-password-spraying`, VPN/OWA access, and AD work.

## Gotchas
- **You're capturing real people's credentials** — this is human-adjacent: only in-scope SSIDs,
  coordinate with the client, minimize capture, and protect/destroy what you collect per RoE (treat
  like `social-eng` data discipline).
- **Cert validation defeats it** — clients that properly pin/validate the RADIUS cert won't leak;
  that's the positive finding (report "clients validate the server cert").
- **Deauth/luring can be disruptive and out of RoE** — confirm before forcing roaming.
- **MSCHAPv2 capture format** must match hashcat `-m 5500` exactly — use the tool's emitted format.
- **Legal line** — capturing enterprise creds without explicit authorization is illegal; stop if
  scope is unclear (`tradecraft-scope-roe`).

## Verify success
Captured PEAP-MSCHAPv2 credentials that crack to a working domain password (or portal creds that
authenticate) — for in-scope, authorized users only, with a "clients don't validate the RADIUS cert"
root cause for the report.

## References
`eaphammer` / `hostapd-wpe` docs; hashcat mode 5500; PEAP-MSCHAPv2 weaknesses. Data discipline:
`social-eng-methodology`; follow-on: `network-password-spraying`.
