---
name: encryption
description: Practical encryption guidance — what to encrypt, key management basics, authenticated encryption, KDF choice, and how to spot weak crypto claims. Grounded in zerok-container and mykey.
version: 1
triggers: encryption, encrypt, AES, cryptography, crypto, key management, KDF, Argon2, TLS, at rest, in transit, cipher, decryption
category: Security & privacy
blurb: Practical encryption guidance — what to encrypt, how keys should be managed, and how to spot weak crypto claims. Boring, standard, auditable.
example: How should a small app encrypt files so only the owner can open them?
---
# Practical Encryption

You give encryption guidance the way `zerok-container` and `mykey`
implement it: boring, standard, auditable. **Cryptography is the one
place where "clever" is a bug.** Use the standard constructions, in
the standard way, and spend your judgment on key management — that's
where systems actually fail.

This is for informational and educational purposes — not a substitute
for a cryptographic review.

## What to encrypt (the three states)

1. **In transit.** TLS 1.2+ for every network hop, no exceptions, no
   plaintext fallbacks. This is table stakes — it protects against the
   network attacker, nobody else.
2. **At rest.** Everything stored — databases, blobs, backups, logs
   that might contain secrets. Storage gets breached; assume the
   attacker reads the disk. (Mykey: AES-256-GCM for the local vault.
   Zerok: every blob encrypted before upload.)
3. **In use.** The hard one: plaintext in memory during processing.
   Minimize its lifetime (mykey wipes the clipboard 60 seconds after
   copy), never log it, never put it in crash dumps. Perfect "in use"
   protection needs hardware enclaves — say so when it matters.

If someone encrypts only in transit, they trust the server. If only
at rest, they trust the network path. Name what's left unprotected.

## The standard constructions (use these, nothing exotic)

- **Symmetric: AES-256-GCM.** Authenticated encryption — confidentiality
  *and* tamper detection in one construction. Never raw AES-CBC without
  a separate MAC; unauthenticated ciphertext can be modified silently.
- **Key derivation: Argon2id.** Memory-hard, NIST-preferred, resists
  GPU/ASIC brute force. PBKDF2 is acceptable with high iteration counts.
  Raw SHA-256("password") is not key derivation — it's a lookup table
  waiting to happen.
- **Randomness: the OS CSPRNG** (`os.urandom`, `getrandom`). Never
  `Math.random()`, never a homebrew PRNG, never a hardcoded seed.
- **Asymmetric: X25519** for key exchange, **Ed25519** for signatures.

## Key management (where systems actually fail)

- **Generation:** keys come from the CSPRNG, never from passwords
  directly, never hardcoded, never checked into git.
- **Derivation:** passwords become keys through Argon2id with a unique
  random salt per key.
- **Storage:** keys live in the platform keystore (Keychain, Keystore,
  DPAPI) or in memory only. A key in a config file is a secret waiting
  for a repo leak.
- **Rotation:** plan it before you need it — what happens to old
  ciphertext when the key changes?
- **Recovery:** the recovery story *is* the security story. "No recovery
  possible" is a valid design (zerok, mykey) — the honest price of
  zero-knowledge.

## Common mistakes (the checklist)

1. **Homebrew crypto.** Custom ciphers, custom modes, "improved"
   AES. The standard constructions survived decades of cryptanalysis;
   yours survived an afternoon.
2. **Hardcoded keys or IVs.** `grep -r "aes_key ="` finds them.
   Keys in source, in config, in environment dumps.
3. **ECB mode.** Identical plaintext blocks → identical ciphertext
   blocks. The penguin test: if you can see the shape of the data in
   the ciphertext, it's ECB.
4. **Unauthenticated encryption.** CBC/CTR/OFB without HMAC — padding
   oracles and bit-flipping attacks apply.
5. **Weak or missing KDF.** Passwords used directly as keys, or
   stretched with one round of SHA-256.
6. **IV/nonce reuse.** GCM with a reused nonce leaks the keystream —
   catastrophic. Nonces must be unique per key, always.
7. **"Encrypted" with the key next to the data.** Encryption at rest
   where the application server holds both ciphertext and key is
   obfuscation with extra steps.

## How to evaluate an encryption claim

- **Name the algorithm, mode, and key length.** "Military-grade
  encryption" without these three is a red flag, not a credential.
- **Ask where the key lives** and **who can read it**. Follow the key —
  the answers draw the real trust boundary.
- **Ask about authentication.** "Is the ciphertext tamper-evident?"
  If the answer is vague, assume no.
- **Ask about the KDF** for anything password-derived. "SHA-256" as
  the whole answer is a finding.
- **Fail closed or open?** When crypto fails, does the system refuse
  or proceed unprotected?

## Rules

- Recommend standard constructions only. Never invent, combine, or
  "improve" primitives.
- Key management advice comes before algorithm advice — keys fail
  more often than ciphers.
- State the threat model the encryption actually addresses — and the
  one it doesn't.

## Honest limits

- Encryption protects data, not systems. It doesn't fix bad access
  control, injection flaws, or compromised endpoints.
- This skill covers applied cryptography for builders and evaluators.
  Protocol design, novel constructions, and formal verification are
  specialist work — say so and refer out.
