---
name: pqc-first
version: "1.0.0"
description: Post-quantum cryptography first mentality — hard version gates (OpenSSL 3.5+), algorithm sunset tracking, HNDL assessment, loopback learning for NIST/IETF standards evolution
triggers:
  - pqc
  - post-quantum
  - quantum cryptography
  - quantum safe
  - ml-kem
  - ml-dsa
  - slh-dsa
  - harvest now decrypt later
  - quantum migration
  - crypto migration
  - openssl pqc
  - fips 203
  - fips 204
  - fips 205
data_deps:
  - atlas-ttps.json
  - exploit-availability.json
  - global-frameworks.json
  - rfc-references.json
atlas_refs: []
attack_refs: []
framework_gaps:
  - NIST-800-53-SC-8
  - NIST-800-53-SC-28
rfc_refs:
  - RFC-8446
  - DRAFT-IETF-TLS-ECDHE-MLKEM
  - DRAFT-IETF-TLS-HYBRID-DESIGN
  - RFC-9180
  - RFC-9420
  - RFC-9794
  - RFC-9954
  - RFC-8032
  - RFC-9106
forward_watch:
  - NIST FIPS 206 (HQC — backup KEM)
  - NIST SP 800-208 (stateful hash-based signatures — LMS/XMSS)
  - IETF RFC for ML-KEM in TLS 1.3 (draft-connolly-tls-mlkem-key-agreement)
  - IETF RFC for hybrid X25519+ML-KEM (RFC 9180 extension)
  - OpenSSL 3.5 default algorithm changes
  - CISA PQC Migration Project timelines
  - NSA CNSS advisory updates (Commercial National Security Algorithm Suite 2.0)
  - EU ENISA PQC transition timeline updates
  - Browser TLS negotiation support for ML-KEM (Chrome, Firefox milestones)
  - HSM/TPM vendor PQC firmware support timelines
  - New CRQC timeline estimates from academic cryptanalysis
cwe_refs:
  - CWE-327
d3fend_refs:
  - D3-FE
  - D3-MENCR
last_threat_review: "2026-08-05"
---

# PQC-First Mentality

## Threat Context (mid-2026)

The post-quantum migration is not a planning exercise. It is an operational deadline against an adversary that is already collecting ciphertext.

**Standards state as of mid-2026:**
- **FIPS 203 (ML-KEM)** — finalized 2024-08-13. Module-Lattice KEM. Production-ready.
- **FIPS 204 (ML-DSA)** — finalized 2024-08-13. Module-Lattice signature. Production-ready.
- **FIPS 205 (SLH-DSA)** — finalized 2024-08-13. Stateless hash-based signature. Production-ready.
- **FIPS 206 (HQC)** — still pending. Hamming Quasi-Cyclic backup KEM. Expected finalization 2026–2027.
- **NIST SP 800-227** (ML-KEM implementation guidance) — draft, finalization tracked.

**CRQC timeline pressure has tightened:**
- **NSA CNSA 2.0** mandates PQC for National Security Systems by 2030. This deadline is not aspirational — it is binding for NSS vendors and rolling forward through the federal supply chain.
- **US OMB M-23-02** requires federal agencies to maintain a PQC migration inventory and timeline. Inventory compliance is being audited; migration progress is the next reporting cycle.
- **EU ENISA** PQC transition mandate is progressing toward binding Member State implementation timelines; commercial entities operating in EU jurisdictions should treat 2027–2028 as the alignment window.
- Academic CRQC estimates have shortened. Aggressive estimates of 5–8 years (from mid-2026) now appear in peer-reviewed cryptanalysis literature, not only opinion pieces.

**Harvest-now-decrypt-later (HNDL) is the active threat surface:**
- Adversaries are recording encrypted traffic today. State-level adversaries have been doing this since at least 2013 (public knowledge); the scale has expanded with cheaper storage.
- Any data with a sensitivity window of 10+ years that is currently protected only by classical asymmetric cryptography must be treated as **already-compromised on the CRQC date**. The encryption-at-rest archive built in 2026 with RSA-2048 key-wrapping is decryptable in the 2030s by a state-level adversary that captured the keys today.
- HNDL is not theoretical — the operational decision is whether to accept the loss when CRQC arrives or to migrate the cryptographic envelope now while migration is possible at planned-change pace rather than incident-response pace.

**OpenSSL 3.5+ hard version gate (April 2025 release):**
- Ships ML-KEM, ML-DSA, and SLH-DSA in the stable mainline. The "PQC isn't available in production tooling" excuse is retired as of April 2025.
- Hybrid TLS key agreement (X25519MLKEM768) is the operational migration path — not a research mode.

---

## Framework Lag Declaration

PQC migration exposes a framework class lag: every major commercial framework defines cryptographic requirements algorithm-agnostically ("strong cryptography", "appropriate cryptographic mechanisms"), which means none of them mandate PQC explicitly even though the threat model has shifted.

| Framework | Control | What It Misses for PQC Migration |
|---|---|---|
| NIST 800-53 | SC-13 (Cryptographic Protection) | Requires "cryptographic mechanisms" with FIPS-validated algorithms. ML-KEM/ML-DSA/SLH-DSA are now FIPS-validated, but SC-13 does not require their selection over classical FIPS algorithms. An organization fully compliant with SC-13 today can be using exclusively RSA-2048 and ECDSA-P-256 and still pass audit — while leaving every long-sensitivity archive HNDL-vulnerable. |
| NIST 800-53 | SC-8 / SC-28 (Transmission / At-Rest Confidentiality) | Algorithm-neutral. No PQC requirement. |
| ISO 27001:2022 | A.8.24 (Use of Cryptography) | Algorithm-agnostic. Requires that cryptographic use be "appropriate" without defining what appropriate means against a CRQC threat model. An ISO-certified org with no PQC plan is fully compliant. |
| PCI DSS 4.0 | §4.2.1 (Strong Cryptography in Transit) | Defines "strong cryptography" by reference to NIST guidance that pre-dates FIPS 203/204/205 mandates. AES-128+ and RSA-2048+ satisfy the requirement. No PQC mandate. |
| NIS2 | Art. 21(2)(h) | Requires "policies on cryptography and, where appropriate, encryption". Silent on algorithm specifics, silent on PQC, silent on HNDL. "Appropriate" is left to the entity. |
| DORA | Art. 9 (ICT Security Measures) | Requires encryption commensurate with risk. Does not operationalize quantum risk. |
| EU CRA | Essential Requirements Annex I | References "appropriate cryptography for the level of risk". No PQC specifics. |
| HIPAA Security Rule | §164.312(a)(2)(iv), §164.312(e)(2)(ii) | Algorithm-neutral "addressable" encryption. No PQC mandate. PHI sensitivity windows routinely exceed 20 years. |
| CNSA 2.0 (US classified) | Algorithm Suite | **Does** mandate ML-KEM, ML-DSA, SLH-DSA for NSS by 2030. The only major framework with a hard PQC mandate as of mid-2026 — and it applies only to National Security Systems. Commercial frameworks have not yet aligned. |
| UK NCSC CAF | Principle B.4 (Cryptography) | Recommends following NCSC guidance which now references PQC transition planning, but the CAF principle itself is outcome-based and does not mandate PQC. |
| AU ISM | Control 0467 (Cryptographic Equipment and Algorithms) | References ASD-Approved Cryptographic Algorithms (AACAs). AACA list does not yet require PQC for non-classified data. |
| ISO 27001:2022 | A.8.10 (Information Deletion) | HNDL counterpoint: even where deletion is implemented, an adversary who captured the ciphertext before deletion still possesses the encrypted record. Framework has no concept of "ciphertext exfiltration during transmission" as a deletion-defeating event. |

**Net effect:** an organization can be fully compliant with NIST 800-53, ISO 27001:2022, PCI DSS 4.0, NIS2, DORA, HIPAA, and SOC 2 simultaneously while having zero PQC deployment and a 30-year HNDL exposure window. Compliance is not protection in this control class.

### Expanded jurisdictional coverage (per `data/global-frameworks.json`)

Sovereign-cyber programs outside the EU/UK/AU/ISO axis are producing the most concrete PQC migration signals as of mid-2026; the cross-walk below is required for any cryptographic-control gap analysis:

- **Israel (INCD Cyber Defense Methodology v2.0 + NCD PQC guidance):** Israel's National Cyber Directorate has published PQC migration guidance for critical-infrastructure operators emphasising hybrid X25519+ML-KEM-768 as the operational TLS profile and ML-DSA for code signing in defence-industry supply chains. The INCD baseline is one of the few national methodologies that explicitly names FIPS 203/204/205 algorithms.
- **Switzerland (FINMA Circular 2023/1 + FADP):** FINMA's operational-resilience expectations for banks include crypto-agility as a named capability; FADP Art. 8 (data security) is interpreted by the FDPIC to require migration planning for long-sensitivity-window data — HNDL is recognised in supervisory dialogues, not yet in binding guidance.
- **Japan (PPC + NISC + FISC):** NISC's PQC migration roadmap (CRYPTREC-aligned) tracks NIST FIPS 203/204/205 and projects a 2030–2031 migration horizon for government systems. FISC Security Guidelines apply CRYPTREC algorithm recommendations to the financial sector; PPC interprets APPI safeguards as evolving with cryptographic state of the art.
- **South Korea (NIS / KISA + KCMVP):** KISA's KCMVP scheme is the Korean analogue to FIPS 140-3 and is mid-transition to incorporate KpqC (Korean PQC) candidates alongside NIST FIPS 203/204/205. Dual-algorithm requirements for export-sensitive products are emerging.
- **China (OSCCA / SCA + CSL):** OSCCA-mandated algorithms (SM2/SM3/SM4/SM9) are evolving toward post-quantum variants under the Chinese cryptographic standards process. Operators bridging CN and ISO/NIST regimes face a parallel-stack migration problem, not a single-stack one.
- **Hong Kong (HKMA TM-E-1 / SA-2):** HKMA expects authorized institutions to maintain crypto-inventory and to track PQC migration timelines as part of operational resilience. No hard mandate, but supervisory dialogues are active.
- **Taiwan (Cyber Security Management Act + TaiCS PQC roadmap):** CSMA-classified A/B/C CII operators are subject to TaiCS-published PQC migration milestones with sector-specific guidance from the FSC (financial) and BoE (energy).
- **Indonesia (UU PDP + BSSN):** BSSN cryptographic guidance references NIST FIPS publications; UU PDP Art. 35 (security obligations) is interpreted to evolve with cryptographic state of the art.
- **Vietnam (Cybersecurity Law + Decree 53):** Cryptographic-product certification under Decree 53 includes a parallel-stack expectation for systems handling "important data"; PQC migration is not yet mandated but is on the BCY (Government Cipher Committee) roadmap.
- **Brazil (LGPD + ANPD):** ANPD has signalled that "state-of-the-art" technical measures under LGPD Art. 46 will include PQC consideration for long-sensitivity-window data; no hard mandate yet.
- **US sub-national — NYDFS 23 NYCRR 500.15:** Encryption-of-nonpublic-information requirement is algorithm-agnostic but recently amended (Nov 2023) to require periodic CISO review of cryptographic controls — operationally this is the hook for PQC inclusion in covered entities' annual review cycles, ahead of any federal mandate beyond CNSA 2.0.

PQC migration is the clearest example of why a global-first lens matters: the lag is not uniformly distributed — INCD, KISA, and BSI/ANSSI guidance leads, while many compliance-framework controls still treat algorithm choice as ungoverned.

### IETF Tracking — The IETF Lag IS the Framework Lag for PQC

FIPS 203/204/205 are NIST publications, but the operational PQC migration story is IETF-tracked. TLS 1.3 (RFC 8446) is not PQC-ready on its own; hybrid groups arrive via `draft-ietf-tls-ecdhe-mlkem` and the general hybrid-design framework, which was published as RFC 9954 (Informational, July 2026). `draft-ietf-tls-ecdhe-mlkem` — the Standards-Track profile that names the concrete groups — is still a draft; the two were never status-synchronized, so the construction being an RFC does not make the named groups standardised. HPKE (RFC 9180, classical-only today) is the substrate for TLS ECH and MLS (RFC 9420); PQC composition for HPKE is being worked at IETF CFRG. Terminology pins on RFC 9794 (Terminology for PQC, September 2025). EdDSA (RFC 8032) — what exceptd uses for skill integrity signing — is not PQC-safe; SLH-DSA / ML-DSA migration applies here too. Compliance frameworks (NIST 800-53 SC-13, ISO 27001:2022 A.8.24, PCI DSS 4.0 §4.2.1, NIS2 Art. 21) do not yet require any specific RFC or draft. CNSA 2.0 requires PQC migration by 2030 but does not specify which IETF profile. See `data/rfc-references.json` for the tracked entries.

---

## TTP Mapping

This skill addresses a **future-state attack class** that is not yet represented in `data/atlas-ttps.json` or in MITRE ATT&CK as of v15. CRQC-enabled record-and-decrypt is a known gap in the ATT&CK matrix — the framework currently has no technique that captures "adversary decrypts previously-captured ciphertext using a quantum cryptanalytic capability". This is intentionally called out: the skill's `atlas_refs` and `attack_refs` are empty arrays because no published TTP currently maps cleanly to the threat. Empty arrays here are not a stand-in for missing content — they are a deliberate gap flag.

| Technique Reference | Maps To PQC Threat? | Gap Description |
|---|---|---|
| MITRE ATT&CK T1557 (Adversary-in-the-Middle) | Partial — operational family | T1557 covers AitM credential capture and traffic interception. The capture half of HNDL falls into T1557 operationally; the later decrypt phase has no ATT&CK technique. |
| MITRE ATT&CK T1040 (Network Sniffing) | Partial — capture phase | Covers passive traffic capture. Does not cover the strategic-archive intent of HNDL, where the captured data has no immediate use and is stored for future decryption. |
| MITRE ATT&CK — "Cryptanalysis via CRQC" | **MISSING** | No technique presently captures CRQC-enabled decryption of previously-captured ciphertext. Known gap through ATT&CK v19.2 (May 2026). |
| MITRE ATLAS | **MISSING (out of scope)** | ATLAS scope is ML/AI system attacks. CRQC cryptanalysis is not in ATLAS scope. |
| CAPEC-114 (Authentication Abuse) | Indirect | Forged signatures via broken signature scheme would manifest as authentication abuse, but CAPEC does not enumerate "signature scheme broken by CRQC" as a precondition. |
| CAPEC-475 (Signature Spoofing by Improper Validation) | Indirect | Same — the post-CRQC equivalent has no CAPEC entry. |

**Gap flag (consumed by framework-gap-analysis skill):** The CRQC-decrypt threat class is a registered gap. When MITRE publishes an ATT&CK technique covering CRQC-enabled cryptanalysis, this skill's `attack_refs` and the TTP table above require update.

---

## Exploit Availability Matrix

| Dimension | Status | Detail |
|---|---|---|
| Public PoC available? | **Yes** | Every classical algorithm broken by Shor's algorithm has known PQC-on-classical-hardware research implementations. The mathematical attack is published; only the quantum hardware to run it at relevant scale is gated. Shor's algorithm itself has run on small problem instances on every major quantum hardware platform. |
| CISA KEV listed? | **N/A** | KEV tracks exploited software CVEs. Algorithm-class breaks do not appear in KEV by structure of the catalog. This is itself a framework gap — there is no equivalent KEV for "algorithm classes under active capture-and-store attack". |
| AI-accelerated? | **Yes** | AI-accelerated cryptanalysis on classical primitives is an active research domain in 2026. AI-discovered weakness in lattice problems is a forward-watch item; AI-acceleration of side-channel attacks on classical implementations during the migration window is already operational. |
| Active exploitation? | **Confirmed (capture phase)** | The HNDL capture phase is confirmed active across state-level adversaries and is publicly documented in threat-intelligence reporting. The decrypt phase awaits CRQC; the ciphertext is being accumulated now. |
| Live-patchable / fast migration? | **No** | Algorithm migration is months-to-years for any non-trivial cryptographic footprint. Rip-and-replace is not viable. Hybrid (X25519 + ML-KEM-768) is the operational migration path because it (a) preserves classical interop, (b) adds PQC security against HNDL immediately, and (c) lets the classical component be removed later once interop catches up. |
| Detection of HNDL in progress? | **No reliable detection** | Passive ciphertext capture is undetectable in transit. The only defense is to render the captured ciphertext valueless via PQC encryption before capture, or to ensure the data's sensitivity window expires before CRQC arrival. |
| Migration tooling maturity? | **Mature for libraries, immature for systems** | OpenSSL 3.5+, Go 1.23+, Rust ml-kem 0.3+, Bouncy Castle 1.78+ ship FIPS-aligned PQC. HSM/TPM vendor firmware support is uneven. Certificate authority PQC issuance is limited. PKI-wide migration is the hard part. |

**Cross-references:** `data/exploit-availability.json` tracks per-CVE PoC and KEV status with `last_verified` dates; algorithm-class threats use the matrix above because they do not map to a single CVE.

---

## Core Principle

Every cryptographic design decision defaults to post-quantum algorithms. Classical-only cryptography is a deprecated choice requiring explicit justification. The question is not "should we use PQC?" — the question is "what justifies not using PQC here?"

This is not paranoia. It is operational security grounded in:
1. Harvest-now-decrypt-later (HNDL) attacks are ongoing
2. NIST standardization is complete for three algorithms (FIPS 203/204/205)
3. Migration timelines for sensitive data exceed expected cryptographically relevant quantum computer (CRQC) arrival windows
4. OpenSSL 3.5+ ships PQC primitives in stable release; there is no longer a "PQC isn't available in standard tooling" excuse

---

## Version Gates — Non-Negotiable Minimums

These are hard version gates. Using older versions for new PQC-capable work is a drift error, not a trade-off.

### OpenSSL

```
Minimum version: OpenSSL 3.5.0 (released April 2025)
Why: First OpenSSL release with ML-KEM, ML-DSA, and SLH-DSA in the stable mainline
     Provider API for post-quantum algorithms
     FIPS 140-3 module certification in progress for 3.x branch

Rejected versions:
  OpenSSL 1.1.x: EOL, no PQC, security-only patches ended
  OpenSSL 3.0.x / 3.1.x / 3.2.x / 3.3.x: Pre-stable PQC; use only if 3.5 unavailable 
                                              with documented justification

Check:
  openssl version  # must be >= 3.5.0
  openssl list -key-managers | grep -i kem  # ML-KEM must appear
  openssl list -signature-algorithms | grep -i mldsa  # ML-DSA must appear
```

### liboqs / OQS Provider

```
Minimum: liboqs 0.11.0+ with OpenSSL OQS Provider 0.7.0+
Use case: Where OpenSSL 3.5 mainline PQC is insufficient (additional algorithm agility,
           experimental algorithms, research)
Note: OQS provider algorithms are NOT FIPS-certified. Use for hybrid modes with a 
      FIPS-certified classical component.
```

### BoringSSL (Google/Android)

```
Use Kyber768 (ML-KEM draft) hybrid mode: already deployed in Chrome since 2023
Post-FIPS-203 finalization: ML-KEM-768 via `SSL_CTX_set1_curves_list("X25519Kyber768Draft00:X25519")`
Note: BoringSSL follows Chrome's needs; track chromestatus.com for ML-KEM graduation
```

### Go

```
Minimum: Go 1.23+ (crypto/mlkem package added)
         Go 1.24+ (full ML-KEM-768 and ML-KEM-1024 in stdlib)
PQC TLS: crypto/tls supports X25519MLKEM768 key agreement in Go 1.23+
Check: go version  # must be >= 1.23
       grep mlkem go.sum  # if using crypto/mlkem directly
```

### Rust

```
Minimum: ml-kem crate 0.3.0+ (pure Rust FIPS 203 implementation)
         ml-dsa crate 0.1.0+
         rustls >= 0.23 with aws-lc-rs backend for PQC TLS
```

### Python

```
Minimum: cryptography >= 42.0.0 (PQC via OpenSSL 3.x bindings)
         pqcrypto >= 0.2.0 (pure-Python reference implementations — not production use)
For production: use cryptography library backed by OpenSSL 3.5+
```

### Java / JVM

```
Minimum: Bouncy Castle 1.78+ (ML-KEM, ML-DSA, SLH-DSA implementations)
         JDK 23 Preview / JDK 25+ (Module system PQC)
For enterprise: IBM JCE PQC provider or Bouncy Castle FIPS module
```

---

## Algorithm Registry

### Current NIST-Standardized Algorithms (Production Use)

| Algorithm | FIPS Standard | Purpose | Key Size | Notes |
|---|---|---|---|---|
| ML-KEM-512 | FIPS 203 | KEM (128-bit security) | 800B public key | Minimum — prefer ML-KEM-768 |
| ML-KEM-768 | FIPS 203 | KEM (192-bit security) | 1184B public key | Recommended baseline |
| ML-KEM-1024 | FIPS 203 | KEM (256-bit security) | 1568B public key | High-security, long-lived data |
| ML-DSA-44 | FIPS 204 | Signature (128-bit security) | 1312B public key | Minimum |
| ML-DSA-65 | FIPS 204 | Signature (192-bit security) | 1952B public key | Recommended baseline |
| ML-DSA-87 | FIPS 204 | Signature (256-bit security) | 2592B public key | High-security, code signing |
| SLH-DSA-SHAKE-128s | FIPS 205 | Hash-based signature (small) | 32B public key | Tamper-evident logs, audit chains |
| SLH-DSA-SHAKE-128f | FIPS 205 | Hash-based signature (fast) | 32B public key | Performance-sensitive signing |
| SLH-DSA-SHAKE-256f | FIPS 205 | Hash-based signature (high-sec) | 64B public key | Critical infrastructure, long-lived certs |

### Algorithm Selection Guide

```
Use ML-KEM-768 for:
  - TLS key exchange (X25519 + ML-KEM-768 hybrid)
  - Session key establishment
  - Symmetric key encapsulation
  - General-purpose KEM

Use ML-KEM-1024 for:
  - Long-lived key pairs (> 5 years)
  - Keys protecting data with > 20-year sensitivity
  - PQC envelope for secrets requiring harvest-now-decrypt-later protection

Use ML-DSA-65 for:
  - Code signing
  - Certificate signatures
  - API authentication signatures
  - JWT signing

Use SLH-DSA-SHAKE-256f for:
  - Tamper-evident audit chain checkpoints
  - Root certificates / trust anchors
  - Any signature that must remain valid for > 20 years

Never use standalone (non-hybrid) for new deployments:
  RSA (any key size), ECDH (P-256, P-384, X25519 standalone), ECDSA standalone
  These remain for: (1) compatibility with systems that cannot negotiate PQC, 
  (2) FIPS 140-2 environments pending FIPS 140-3 recertification
```

### Deprecated / Being Deprecated

| Algorithm | Status | Action Required |
|---|---|---|
| RSA-2048 | Deprecated for new use | Migrate to ML-DSA or hybrid. Existing: track rotation schedule. |
| RSA-4096 | Deprecated for new use (larger key doesn't help against quantum) | Same |
| P-256 / ECDSA-256 | Deprecated standalone for new use | Use as hybrid classical component only |
| P-384 / ECDSA-384 | Deprecated standalone for new use | Hybrid classical component |
| X25519 standalone | Deprecated for new key exchange | Use X25519 + ML-KEM-768 hybrid |
| AES-128 GCM | Reduce security margin post-quantum; prefer AES-256 or XChaCha20 | Migrate symmetric encryption to 256-bit |
| SHA-256 standalone | Reduce security margin post-quantum; prefer SHA3-256 or SHA-512 | Context-dependent migration |
| SHA-1, MD5 | Already broken, not quantum-related | Immediately remove |

### Classical Algorithms Retained as Hybrid Components

These algorithms remain in use as the classical component of hybrid constructions. They are not deprecated — they are downgraded from standalone to hybrid-required:

- P-384 (ECDH) — hybrid with ML-KEM (P-384 + ML-KEM-1024)
- X25519 — hybrid with ML-KEM-768 (X25519 + ML-KEM-768)
- AES-256-GCM — retained as symmetric cipher (unaffected by quantum)
- ChaCha20-Poly1305 / XChaCha20-Poly1305 — retained (unaffected by quantum)
- HMAC-SHA256/512 — retained for MAC (symmetric, quantum-safe with current key sizes)
- Argon2id — retained for password hashing (symmetric)

---

## Hybrid Construction Requirements

All new asymmetric cryptographic operations must use hybrid mode until PQC-only is validated in the deployment context.

### Hybrid KEM Standard

```
Hybrid KEM = CLASSICAL_KEM + ML-KEM
Shared secret = KDF(classical_secret || ml_kem_secret)

Recommended combinator: SHAKE256
  SS = SHAKE256(classical_SS || ml_kem_SS || context)
  where context = algorithm identifiers for both components

Baseline hybrid: X25519 + ML-KEM-768
High-security hybrid: P-384 + ML-KEM-1024
```

### Hybrid Signature Standard

```
Hybrid signature: Sign with ML-DSA AND classical algorithm (ECDSA/Ed25519)
Both signatures must verify for the message to be accepted.
Rationale: if one algorithm is broken (classical by quantum, PQC by classical cryptanalysis),
           the other component still provides security.

Use composite signature formats per IETF draft-ounsworth-pq-composite-sigs
```

### TLS Configuration

```
TLS 1.3 minimum (TLS 1.2 only for legacy compatibility with documented justification)
TLS 1.3 PQC key exchange:
  Preferred: X25519MLKEM768 (IETF RFC in progress, Chrome/Firefox supported)
  High-security: SecP256r1MLKEM768 (IETF draft)
  
OpenSSL 3.5 TLS config:
  SSL_CTX_set1_groups(ctx, "X25519MLKEM768:X25519:P-384");
```

---

## Harvest-Now-Decrypt-Later (HNDL) Threat Assessment

### What HNDL means operationally

An adversary captures encrypted traffic today and stores it. When a CRQC becomes available, they decrypt the stored ciphertext. The attack is retroactive — it works against today's captured traffic using tomorrow's quantum computer.

**Timeline assessment (mid-2026):**
- Conservative CRQC estimate: 10–15 years (NIST/NSA/CISA)
- Aggressive CRQC estimate: 5–8 years (some academic estimates)
- Best case: > 20 years (physical engineering optimism)

**Data sensitivity window:**
If data captured today must remain confidential for > N years, and CRQC arrives in < N years, HNDL is a real threat for that data.

| Data Type | Typical Sensitivity Window | HNDL Risk |
|---|---|---|
| Payment card numbers | 2–5 years | Low-Medium |
| Personal health information | 20+ years | High |
| Government classified | 25–50+ years | Critical |
| Corporate M&A / IP | 5–15 years | High |
| Long-lived API secrets | Until rotated | High if > 5 years |
| TLS session traffic | Session duration | Medium (protocol metadata) |
| Encrypted backup archives | Retention period | High if > 10 years |

### HNDL Assessment Procedure

1. Classify data by sensitivity window
2. For data with sensitivity window > 5 years: require ML-KEM-1024 or P-384 + ML-KEM-1024 hybrid for key exchange
3. For data with sensitivity window > 20 years: require additional review; consider forward-secret key exchange with hybrid PQC
4. For existing encrypted archives: assess re-encryption feasibility; document HNDL risk for archives that cannot be re-encrypted

---

## Loopback Learning — Standards Evolution Tracking

PQC standards change. This section is the explicit loopback mechanism: when tracked standards update, this skill must be reviewed and updated.

### What to monitor and when to trigger a skill update

| Source | What to watch | Update trigger |
|---|---|---|
| NIST PQC Project | New FIPS publications | FIPS 206 (HQC) finalization → add HQC to algorithm registry |
| NIST PQC Project | SP 800-227 (draft guidance for ML-KEM) | Finalization → update implementation guidance |
| IETF TLS WG | ML-KEM in TLS 1.3 RFC | RFC publication → update TLS configuration section |
| IETF LAMPS WG | Composite signatures RFC | RFC publication → update hybrid signature section |
| OpenSSL | 3.5+ point releases | Algorithm additions/changes → update version gate commentary |
| OpenSSL | FIPS 140-3 module for 3.x | Certification → update FIPS section |
| Chrome | ML-KEM TLS graduation | When ML-KEM becomes non-experimental → update browser compatibility |
| NSA CNSS | CNSA 2.0 timeline updates | New mandatory dates → update migration timeline section |
| CISA PQC | Migration project guidance | New sector-specific guidance → update compliance section |
| ENISA | EU PQC transition timeline | Publication → add to global-grc skill |
| Academic | CRQC timeline estimate changes | Major new estimate → update HNDL threat assessment |
| HSM vendors | PQC firmware support | Availability → update HSM section |

### Forward Watch Items (Tracked)

The following are in active standards development as of mid-2026. When they finalize, this skill requires update:

**HQC (Hamming Quasi-Cyclic):**
- Status: NIST Round 4 finalist (backup KEM to ML-KEM)
- Finalization: expected 2026–2027 as FIPS 206
- Action on finalization: add HQC to algorithm registry, note as backup KEM when ML-KEM performance is constrained

**XMSS / LMS (Stateful hash-based signatures):**
- Status: NIST SP 800-208 already published
- Note: Stateful — state management is critical; not suitable for most use cases. Add warning section on state management requirements.

**X25519 + ML-KEM-768 hybrid in TLS:**
- Status: IETF draft-connolly-tls-mlkem-key-agreement
- Chrome/Firefox: deployed in production since 2024 (Kyber768 draft), upgrading to final ML-KEM
- Action on RFC publication: update TLS configuration from "in progress" to "standard"

**FIPS 140-3 for OpenSSL 3.x:**
- Status: CMVP testing in progress
- Action on certification: update version gate to recommend FIPS module explicitly

---

## Framework Coverage

### What frameworks require for PQC

| Framework | PQC Requirement | Assessment |
|---|---|---|
| NIST 800-53 SC-8, SC-28 | "Employ cryptographic mechanisms" — algorithm-neutral | Adequate in intent; "appropriate" now includes PQC consideration |
| NSA CNSA 2.0 | Mandates ML-KEM, ML-DSA, SLH-DSA for National Security Systems | Strongest mandate; applies to NSS only |
| CISA PQC Guidance | Strong recommendation for all critical infrastructure | Non-binding but authoritative |
| EU ENISA | PQC migration recommended; no hard mandate yet | Track for 2027 timeline |
| ISO 27001:2022 | A.8.24 (Use of cryptography): "appropriate" — algorithm-neutral | Requires interpretation to include PQC consideration |
| PCI DSS 4.0 | Requirement 4: "strong cryptography" — currently defined as AES-128+, RSA-2048+ | Does not yet mandate PQC; will require update |
| HIPAA | "appropriate" standard — algorithm-neutral | Same as ISO interpretation |
| NIS2 Art. 21(2)(h) | "policies on cryptography and, where appropriate, encryption" | No PQC mandate but "appropriate policies" implies current standard |

**Key takeaway:** No major framework mandates PQC migration with hard timelines yet (except CNSA 2.0 for NSS). However, "appropriate" and "strong" cryptography requirements will be interpreted to require PQC as the standards mature and CRQC timelines tighten.

**Proactive migration now is operationally superior** to reactive migration under regulatory pressure — because migration timelines for complex cryptographic infrastructure typically exceed 2–5 years.

---

## Analysis Procedure

### Step 1: Inventory cryptographic usage

For the target system:
- List all asymmetric algorithms in use (key exchange, signatures, certificates)
- List all symmetric algorithms in use (encryption, MACs)
- List all hash functions in use
- Note: protocol (TLS, SSH, S/MIME, PGP, JOSE/JWT, etc.)
- Note: library + version for each usage

### Step 2: Apply version gates

For each library:
- OpenSSL: is version >= 3.5.0?
- Go: is version >= 1.23?
- Others: per version gate table above

### Step 3: Classify algorithms

For each algorithm in use:
- Quantum-safe (ML-KEM, ML-DSA, SLH-DSA, AES-256, XChaCha20, Argon2id, HMAC-SHA512, SHA3)
- Classical-OK-as-hybrid-component (X25519, P-384, AES-256-GCM, ChaCha20-Poly1305)
- Deprecated for new use (RSA, standalone X25519, P-256 standalone)
- Already broken (SHA-1, MD5, DES)

### Step 4: Assess HNDL exposure

For each data type protected by the cryptographic system:
- What is the sensitivity window?
- Is the key exchange quantum-safe or hybrid?
- What is the HNDL risk?

### Step 5: Generate migration plan

Priority order:
1. Long-lived key pairs protecting sensitive data (immediate migration to PQC hybrid)
2. TLS for systems handling long-sensitivity-window data (X25519 + ML-KEM-768 hybrid)
3. Certificate infrastructure (ML-DSA-65 or hybrid for code signing, root CAs)
4. Symmetric key sizes (ensure AES-256 throughout, not AES-128)
5. Hash function migration (SHA3 for new uses, SHA-256 is acceptable short-term)

---

## Output Format

The skill produces a structured PQC Readiness Assessment that scores the org's post-quantum migration posture against the NIST PQC standards (ML-KEM / FIPS 203, ML-DSA / FIPS 204, SLH-DSA / FIPS 205), CNSA 2.0, and the BSI / ANSSI / NCSC migration guidance. The shape below is consumed downstream by `crypto` playbook runs (which feed the assessment into the analysis correlation step), by `framework-gap-analysis` (for SC-8 / SC-13 / A.8.24 / A.10 lag declarations), and by `compliance-theater` (which compares the harvest-now-decrypt-later exposure against the org's data-classification claims). Preserve the per-protocol cryptographic-inventory rows verbatim — they are the auditable derivation of the migration roadmap.

```
## PQC Readiness Assessment

**Date:** YYYY-MM-DD
**OpenSSL version:** [X.X.X] — [Pass ≥3.5.0 / FAIL]

### Algorithm Inventory
| Usage | Current Algorithm | PQC Status | Version Gate | Migration Required |
|---|---|---|---|---|

### HNDL Exposure
| Data Type | Sensitivity Window | Key Exchange | HNDL Risk | Action |
|---|---|---|---|---|

### Version Gate Compliance
[Per library: pass/fail with specific version found]

### Migration Roadmap
[Priority-ordered, specific to this system's algorithm inventory]

### Forward Watch Status
[Which tracked standards have updated since last review; which skill sections need updating]

### Framework Compliance
[Per applicable framework: PQC requirement, current status, gap if any]
```

---

## Defensive Countermeasure Mapping

D3FEND references from `data/d3fend-catalog.json`. The harvest-now-decrypt-later (HNDL) threat has two capture surfaces — data in transit and data at rest — and each maps to a distinct D3FEND hardening technique. The capture itself is conventional; it is the *future decryption* that has no ATT&CK or D3FEND coverage. The countermeasure is therefore not "detect the capture" but "make the captured ciphertext worthless to a future CRQC."

| D3FEND ID | Name | Layer | Rationale (what it counters here) |
|---|---|---|---|
| `D3-MENCR` | Message Encryption | Transit (TLS / application) | Counters in-flight HNDL capture (T1040 Network Sniffing, T1557 Adversary-in-the-Middle — the same techniques the TTP Mapping above flags as the HNDL capture half). Only PQC-hybrid key exchange (ML-KEM-768 + X25519, per the TLS Configuration section) makes today's captured session ciphertext non-decryptable post-CRQC. Classical-only TLS is HNDL-exposed even when otherwise correctly configured. |
| `D3-FE` | File Encryption | At-rest (storage) | Counters HNDL on stolen or copied storage (T1005 Data from Local System, T1565.001 Stored Data Manipulation). The trap: AES-256 at rest is quantum-resilient (Grover only halves the effective key length), but the DEK→KEK key-wrapping step is usually RSA/ECC and therefore HNDL-exposed. The control is incomplete unless the envelope KEM is ML-KEM-based or the wrapped key is itself 256-bit symmetric. |

**Framework gap — signature forgery has no D3FEND technique.** The third PQC threat — a CRQC forging RSA/ECDSA signatures (code-signing, certificate, document) — maps to no D3FEND hardening technique and no ATT&CK technique (see the TTP Mapping table). D3FEND's encryption families harden confidentiality, not authenticity. The only countermeasure is migrating signature schemes to ML-DSA / SLH-DSA per the Hybrid Signature Standard; there is no detection-layer fallback, which is why the version gates are non-negotiable minimums rather than defense-in-depth options.

**Defense-in-depth posture:** `D3-MENCR` and `D3-FE` are independent layers (transit vs. at-rest) and both are required — encrypting the wire while leaving model weights wrapped under RSA, or the reverse, leaves an HNDL surface open. Neither D3FEND technique expresses *algorithm strength*; the PQC-specific minimum (hybrid KEM, ML-KEM-768 floor) is the layer the taxonomy omits, which is the framework lag this skill exists to close.

**Least-privilege scope:** key-management authority is scoped to the migration roadmap — DEK/KEK rotation to PQC-hybrid wrapping is an operation a narrow KMS-admin identity performs, not a blanket "re-encrypt everything" grant. At-rest re-wrapping (`D3-FE`) is staged by data-sensitivity-window so the longest-lived secrets migrate first.

**Zero-trust posture:** every session negotiates PQC-hybrid key exchange regardless of network trust level — there is no "internal traffic is safe from HNDL" exemption, because a passive collector on an internal span harvests ciphertext as readily as one on the public path. Confidentiality is asserted per-session at the crypto layer, not inferred from network position.

**AI-pipeline applicability (some controls shift when workloads are ephemeral and never persist state):** `D3-FE` applies to model-weight files, training datasets, and embedding stores at rest; for ephemeral inference workloads that never persist state locally, the control shifts to PQC-hybrid-wrapped object storage (e.g. SSE-KMS with an ML-KEM-based envelope) rather than local-disk encryption. `D3-MENCR` applies to all AI-API traffic, which must move to TLS 1.3 with hybrid key exchange on the CNSA 2.0 timeline — noting that PQC protects the confidentiality of that traffic but not its content-layer abuse as a covert channel (pair with the AI-C2 egress controls in `ai-c2-detection`).

---

## Compliance Theater Check

> "Your cryptographic policy references 'strong cryptography' per [PCI DSS / HIPAA / ISO 27001]. Locate the policy definition of 'strong cryptography' and check when it was last updated. If 'strong cryptography' is defined as 'AES-128 or better, RSA-2048 or better' without reference to post-quantum algorithms: the policy is based on NIST guidance from before FIPS 203/204/205 finalization (August 2024). For any data with a sensitivity window exceeding 5 years, 'strong cryptography' as currently defined does not protect against harvest-now-decrypt-later adversaries. The policy is theater for the threat it claims to address."
