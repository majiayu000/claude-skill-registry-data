---
name: wireless-wpa2-attacks
description: >
  Attack WPA2-PSK Wi-Fi end to end — monitor mode, network discovery, handshake/PMKID capture, and
  offline cracking. Load on an authorized wireless engagement with a WPA2-personal network in scope.
  Signals: an SSID/BSSID to test, a wireless adapter in monitor mode, a captured .pcap/.22000,
  "crack the Wi-Fi", "capture the handshake", aircrack-ng/hcxdumptool in play.
domain: wireless
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1040, T1110.002]
cwe: [CWE-326, CWE-521]
tools: [aircrack-ng, hcxdumptool, hcxtools, hashcat]
schema_version: 1
---

# WPA2-PSK attacks

## When it applies
An authorized wireless assessment where a WPA2-Personal (pre-shared key) network is in scope and you
have a monitor-mode-capable adapter within radio range. This is `pentest`-only — wireless testing
needs physical proximity and authorization for the specific SSIDs (record them in `scope.txt`).

## Why it works
WPA2-PSK derives its session keys from the passphrase and values exchanged in the 4-way handshake.
Capture that handshake (or a single PMKID from the AP) and you can brute the passphrase offline — no
further interaction with the network, no lockout. Weak/guessable PSKs fall quickly.

## Method
1. **Monitor mode.** `airmon-ng check kill` then `airmon-ng start wlan0` (interface → `wlan0mon`).
2. **Discover.** `airodump-ng wlan0mon` — note the target BSSID, channel, and associated clients.
3. **Capture — two routes:**
   - **4-way handshake:** lock to the channel and capture:
     `airodump-ng -c <ch> --bssid <BSSID> -w cap wlan0mon`. Speed it up with a *targeted* deauth of
     one associated client: `aireplay-ng -0 3 -a <BSSID> -c <CLIENT> wlan0mon` (minimal, not a flood).
   - **PMKID (clientless):** `hcxdumptool -i wlan0mon --enable_status=1` — grabs the PMKID from APs
     that expose it, no client needed.
4. **Convert to hashcat format.** `hcxpcapngtool -o hash.22000 cap.pcapng` (the modern `.22000`
   format replacing `.hccapx`).
5. **Crack offline.** `hashcat -m 22000 hash.22000 rockyou.txt -r rules/best64.rule` — hand off the
   deeper cracking flow to `network-credential-cracking` (wordlists, rules, masks).
6. **Prove and pivot** — once on the WLAN, treat it as a network foothold (`recon`,
   `network-*`, `network-pivoting-tunneling`).

## Gotchas
- **Deauth minimally.** A broadcast deauth flood is disruptive and often out of RoE — deauth one
  client, briefly, only to force a handshake; confirm the RoE allows it.
- **Handshake completeness** — `aircrack-ng cap.pcapng` should report a valid handshake / EAPOL
  M1-M4; a partial capture won't crack. PMKID avoids this.
- **Channel lock matters** — capturing while hopping misses frames; pin `-c <channel>`.
- **Regulatory/adapter limits** — some adapters/regions restrict channels or injection; verify the
  adapter supports monitor mode + injection first.
- **PSK strength decides everything** — a long random PSK won't crack; report that as the positive
  finding rather than burning weeks.

## Verify success
A recovered PSK that authenticates to the target SSID (or a demonstrably valid captured handshake for
a weak-PSK finding) — obtained with minimal disruption and only for in-scope SSIDs.

## References
aircrack-ng suite docs; `hcxdumptool`/`hcxtools`; hashcat mode 22000. Cracking depth:
`network-credential-cracking`.
