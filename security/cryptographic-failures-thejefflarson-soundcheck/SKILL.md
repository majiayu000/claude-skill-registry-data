---
name: cryptographic-failures
description: Detects weak or broken cryptography that lets attackers recover plaintext
  passwords, forge tokens, or decrypt sensitive data. Use when writing code
  that encrypts or decrypts data, hashes passwords or tokens, generates random
  values for security purposes, manages cryptographic keys, or configures
  TLS/SSL settings. Also invoke when storing sensitive data at rest.
---

# Cryptographic Failures Security Check (A04:2025)

## What this checks

Protects against weak or broken cryptography that allows attackers to recover
plaintext passwords, forge tokens, or decrypt sensitive data. Failures here
directly enable credential stuffing, account takeover, and data breach.

## Vulnerable patterns

- Password hashed with a fast or unsalted algorithm such as MD5, SHA1, or bare SHA-256
- Security-sensitive token, session ID, nonce, or key generated from a non-cryptographic PRNG
- Encryption or signing key declared as a hardcoded string in source
- Symmetric encryption using ECB mode, or CBC mode with no separate MAC
- A nonce or IV that is constant, zero, or reused across messages with the same key

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Passwords go through a slow, salted, memory-hard hash** — bcrypt, scrypt, or
   argon2. Never MD5, SHA1, or SHA256-alone: they're fast enough to brute-force
   billions of candidates per second on consumer GPUs. The salt is per-password
   and stored alongside the hash, not a global constant.
2. **Security-sensitive randomness comes from a CSPRNG** — the language's
   documented cryptographic random source. Never a general-purpose PRNG or
   time-seeded generator for tokens, session IDs, nonces, or keys.
3. **Symmetric encryption uses an authenticated mode** — AES-GCM, AES-CCM, or
   ChaCha20-Poly1305. ECB never; CBC only with a separate MAC (encrypt-then-MAC).
   A fresh nonce per message, never reused with the same key.
4. **Keys live outside the source tree** — environment variable, secrets manager,
   KMS, or OS keystore. Never hardcoded literals, never committed config files.
   Rotation requires touching infrastructure, not source.

Translate these principles to the audited file's language and platform. Use the
documented cryptographic primitives for that stack — do not reimplement hashing,
random, or AEAD from lower-level building blocks.

## Verification

Confirm the response:

- [ ] Passwords are hashed with bcrypt, scrypt, or argon2 — never MD5, SHA1, or SHA256 alone
- [ ] All security tokens use the language's cryptographic random source — never a general-purpose PRNG
- [ ] No keys or secrets appear in source code; all loaded from environment or a secrets manager
- [ ] Symmetric encryption uses an authenticated mode (GCM, CCM, ChaCha20-Poly1305) — not ECB or CBC without MAC

## References

- CWE-327 ([Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html))
- CWE-326 ([Inadequate Encryption Strength](https://cwe.mitre.org/data/definitions/326.html))
- CWE-330 ([Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html))
- [OWASP A04:2025 Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
