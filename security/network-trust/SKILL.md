---
name: network-trust
version: "1.0.0"
description: Network-layer trust and adversary-in-the-middle resistance for mid-2026 — DNSSEC validation, DANE/TLSA pinning, TSIG, mTLS private-CA pinning, RFC 9421 HTTP message signatures, DNS-rebinding/SSRF guarding, and authenticated time (NTS) and its effect on certificate validity and TOTP
triggers:
  - network trust
  - adversary in the middle
  - aitm
  - dnssec
  - dane
  - tlsa
  - tsig
  - mtls pinning
  - certificate pinning
  - http message signature
  - rfc 9421
  - dns rebinding
  - nts
  - authenticated time
  - ntp spoofing
  - public suffix list
  - name resolution trust
discovery_mode: standalone
data_deps:
  - cve-catalog.json
  - atlas-ttps.json
  - attack-techniques.json
  - framework-control-gaps.json
  - cwe-catalog.json
  - rfc-references.json
atlas_refs: []
attack_refs:
  - T1557
  - T1071.004
  - T1556
framework_gaps:
  - NIST-800-53-SC-8
  - ISO-27001-2022-A.8.21
  - NIS2-Art21-network-security
  - UK-CAF-B4
cwe_refs:
  - CWE-345
  - CWE-918
  - CWE-290
  - CWE-347
last_threat_review: "2026-06-02"
---

# Network-Layer Trust (AiTM Resistance)

## Threat Context (mid-2026)

Below the application, TLS authenticates a certificate against a CA bundle — not the specific peer you intended to reach, and not the DNS answer or the clock that got you there. Adversary-in-the-middle attacks exploit the trust-anchor validation TLS does not perform: forge a DNS answer where DNSSEC is not validated; present a mis-issued-but-CA-valid certificate where DANE/TLSA or an mTLS CA pin is not checked; shift an unauthenticated clock to revive an expired certificate or a TOTP window; or rebind a name from a public to an internal address. The DNSSEC validation surface itself carries availability risk (KeyTrap CVE-2023-50387, NSEC3 CVE-2023-50868). These are validation-posture gaps, not cryptographic-primitive weaknesses.

## Framework Lag Declaration

Organisational network controls equate TLS with peer authenticity and assume DNS and time are trustworthy. NIST 800-53 SC-8 (transmission integrity) is satisfied by TLS to a CA bundle and does not require DANE pinning, DNSSEC, or authenticated time. ISO 27001 A.8.21 (security of network services) is met with TLS + a CA bundle. NIS2 Art.21 names network security of essential services but not the DNS/time/transport trust-anchor posture that AiTM exploits. A clean "we use TLS and a validating resolver and NTP" audit is therefore NON-EVIDENCE for network-trust posture; it confirms encryption and a CA bundle, not end-to-end DNSSEC validation, peer pinning, or authenticated time.

## TTP Mapping

The network-trust failures map to MITRE ATT&CK: **T1557 (Adversary-in-the-Middle)** for mis-issued-certificate acceptance (no DANE/mTLS pin), DNS-rebinding SSRF, and clock-shift cert revival; **T1071.004 (Application Layer Protocol: DNS)** for forged answers accepted without DNSSEC and unauthenticated zone transfer/update without TSIG; and **T1556 (Modify Authentication Process)** for unverified HTTP message signatures and PSL-driven cookie-boundary confusion, plus the TOTP-window impact of time-shift. The weakness classes are CWE-345 (insufficient verification of data authenticity), CWE-918 (SSRF via DNS rebinding), CWE-290 (authentication bypass by spoofing), and CWE-347 (improper signature/certificate verification).

## Exploit Availability Matrix

These are posture gaps, so weaponisation is low-cost given an on-path or DNS-influencing position. DNS forgery and cache poisoning have commodity tooling; the DNSSEC validation surface's own DoS (KeyTrap / NSEC3) is catalogued with public analysis. DNS rebinding has public frameworks. A mis-issued or compromised-CA certificate is a recurring real-world event that DANE/mTLS pinning is designed to contain. Unauthenticated NTP is steerable by any on-path attacker. None require a novel exploit; the exploit is the absent validation. Real-world priority is driven by whether the unvalidated anchor sits on an internet-facing authentication, credential, or payment path, and by how many trust decisions ride on it.

## Analysis Procedure

1. Inventory the paths whose security depends on DNS authenticity, peer-certificate identity, accurate time, or request-signature integrity. 2. Confirm the application path validates DNSSEC end-to-end (or trusts a validated upstream over DoT/DoH) and guards DNS rebinding (pin resolved IP, refuse private ranges). 3. Confirm DANE/TLSA is checked on capable peers and that mTLS pins the expected private CA / SPKI rather than the full public bundle. 4. Confirm time is authenticated (NTS or an authenticated source) and treated as a trust input for cert-validity and TOTP. 5. Confirm TSIG on zone operations and adequately-scoped RFC 9421 message-signature verification. 6. Confirm the Public Suffix List is current. Run the `network-trust` playbook to execute these as detect indicators with false-positive checks, then score by reachability and the number of trust decisions affected.

## Output Format

Report per trust anchor (DNS, peer certificate, time, message signature), marking each enforced / missing / inconclusive (visibility gap). For every missing check, state whether the path is internet-facing and which trust decisions (peer auth, name resolution, cert validity, TOTP) depend on it. Distinguish a genuinely-not-in-scope anchor (no DANE-capable peer, no authoritative zone, fixed pinned IP) from an unvalidated one. Provide the prioritised remediation (validate DNSSEC + guard rebinding, pin peer certificates via DANE/mTLS, authenticate time, require TSIG + verify message signatures, refresh the PSL) and the negative validation tests that prove each fix (forged DNS rejected, mis-issued cert rejected, time-shift cannot revive a cert) plus a functional test that legitimate traffic still flows.

## Compliance Theater Check

The recurring theater is "we use TLS everywhere, so the peer is authenticated," "we use a DNSSEC-validating resolver," and "time sync is handled." TLS authenticates against a CA bundle, not the expected peer; a validating resolver upstream is moot if the application accepts any answer over an unauthenticated hop; unauthenticated NTP is attacker-steerable. The distinguishing test: confirm the application path checks DANE/TLSA (or pins the mTLS CA), trusts the AD flag / validates DNSSEC end-to-end, and uses authenticated time. If a forged DNS answer, a mis-issued certificate, or a time shift would be accepted, TLS did not make the network trustworthy and the assurance is paper.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: DNSSEC validation and DNS-rebinding guarding realise DNS Traffic Analysis and Resolution-Trust enforcement (countering T1071.004/T1557); DANE/TLSA and mTLS CA pinning realise Certificate Pinning and Public Key Infrastructure validation (countering T1557 mis-issuance); authenticated time (NTS) realises System Time Integrity (countering clock-shift cert/TOTP abuse); RFC 9421 message-signature verification realises Message Authentication (countering T1556). Pair DANE with DNSSEC (TLSA without DNSSEC is meaningless) and treat the clock as a security input. The residual risk after validation is compromise of the trust anchor itself (signing key, pinned CA, time authority), addressed by key-management and monitoring, accepted at the CISO level.
