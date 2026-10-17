---
name: certification
description: The certification methodology — how to go from a plain-language spec to code you can prove correct. Proof certificates, the trust primitive, what "certified" means and what it doesn't.
version: 1
triggers: certify, certification, proof certificate, formally verified, Lean, proof assistant, correctness proof, verified code, audit trail, tamper-evident, specification to code, algorithm correctness
category: Engineering & code
blurb: Explains and applies the certification method — how software goes from a plain-language promise to a proof certificate anyone can re-check.
example: How would you certify that a sorting routine is correct?
---
# Certification — From Plain Language to Provable Code

When someone asks you to certify an algorithm — to prove code correct,
not just test it — follow the AxiomCode pipeline. The core insight:
**separate what the code should do (the spec) from whether it does it
(the proof), and let a machine check the second part.**

## The pipeline (in order, never reorder)

1. **Plain-language description.** The human describes the algorithm in
   ordinary words: "binary search on a sorted array." No code yet.
2. **Formal specification.** Translate the description into theorem
   statements (Lean 4 style): preconditions, postconditions, invariants.
   This is the step where ambiguity dies — if you can't state it
   formally, you don't understand it yet.
3. **Proof search.** Find a machine-checkable proof that the algorithm
   satisfies the spec. This is the hard, expensive step. It may fail.
4. **Machine checking.** A proof assistant (Lean 4) checks the proof.
   Only this step confers the word "verified." Nothing else does.
5. **Code extraction.** Generate the actual artifact (C binary, Python
   package) from the proven construction.
6. **Signing + certificate.** Sign the artifact. Issue a proof
   certificate binding: what was checked, the artifact hash, the
   outcome, the timestamp, the signer.

## The trust primitive (shared with codetopo)

Two pieces, always together:

- **Proof certificate** — a signed attestation of provenance and
  integrity. Anyone can re-check it without trusting you. Ed25519
  signatures; public verification, no secret needed to audit.
- **Tamper-evident audit log** — hash-chained, append-only. Every
  operation recorded; each entry hashes the previous one. Re-walk the
  chain to verify the log itself, not just the tool that wrote it.

## What "certified" means — and what it doesn't

**Certified means:** a proof assistant actually checked the proof, and
the certificate says `verified`. The code does what the spec says, as
far as the machine could check.

**Certified does NOT mean:**

- The spec was right. A perfectly proven implementation of the wrong
  specification is still wrong. Spec correctness is human judgment —
  the proof can't check your intent.
- The proof was complete. Artifacts carry honest status:
  `verified` (machine-checked), `unverified` (no proof attempted or
  available), `failed` (proof attempted, didn't check). Never claim a
  proof you did not check. An honest `unverified` beats a fake
  `verified` every time.
- The code is fast, secure against side channels, or robust to
  adversarial input. Correctness is one property, not all of them.
- The LLM-generated spec was faithful. LLMs draft specs; humans review
  them. The formalization step is where most real errors hide.

## Rules

- **Verify, don't trust.** The certificate is the product, not the
  claim. "Trust me" is not a certification methodology.
- **Honest status always.** Every artifact declares verified /
  unverified / failed. Hiding the status is mis-issuance — the
  existential risk.
- **Zero-trust components.** Every output independently verifiable. No
  component gets trusted because another component vouched for it.
- **Spec first, code second.** If you can't write the spec, you can't
  certify the code. Refuse to certify what you can't specify.
- **Minimal dependencies.** Every dependency is an unaudited trust
  assumption. Prefer stdlib; justify everything else.

## Honest limits

- Formal methods prove what was specified, not what was wanted. The
  gap between intent and spec is where certification fails silently.
- Proof search doesn't always succeed — complex algorithms may resist
  automation. Say so; don't fake it.
- This methodology covers functional correctness. Performance,
  concurrency, and security properties need their own proofs.
- Toolchain bugs happen. Certificates need serials, issuers, and
  validity windows — and revocation must exist for when the prover
  itself is found wrong.
