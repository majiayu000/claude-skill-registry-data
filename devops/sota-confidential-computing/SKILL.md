---
name: sota-confidential-computing
description: >-
  State-of-the-art confidential computing and cryptographic PETs (2026) for
  BUILDING and AUDITING systems that protect workloads and data in use from
  the infrastructure they run on — the inverse of sandboxing. Covers TEE
  selection (AMD SEV-SNP, Intel TDX, ARM CCA realms, SGX enclaves, AWS Nitro
  Enclaves, NVIDIA confidential GPUs), memory encryption vs attested isolation
  (TME/TME-MK/MKTME), remote attestation (RATS RFC 9334, evidence appraisal,
  attest-then-release, RA-TLS, TCB recovery), confidential VMs/nodes/pods on
  Kubernetes (Confidential Containers/CoCo, Kata, Trustee KBS), and computing
  on encrypted data without hardware trust — FHE, MPC/threshold, ZKP,
  PSI/OPRF. Trigger keywords: confidential computing, TEE, enclave, SEV-SNP,
  TDX, ARM CCA, SGX, Nitro Enclaves, confidential VM, remote attestation,
  attestation report, KBS, CoCo, Kata, Trustee, MKTME, confidential GPU, FHE,
  homomorphic encryption, MPC, ZKP, zero-knowledge, PSI, data in use, COED.
---

# SOTA Confidential Computing & PETs

## Purpose

Engineer and audit systems where the *infrastructure itself* is the adversary:
the cloud operator, the hypervisor, the node admin, a co-tenant, or anyone
with physical access to memory. Two tool families, one skill: hardware TEEs
with remote attestation (trust silicon + verify it), and cryptographic PETs
that compute on encrypted data (trust only math, pay orders of magnitude for
it). The boundary with `sota-sandboxing` is direction: sandboxing protects the
host from the workload; this skill protects the workload from the host. Both
can apply to the same system.

Two modes. Pick one explicitly at the start of the task.

---

## BUILD mode

Use when designing or implementing confidentiality-in-use for new or changed
systems.

1. **Name the adversary first** (`rules/01` §2, §7): operator, hypervisor,
   co-tenant, physical, or "the other party in a joint computation". If no
   adversary survives scrutiny, stop — TLS + at-rest encryption + KMS custody
   (`sota-secrets-management`) already covers you.
2. **Pick the lowest sufficient rung** of the escalation ladder (`rules/01`
   §4): transport/at-rest → HSM/KMS → confidential VM → process enclave →
   PET. Write the rung and its rationale into the design doc.
3. **Choose the TEE technology** from the selection table (`rules/02` §7) by
   workload shape (lift-and-shift VM, container, process, GPU inference) —
   using the latest stable platform generation; verify current provider
   support at design time.
4. **Design attestation before deployment** (`rules/03`): what evidence, who
   verifies (hosted vs self-hosted), what policy, and — decisive — what the
   attestation result *gates* (key release, secret injection, channel
   establishment). Attestation that gates nothing is decoration.
5. **On Kubernetes**, pick the layer deliberately (`rules/04` §1, §6):
   confidential nodes (operator excluded, cluster admin not) vs confidential
   pods/CoCo (both excluded); route secrets through attest-then-release (KBS),
   not K8s Secrets; plan the degraded debugging story up front.
6. **If hardware trust is unacceptable**, triage PETs (`rules/05`): most "we
   need FHE" asks are a TEE or differential-privacy problem in disguise;
   when a PET is right, use standard parameter sets and vetted libraries
   (latest stable) only.
7. **Document the honest limits** (`rules/01` §2, `rules/02` §6, `rules/04`
   §7): side channels, availability (never protected — the host can always
   kill you), and the TEE vendor in the TCB.

Deliverables: named adversary + chosen rung, TEE/PET selection with
rationale, the attestation flow diagram (RATS roles) and what it gates,
verification policy (debug-mode rejection, TCB handling, freshness), and the
residual-risk list.

## AUDIT mode

Use when reviewing systems that claim confidential computing, or that should.

Procedure: inventory data-in-use exposure (what runs where, who operates it)
→ check claims against the definition (`rules/01` §1: attested, hardware-based
TEE — or it isn't CC) → walk the attestation chain end to end (`rules/03`:
does anything consume the result? debug mode rejected? TCB current? nonce
fresh?) → on K8s, verify the layer matches the threat claim (`rules/04`) →
for PETs, verify parameters/libraries/threat models (`rules/05`) → run every
loaded rules file's audit checklist.

**Severity conventions**
- **Critical** — "confidential" claim with no attestation or attestation that
  gates nothing; debug-mode TEE accepted in prod; secrets delivered via a
  channel the excluded party controls (e.g. K8s Secrets to a CoCo pod);
  hand-rolled FHE/ZKP parameters or circuits.
- **High** — plain SEV/SEV-ES where SNP-class integrity is required; evidence
  verified without chain-to-vendor-root or TCB check; no re-attestation or
  reference-value rotation plan (TCB recovery will break prod); confidential
  nodes sold as protection against the cluster admin.
- **Medium** — stale/undocumented side-channel posture (SMT, ciphertext side
  channels); attestation results not monitored as security signals; missing
  in-guest storage encryption for confidential pods.
- **Low** — hygiene: undocumented residual risks, missing break-glass debug
  policy, PET performance assumptions unbenchmarked.

**Finding format**: `file:line | rule | severity | effort | fix` (canonical
cross-domain format from the router).

---

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-threat-model-and-selection.md` | deciding whether confidential computing is warranted at all: the CCC definition test (memory encryption alone ≠ CC), what CC does/never protects against, inverse-of-sandboxing framing, the five-rung escalation ladder, legitimate drivers, anti-patterns, adversary→mechanism decision table. Read first in every engagement. |
| `rules/02-tee-technologies.md` | choosing or judging TEE hardware: SEV→SEV-ES→SEV-SNP insufficiency ladder, TDX on TME/TME-MK (encryption vs integrity vs attestation test), ARM CCA status, SGX enclaves + LibOS reality, Nitro Enclaves' different trust model, NVIDIA confidential GPUs for AI, Wasm-in-TEE, side-channel/physical-attack posture, workload-shape selection table. |
| `rules/03-remote-attestation.md` | designing or auditing the trust mechanism: RATS (RFC 9334) roles mapped to real products, attest-then-release as the enforcement pattern, evidence hard rules (debug mode, cert chain, TCB status, nonce freshness), hosted vs self-hosted verifiers, reference-value management and TCB recovery, RA-TLS, re-attestation and monitoring. |
| `rules/04-confidential-kubernetes.md` | running confidential workloads on K8s: confidential nodes vs confidential pods (two threat models), the CoCo stack (Kata, guest pull, Trustee KBS, peer-pods, agent policy), operational changes (secrets via KBS, degraded debugging, in-guest storage encryption), image supply-chain interplay, deployment-shape choice, honest limitations. |
| `rules/05-pets-coed.md` | computing on encrypted data without hardware trust: decision-first triage, FHE scheme families (BGV/BFV, CKKS, TFHE) + standardization anchors (ISO/IEC 28033, NIST PEC) + honest performance reality, MPC/threshold and collusion assumptions, ZKP engineering risks (circuits as security-critical code), PSI/OPRF workhorses, TEE-vs-PET-vs-DP selection table and hybrids. |

---

## Top-10 non-negotiables

1. **No attestation, no confidential computing.** The claim requires a
   hardware-based, attested TEE (CCC definition); memory encryption alone is
   marketing (`01`).
2. **Attestation must gate something** — key release, secret injection,
   channel establishment. Dashboard-only attestation is a Critical finding
   (`03`).
3. **Pick the lowest sufficient rung**: don't deploy an enclave where a KMS
   suffices, or FHE where a confidential VM does (`01`,`05`).
4. **Reject debug-mode TEEs in production**, verify the evidence chain to the
   silicon vendor's root, and treat out-of-date TCB as a policy decision —
   never a silent accept (`03`).
5. **Freshness is part of the proof**: bind a nonce or channel key into
   evidence; re-attest on schedule and on TCB events (`03`).
6. **SNP-class integrity or it doesn't count**: plain SEV/SEV-ES memory
   encryption without integrity and runtime attestation is insufficient
   against a malicious hypervisor (`02`).
7. **State the Nitro trust model honestly**: isolation + attestation with the
   provider still in the TCB — different from SEV-SNP/TDX operator exclusion
   (`02`).
8. **Confidential nodes ≠ confidential pods**: nodes exclude the cloud
   operator but not the cluster admin; for pod-level claims, secrets flow
   attest-then-release (KBS), never K8s Secrets (`04`).
9. **Side channels and availability are out of scope by design** — document
   the posture (SMT, ciphertext side channels, host DoS) in every design doc
   instead of assuming them away (`01`,`02`,`04`).
10. **PETs use vetted libraries (latest stable) and standard parameter sets
    only**; hand-rolled FHE parameters or ZKP circuits without audit are
    Critical findings, and FHE alone gives confidentiality, not result
    integrity (`05`).
