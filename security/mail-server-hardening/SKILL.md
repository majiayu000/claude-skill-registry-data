---
name: mail-server-hardening
version: "1.0.0"
description: Inbound mail-server protocol hardening for mid-2026 — SMTP smuggling, STARTTLS command/response injection, IMAP/POP3/ManageSieve command injection, Sieve redirect exfiltration, open relay, mailbox-DAV traversal/XXE, and cleartext-AUTH (the server-side protocol layer that SPF/DKIM/DMARC do not protect)
triggers:
  - mail server hardening
  - smtp smuggling
  - starttls injection
  - open relay
  - imap command injection
  - managesieve
  - sieve redirect
  - mailbox dav
  - caldav
  - carddav
  - pop3
  - mx hardening
  - rfc 5321
  - rfc 9051
  - rfc 5804
  - mail protocol
  - inbound mail
  - smtp listener
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
  - T1190
  - T1071.003
  - T1557
framework_gaps:
  - NIST-800-53-SI-2
  - ISO-27001-2022-A.8.8
  - NIS2-Art21-network-security
  - PCI-DSS-4.0-6.3.3
cwe_refs:
  - CWE-77
  - CWE-93
  - CWE-22
  - CWE-611
  - CWE-863
  - CWE-400
last_threat_review: "2026-06-02"
---

# Inbound Mail-Server Protocol Hardening

## Threat Context (mid-2026)

A mail server that terminates inbound SMTP, IMAP, POP3, JMAP, or ManageSieve exposes a protocol surface that sender-authentication (SPF/DKIM/DMARC) and transport TLS do not protect. SMTP smuggling (CVE-2023-51764/51765/51766) exploits a server that accepts a non-standard end-of-data sequence to deliver a second message that inherits the outer connection's authentication pass — spoofed mail past DMARC. STARTTLS command/response injection (CVE-2021-38371, CVE-2021-33515) executes attacker plaintext buffered before the handshake. An open relay lends the operator's reputation to spammers. Uncapped Sieve `redirect` is a silent mail-exfiltration primitive. Mailbox-DAV (CalDAV/CardDAV) endpoints add path-traversal and XXE. Each is a configuration or parser-hardening gap, not a CVE to patch.

## Framework Lag Declaration

Organisational mail controls center on sender authentication and transport encryption: SPF, DKIM, DMARC, and a TLS certificate. None prescribe the server-side protocol hardening this skill audits. NIST 800-53 SI-2 expects flaw remediation via a patch cadence, but the smuggling and STARTTLS-injection fixes are configuration (strict end-of-data handling, receive-buffer drain) the patch process never surfaces. NIS2 Art.21 names network security of essential services but assumes SPF/DKIM/DMARC and TLS suffice — they are bypassed at the protocol layer. A clean DMARC + TLS audit is therefore NON-EVIDENCE for inbound protocol hardening; the two address different boundaries.

## TTP Mapping

The inbound mail-protocol failures map to MITRE ATT&CK: **T1190 (Exploit Public-Facing Application)** for command-literal injection in the IMAP/POP3/ManageSieve parsers and mailbox-DAV traversal/XXE; **T1071.003 (Application Layer Protocol: Mail Protocols)** for SMTP smuggling delivering spoofed mail and open-relay abuse; and **T1557 (Adversary-in-the-Middle)** for STARTTLS receive-buffer injection that crosses the TLS boundary. Cleartext AUTH before STARTTLS enables **T1040 (Network Sniffing)**; absent auth rate limiting enables **T1110 (Brute Force)**; uncapped Sieve redirect enables **T1114 (Email Collection)**. The weakness classes are CWE-93 (CRLF/smuggling), CWE-77 (command injection), CWE-22 (path traversal), CWE-611 (XXE), CWE-863 (open-relay authorization), and CWE-400 (uncapped Sieve/PUTSCRIPT resource use).

## Exploit Availability Matrix

These are protocol-posture gaps, so weaponisation is low-cost and reusable. SMTP smuggling has public tooling (SEC Consult, December 2023) and the CVE-2023-51764/51765/51766 entries are catalogued. STARTTLS injection has public test tooling from the 2021 "NO STARTTLS" research (CVE-2021-38371, CVE-2021-33515). Open-relay testing requires only an unauthenticated MAIL FROM + RCPT TO probe. Command-literal injection and mailbox-DAV traversal require only a crafted protocol line. None need a novel exploit; the exploit is the absence of the check. Real-world priority is driven by internet-reachability of the listener and whether the gap yields spoofing/relay (reputation + phishing delivery) or mailbox-data exposure.

## Analysis Procedure

1. Inventory every inbound mail listener and its port (implicit-TLS 465/993/995 vs opportunistic-STARTTLS 25/587/143/110/4190). 2. Probe SMTP for non-standard end-of-data acceptance (smuggling) and unauthenticated relay. 3. Probe each opportunistic-STARTTLS listener for an undrained pre-handshake buffer and for AUTH offered before TLS. 4. Inspect the IMAP/POP3 parsers for bare-CR/LF acceptance and the ManageSieve listener for unbounded PUTSCRIPT and cleartext AUTH. 5. Inspect the Sieve engine for an uncapped `redirect` and the mailbox-DAV endpoint for traversal + XXE. 6. Confirm auth rate limiting / greylisting is active. Run the `mail-server-hardening` playbook to execute these as detect indicators with false-positive checks, then score by reachability and impact class.

## Output Format

Report per listener and protocol, marking each hardening check enforced / missing / inconclusive (visibility gap). For every missing check, state the port, whether it is internet-facing, and whether the gap yields spoofing/relay or mailbox-data exposure. Distinguish a live-listener finding from a documented test fixture or an upstream-proxy-enforced control. Provide the prioritised remediation (enforce standard end-of-data, drain the STARTTLS buffer and gate AUTH on TLS, harden the command parsers, restrict relay and cap Sieve redirect, harden mailbox-DAV and add rate limits) and the negative validation tests that prove each fix (smuggling rejected, relay rejected, STARTTLS injection rejected) plus the functional test that legitimate mail still flows.

## Compliance Theater Check

The recurring theater is "we have SPF/DKIM/DMARC and TLS, so our mail server is secure" and "relay is restricted in our config." Sender authentication and transport TLS protect different boundaries than the inbound protocol parser; a config flag is not evidence the listener enforces it. The distinguishing test: probe the live inbound listener for non-standard end-of-data acceptance, an undrained STARTTLS buffer, unauthenticated relay, and cleartext AUTH. If any probe succeeds, the DMARC record and TLS certificate did not protect the protocol layer, and the assurance is paper. "Relay is restricted" is theater until an unauthenticated RCPT-to-external probe is actually refused.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: strict end-of-data enforcement and command-parser hardening realise Message Authentication and Inbound Traffic Filtering (countering T1071.003/T1190); STARTTLS receive-buffer draining and AUTH-after-TLS gating realise Transport Session Integrity (countering T1557/T1040); relay authorization realises Outbound Traffic Filtering (countering open-relay reputation abuse); Sieve redirect caps realise Email Filtering (countering T1114 exfiltration). Pair the protocol hardening with auth rate limiting and greylisting (countering T1110). The residual risk after hardening is a compromised authenticated account acting within its own authorization, which protocol hardening does not address — accept it at the CISO level with identity-control compensation.
