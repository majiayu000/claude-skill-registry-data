---
name: crypto-oracle-attacks
description: >
  Break weak symmetric crypto in real apps — decrypt or forge encrypted tokens/cookies without the
  key via padding oracles (CBC), ECB block shuffling, and hash-length-extension of homemade MACs.
  Load when the app hands you ciphertext you can tamper with and resend: an encrypted cookie/token,
  a "state"/"data" blob, an IV+ciphertext, a `H(secret‖msg)` signature, base64 that changes on edit.
domain: cryptography
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A02:2021-Cryptographic-Failures]
cwe: [CWE-327, CWE-347, CWE-649]
tools: [padbuster, python-pycryptodome, hashpump, burp]
schema_version: 1
---

# Oracle & symmetric-crypto attacks

## When it applies
An app protects data with symmetric crypto you can poke — an encrypted session cookie, a
"remember me"/state token, a signed-with-a-hash parameter — and it lets you submit modified
ciphertext and observe a difference (an error vs. success, a padding error, different output). That
observable difference is an oracle you can turn into full decrypt/forge, no key needed.

## Why it works
Encryption without authentication is malleable: CBC leaks validity through padding errors, ECB
reveals structure and lets you rearrange blocks, and `MAC = H(secret‖message)` (Merkle–Damgård) can
be extended without knowing the secret. The key never leaks — the *mode/construction* does the work.

## Method
1. **Fingerprint the token.** Decode (base64/hex); measure length. A multiple of 8/16 bytes → a block
   cipher (CBC/ECB). Flip one byte and resend: a distinct "padding"/"decryption" error = CBC padding
   oracle; identical ciphertext blocks for identical plaintext = ECB.
2. **CBC padding oracle** — when the server reveals valid vs. invalid padding: recover plaintext byte
   by byte, and *encrypt* arbitrary plaintext (forge a token) by controlling the preceding block.
   `padbuster <url> <ciphertext> <blocksize> -cookies ...`, or a Python oracle loop. This is the
   classic "decrypt/forge the admin cookie" attack.
3. **ECB weaknesses** — identical plaintext blocks → identical ciphertext:
   - **Cut-and-paste**: rearrange whole blocks to splice a privileged value (e.g. move an aligned
     `role=admin` block into place).
   - **Byte-at-a-time decryption**: if your input is prepended to a secret and ECB-encrypted, recover
     the secret one byte per aligned block.
4. **Hash length extension** — a signature of the form `H(secret‖data)` (MD5/SHA1/SHA2) with known
   `data` and secret length: append your own data and compute a valid new MAC with **hashpump**
   (`hashpump -s <sig> -d <data> -a <append> -k <keylen>`), bypassing the "integrity" check.
5. **Weak/predictable tokens** — if it turns out not to be real crypto: ECB pattern, a static IV,
   XOR with a fixed keystream, or a guessable PRNG seed (timestamp) → derive/forge directly.
6. **Forge and use** — mint the token that says what you want (admin, another user) and replay it;
   validate the access gained with `reporting-triage-validation`.

## Gotchas
- **Authenticated encryption (AES-GCM, encrypt-then-HMAC) kills these** — a padding oracle needs an
  *unauthenticated* CBC error signal; if tampering just fails uniformly, move on.
- **The oracle can be subtle** — a timing difference, a 500 vs 403, or a different redirect counts;
  diff responses carefully before concluding "not vulnerable".
- **Block alignment is everything** for ECB cut-and-paste and byte-at-a-time — pad your input to land
  targets on block boundaries.
- **HMAC (not `H(secret‖msg)`) is not extendable** — length extension only hits raw Merkle–Damgård
  concatenation MACs.

## Verify success
A token you decrypted or forged that the application accepts as another/privileged user (or recovered
plaintext of a value you couldn't read), reproduced from a clean session.

## References
Vaudenay padding-oracle; `padbuster`; the Cryptopals set (mechanisms); `hashpump`.
Related: `web-auth-jwt`, `crypto-rsa-attacks`, `web-idor`.
