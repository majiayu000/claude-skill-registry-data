---
name: self-update-integrity
version: "1.0.0"
description: Consumer-side self-update and artifact integrity for mid-2026 — signature-verification-before-apply, out-of-band key pinning, anti-rollback/downgrade protection, channel pinning, Subresource Integrity on browser modules, and C2PA / SCITT-TSA transparency verification on received artifacts
triggers:
  - self update
  - auto update
  - update integrity
  - anti rollback
  - downgrade attack
  - code signing verification
  - key pinning
  - subresource integrity
  - sri
  - import map integrity
  - c2pa
  - content credentials
  - scitt
  - transparency log
  - software supply chain consumer
  - update channel
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
  - T1195.002
  - T1574
framework_gaps:
  - NIST-800-53-SR-11
  - NIS2-Art21-network-security
  - UK-CAF-B4
  - AU-ISM-0298
cwe_refs:
  - CWE-494
  - CWE-829
  - CWE-353
  - CWE-347
last_threat_review: "2026-06-02"
---

# Consumer-Side Self-Update & Artifact Integrity

## Threat Context (mid-2026)

The self-update loop is the highest-privilege code path most products ship: it fetches code and runs it as the application. Publisher-side posture — code signing, SBOM, SLSA attestations — is necessary but useless if the receiving client does not enforce it. The consumer-side failures are an update applied without verifying a signature, a signature verified against a key the update channel itself supplied, a signed-but-older version accepted (downgrade / no anti-rollback) that re-opens a patched CVE, an update fetched over an unauthenticated channel as the sole control, browser modules served without Subresource Integrity, and an apply step that does not gate on the verifier result. A channel compromise (poisoned CDN, mirror, MITM) then yields arbitrary code execution across the installed base.

## Framework Lag Declaration

Organisational supply-chain controls focus on the publisher: signing, SBOM generation, SLSA build levels. NIST 800-53 SR-11 (component authenticity) covers the supplier side and does not require the consumer's update path to verify signatures against a pinned key before applying or to refuse downgrades. The EU Cyber Resilience Act mandates secure updates for products with digital elements, but conformance is commonly attested by "we ship signed updates" without verifying the receiving client enforces signature + anti-rollback + key-pin. A clean "updates are signed / SLSA-attested / SBOM-published" audit is therefore NON-EVIDENCE for consumer-side update integrity; it confirms publisher posture, not signature-before-apply, key pinning, anti-rollback, or verifier-gating on the receiving client.

## TTP Mapping

The consumer-side update failures map to MITRE ATT&CK: **T1195.002 (Supply Chain Compromise: Software Supply Chain)** for an update applied without signature verification, against an in-band key, over an unauthenticated channel, or as an unverified browser module / artifact; and **T1574 (Hijack Execution Flow)** for an apply step that swaps the new code into the execution path without gating on the verifier. The weakness classes are CWE-494 (Download of Code Without Integrity Check), CWE-829 (Inclusion of Functionality from an Untrusted Control Sphere), CWE-353 (Missing Support for Integrity Check — e.g. absent SRI), and CWE-347 (Improper Verification of Cryptographic Signature — in-band or unpinned key).

## Exploit Availability Matrix

These are consumer-side validation gaps exploited from a channel-influencing position, so the exploit is the absent check, not a published CVE. Serving a tampered update to a client that applies without signature verification requires only control of a mirror or an on-path position. A downgrade requires merely a genuinely-signed older release. Substituting a key when trust is in-band requires control of the same endpoint as the update. The real-world priority is driven by the breadth of the installed base reachable through the update channel and whether a single channel compromise yields mass arbitrary-code execution — historically the highest-impact supply-chain outcome.

## Analysis Procedure

1. Identify every self-updating client/agent and every consumer of externally-sourced executable artifacts (modules, models, signed bundles). 2. Confirm the update path verifies a signature over the artifact BEFORE applying (not a server-provided hash) and fails closed. 3. Confirm the verifying root key is pinned out-of-band (in the binary / OS trust store), not fetched alongside the update. 4. Confirm anti-rollback: the updater refuses a version lower than installed. 5. Confirm the channel is TLS-pinned (defence-in-depth behind the signature). 6. Confirm browser-served modules carry SRI and the import map is integrity-protected. 7. Confirm C2PA content credentials and SCITT/TSA receipts on received artifacts are verified where relied upon, and that the apply gates on the verifier. Run the `self-update-integrity` playbook to execute these as detect indicators with false-positive checks, then score by installed-base breadth.

## Output Format

Report per update path, marking each consumer-side control enforced / missing / inconclusive (visibility gap). For every missing control, state whether a channel compromise would yield arbitrary-code execution and across how much of the installed base. Distinguish a control delegated to a verifying mechanism (OS package manager, gated verifier) from an absent one. Provide the prioritised remediation (verify signature against a pinned key before apply, enforce anti-rollback, pin the channel, enforce SRI on modules, verify provenance/transparency) and the negative validation tests that prove each fix (tampered update rejected, downgrade rejected, verifier-failure blocks apply) plus a functional test that a legitimate newer update still verifies and applies.

## Compliance Theater Check

The recurring theater is "our updates are signed, so the channel is secure," "updates come over HTTPS, so they cannot be tampered," and "we have an update verifier." Signing is the publisher side; HTTPS authenticates a CA bundle and falls to a mis-issued cert; a verifier whose output does not gate the apply is decorative. The distinguishing test: verify the client checks the signature against an out-of-band-pinned key before applying, refuses older versions, and blocks the apply on verifier failure. If a swapped artifact, an attacker-supplied key, or an older signed version would be applied, the signing did not protect the consumer and the assurance is paper.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: signature-before-apply with an out-of-band-pinned key realises Executable Allowlisting and Cryptographic Verification (countering T1195.002); anti-rollback realises Software Version Pinning (countering downgrade reintroduction); channel pinning realises Certificate Pinning; Subresource Integrity realises Resource Integrity Checking on browser modules; verifier-gating realises Execution Flow Integrity (countering T1574). Pair the signature check with provenance (C2PA) and transparency (SCITT/TSA) verification for non-repudiation. The residual risk after consumer-side enforcement is compromise of the publisher's signing key or build pipeline itself, which yields a validly-signed malicious update — addressed publisher-side (supply-chain-integrity) and accepted at the CISO level with key-management oversight.
