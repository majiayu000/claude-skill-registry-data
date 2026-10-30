---
name: crypto-library-misuse
description: Detects library-internal cryptographic correctness bugs that pattern matchers and crypto-failures skills miss — AEAD nonce reuse, ECDSA k-value reuse, length-extension on bare hashes, padding-oracle exception distinguishability, and branching on secret material. Use when writing code that calls a crypto primitive directly (AEAD encrypt/decrypt, ECDSA/DSA sign, raw hash, RSA decrypt). Distinct from cryptographic-failures, which covers application-layer choices like MD5 for passwords; this skill is about how primitives are wired up.
---

# Crypto Library Misuse (CWE-323, CWE-330, CWE-208)

## What this checks

Cryptographic primitives are correct only when their preconditions are met. Not
"weak algorithm picked" — that's `cryptographic-failures`. These are "right
primitive, wrong wiring": nonce reused, per-signature random reused, comparison
branches on secret bits, exception type leaks which decryption failure happened.
Each pattern below has produced a real CVE (Sony PS3 ECDSA k-reuse, Marvin RSA timing).

## Vulnerable patterns

- **AEAD nonce reuse**: an AEAD encrypt call where the nonce is fixed, zeroed, or
  a wrapping counter. A single reused nonce lets an attacker XOR two ciphertexts
  and recover both plaintexts.
- **ECDSA/DSA k reuse or weak randomness**: signing with a predictable or repeated
  per-signature random value. Two signatures with the same k recover the private
  key by linear algebra.
- **Length-extension on bare hashes**: using `hash(secret || msg)` as a MAC. SHA-2
  length-extension lets an attacker forge a valid tag over an extended message.
- **Padding oracle via exception distinguishability**: distinct exception types
  for "ciphertext too short" versus "padding invalid". Bleichenbacher and Manger
  attacks need exactly that one bit per query.
- **Branching on secret material**: a conditional whose branch depends on a key
  bit or MAC byte produces a measurable timing difference. Includes early-exit
  byte comparison on MAC or signature verification.
- **Static IV for CBC**: encrypting two plaintexts with the same IV reveals their
  common prefix.
- **ECB used for structured data**: identical plaintext blocks produce identical
  ciphertext blocks, leaking structure.

## Fix immediately

Flag the vulnerable call site and explain the risk. Then suggest a fix that
establishes these properties:

1. **Every AEAD encrypt uses a fresh nonce drawn from a CSPRNG**, or a managed
   monotonic counter with an overflow guard. The nonce is stored or transmitted
   alongside the ciphertext.
2. **ECDSA/DSA signing uses deterministic k (RFC 6979)** or a library that
   guarantees a fresh per-signature random — the caller never supplies k.
3. **MACs use a MAC primitive (HMAC, Poly1305, KMAC), not a bare hash of
   `secret || msg`.** HMAC's two-pass construction defeats length-extension.
4. **Comparisons over MACs, signatures, or hashes use a constant-time primitive**
   documented for that purpose — never plain equality or early-exit byte comparison.
5. **All decryption-failure paths raise a single exception type at the boundary**,
   collapsing padding, length, and authentication failures into one indistinguishable
   error.
6. **No branch inside a crypto routine depends on a secret bit.** Use bitwise
   selection or library primitives that document constant-time behavior.
7. **CBC uses a fresh random IV per message; ECB is not used for structured data.**
   Prefer an AEAD mode over CBC+MAC when the platform offers one.

Translate these principles to the audited file's language and crypto library. Use
the documented high-level API (AEAD wrapper, signing context, HMAC primitive,
constant-time-compare helper) — do not assemble these guarantees by hand.

## Verification

After rewriting, confirm:

- [ ] Every AEAD encrypt site uses a fresh CSPRNG nonce or a managed monotonic counter with overflow check
- [ ] No signing call passes a caller-supplied k unless the API documents deterministic k (RFC 6979)
- [ ] No MAC is implemented as `hash(secret || msg)`; HMAC or a MAC primitive is used
- [ ] All MAC, signature, and hash comparisons use a constant-time primitive — never plain equality
- [ ] All decryption failures raise the same exception type at the boundary
- [ ] No branch in the crypto routine depends on a secret bit

## References

- CWE-323 ([Reusing a Nonce, Key Pair in Encryption](https://cwe.mitre.org/data/definitions/323.html))
- CWE-330 ([Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html))
- CWE-208 ([Observable Timing Discrepancy](https://cwe.mitre.org/data/definitions/208.html))
- CWE-326 ([Inadequate Encryption Strength](https://cwe.mitre.org/data/definitions/326.html))
