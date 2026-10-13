---
name: defense-network-detection
description: >
  Detect attacker activity in network telemetry — C2 beaconing, DNS tunnelling, data exfil, and
  lateral movement. Load for "detect C2", "find beaconing", "network monitoring / NSM", "suspicious
  traffic", or building Zeek/Suricata coverage. The defensive counterpart to the offensive
  network/pivoting skills.
domain: defense
type: technique
stability: learning
modes: [defense]
severity: info
mitre: [T1071, T1048, T1572, T1021]
tools: [zeek, suricata, rita, arkime, ja4]
schema_version: 1
---

# Network detection (NSM)

## When it applies
You have network visibility (a tap/SPAN, Zeek/Suricata logs, or NetFlow) and want to catch activity
that endpoint tooling misses — especially C2 and exfil that look like ordinary connections.

## Why it works
Malware still has to talk. Even encrypted C2 leaks *behavioural* tells the payload can't hide:
regular call-home intervals, tiny requests with large responses, odd JA3/JA4 TLS fingerprints, and
destinations no user browses to. Metadata beats payload inspection in a TLS world.

## Method
1. **Beaconing**: hunt for connections at regular intervals with low jitter to the same destination
   (RITA's beacon analysis over Zeek `conn.log`); score by consistency, not volume.
2. **DNS tunnelling**: high volume of TXT/NULL queries, long/high-entropy subdomains, one domain
   answering for everything — flag on query length + entropy + count per parent domain.
3. **Exfil**: outbound bytes >> inbound to a rare destination, off-hours transfers, upload to
   unsanctioned cloud — baseline egress and alert on the outliers.
4. **Lateral movement**: internal SMB/WinRM/RDP between hosts that never normally talk; new
   admin-share access — east-west, not just north-south.
5. **TLS fingerprinting**: JA3/JA4(S) on the client hello — known-bad or rare fingerprints betray
   tooling even without decryption.

## Gotchas
- Legit software beacons too (update checks, telemetry) — baseline and allowlist, or you drown.
- Encrypted payloads mean you detect *patterns*, not content; don't wait for a plaintext IOC.
- CDNs and cloud fronting make destination reputation noisy — combine signals, don't rely on one.

## Verify success
A controlled C2/exfil reproduction (e.g. a lab beacon) is flagged by the beacon/entropy/egress
logic, while normal baseline traffic stays quiet.

## References
Zeek; Suricata; Active Countermeasures RITA; JA3/JA4; MITRE ATT&CK (Command and Control, Exfiltration).
