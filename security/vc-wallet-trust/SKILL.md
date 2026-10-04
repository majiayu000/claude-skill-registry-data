---
name: vc-wallet-trust
version: "1.0.0"
description: Verifiable-credential / digital-wallet verifier trust for mid-2026 — SD-JWT-VC, OID4VCI/OID4VP, mdoc (ISO 18013-5), DID resolution, OAuth Token Status List revocation, OpenID Federation trust anchors, and the EUDI wallet (eIDAS 2.0) acceptance path
triggers:
  - verifiable credential
  - digital wallet
  - sd-jwt-vc
  - oid4vp
  - oid4vci
  - mdoc
  - mdl
  - iso 18013-5
  - eudi wallet
  - eidas 2.0
  - did:web
  - status list
  - credential revocation
  - openid federation
  - trust anchor
  - credential verifier
  - presentation exchange
  - dcql
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
  - T1556
  - T1606
  - T1550
framework_gaps:
  - NIST-800-63B-rev4
  - NIST-800-53-IA-5-Federated
  - ISO-27001-2022-A.5.16-Federated
  - NIS2-Art-21-Federated-Identity
  - UK-CAF-B2
cwe_refs:
  - CWE-347
  - CWE-290
  - CWE-863
  - CWE-200
  - CWE-672
last_threat_review: "2026-06-02"
---

# Verifiable-Credential / Digital-Wallet Verifier Trust

## Threat Context (mid-2026)

A credential verifier is a trust boundary: every verifiable credential it accepts grants whatever the credential asserts — age, residency, employment, professional licence, payment authority. With the EU Digital Identity Wallet (eIDAS 2.0) rolling out and ISO 18013-5 mobile driving licences in production, verifiers across payments, age-gating, and onboarding now accept SD-JWT-VC, OID4VP, and mdoc presentations from wallets they do not control. The dominant abuse is not breaking the cryptography but exploiting a missing trust check: an issuer key the verifier never pinned to an anchor, a revocation status it never read, a presentation it never bound to a fresh challenge, or a device signature it never verified. Each lets an attacker present a forged, revoked, or replayed credential that the verifier treats as authentic.

## Framework Lag Declaration

Organisational identity controls were written for service-to-service and human-credential authentication and are silent on the verifiable-credential acceptance path. NIST 800-53 IA-9 (service identification) and IA-5 (authenticator management) do not require credential issuer trust-anchor pinning or presentation replay-binding. ISO 27001:2022 A.5.16 governs the lifecycle of internal identities, not the trust model for externally-issued credentials a verifier accepts. NIS2 Art.21 names supply-chain trust of entities but not the cryptographic anchor model for the credentials those entities present. A clean identity-control audit is therefore NON-EVIDENCE for verifier trust posture; the controls predate the wallet ecosystem and do not exercise it.

## TTP Mapping

The verifier-trust failure modes map to MITRE ATT&CK: **T1606 (Forge Web Credentials)** for accepting a credential from an unanchored or algorithm-substituted issuer key; **T1556 (Modify Authentication Process)** for trusting an unpinned did:web document, an unverified key attestation, or an unanchored federation chain; and **T1550 (Use Alternate Authentication Material)** for replaying a presentation that lacks nonce/audience binding, replaying issuer-signed mdoc data without device-auth, or presenting a revoked credential whose status was never checked. The weakness classes are CWE-347 (improper signature verification), CWE-290 (authentication bypass by spoofing), CWE-672 (operation on a resource after expiration/revocation), CWE-863 (incorrect authorization), and CWE-200 (over-disclosure of personal claims).

## Exploit Availability Matrix

These are configuration and code-posture gaps, not single-CVE exploits, so weaponisation cost is low and reusable. Forging an unanchored issuer requires only standing up an OID4VCI issuer or serving a crafted did:web document — commodity tooling. Replaying an unbound presentation requires capturing one valid presentation and resubmitting it. Presenting a revoked credential requires nothing beyond holding a credential whose authorisation was withdrawn. Algorithm-substitution requires the verifier library to accept an unexpected alg. None require a published CVE; the exploit is the absence of the check. Real-world priority is driven by reachability (internet-facing verifier) and the value of the entitlement the credential gates, not by a CVSS score.

## Analysis Procedure

1. Inventory every service that ACCEPTS credentials (issuer-only services are out of scope for the verifier checks). 2. For each accepted format (SD-JWT-VC, OID4VP, mdoc, DID-identified), read the verifier accept-path and answer: is the issuer key validated against a pinned trust anchor or issuer allowlist? 3. Is the revocation / status-list resolved and enforced fail-closed? 4. Are presentations bound to a fresh verifier-issued nonce and audience (key-binding required, device-auth verified for mdoc)? 5. Is an explicit signature-algorithm allowlist enforced with "none" and unexpected symmetric algorithms refused? 6. Are disclosed claims filtered to the requested query (no over-disclosure)? Run the `vc-wallet-trust` playbook to execute these as detect indicators with false-positive checks, then score by reachability and entitlement value.

## Output Format

Report per accepted credential format, listing each trust check as enforced / missing / inconclusive (visibility gap). For every missing check, state the credential types and downstream entitlements it gates, whether the verifier is internet-facing, and the resulting blast radius. Distinguish a production-reachable gap from a test-only resolver. Provide the prioritised remediation (pin issuer anchors, enforce revocation fail-closed, bind presentations to nonce+audience, verify mdoc device-auth, enforce an algorithm allowlist, filter to requested claims) and the negative validation tests that prove each fix (forged-issuer rejected, revoked rejected, replayed rejected) plus the positive test that the legitimate path still accepts.

## Compliance Theater Check

The recurring theater is "we accept a certified wallet, so acceptance is trustworthy" and "the signature verified, so the credential is trusted." Wallet certification covers the wallet, not the verifier; a valid signature only proves some key signed the credential, not that the issuer is authentic. The distinguishing test: ask for the verifier's trust-anchor / issuer-allowlist configuration, the revocation check on the accept path, and the presentation nonce/audience binding. If acceptance succeeds against an unpinned issuer key, a never-read status list, or an unbound presentation, the assurance is paper. "Our credentials support a status list" is theater unless the verifier accept-path actually fetches and enforces it.

## Defensive Countermeasure Mapping

Map findings to MITRE D3FEND: trust-anchor pinning and issuer-allowlist validation realise Credential Hardening and Certificate Pinning (countering T1606/T1556); presentation nonce/audience binding and mdoc device-auth verification realise Authentication Event Thresholding and Message Authentication (countering T1550 replay); fail-closed revocation enforcement realises Credential Revoking. Pair the verifier checks with issuer key-rotation monitoring and a fast anchor-revocation path so a compromised-but-trusted issuer can be removed quickly. The residual risk after pinning is a trusted issuer's own key compromise, which trust-anchor pinning does not address — accept it at the CISO level with compensating issuer-key monitoring.
