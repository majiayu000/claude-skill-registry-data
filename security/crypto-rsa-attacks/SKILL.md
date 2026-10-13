---
name: crypto-rsa-attacks
description: >
  Break RSA when parameters or padding are weak — recover plaintext or the private key from a public
  key and ciphertext. Load when you meet RSA in auth/tokens/TLS/custom crypto and have (n, e) + a
  ciphertext. Signals: a public key or n/e/c values, small exponent e=3, "textbook RSA", a JWT signed
  RS256 with a suspicious key, RsaCtfTool, factordb, close/shared primes, key you can't verify.
domain: cryptography
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A02:2021-Cryptographic-Failures]
cwe: [CWE-327, CWE-780]
tools: [rsactftool, openssl, python-pycryptodome, sympy]
schema_version: 1
---

# RSA attacks

## When it applies
RSA is used somewhere you can reach on an authorized target — a session token/cookie, a licence
check, a custom API request signature, a JWT (RS256), or an exposed keypair — and you can read the
public key `(n, e)` and a ciphertext/signature. Real systems get RSA wrong in a handful of
repeatable ways; each has a direct recovery.

## Why it works
RSA is only as strong as its parameters and padding. "Textbook" RSA (no OAEP/PSS) is malleable and
deterministic, small or shared parameters are mathematically reversible, and a factorable modulus
hands you the private key outright. You don't break RSA — you exploit the specific weakness in *this*
key.

## Method
1. **Extract parameters.** From a PEM: `openssl rsa -pubin -in key.pem -text -noout` (gives `n`, `e`).
   From a JWT: decode the header/key. Note `e` and the bit-length of `n`.
2. **Match the weakness → attack:**
   - **Factorable `n`** — look it up on **factordb**; small/known `n` factors instantly → derive `d`.
   - **Close primes (p≈q)** — **Fermat factorisation** recovers `p,q` in milliseconds.
   - **Small `e` (e=3) + small message** — plaintext may be `< n^(1/e)`; take the integer **cube root**
     of `c` (no modular reduction happened). Also **Håstad** broadcast if the same msg is sent to
     several keys.
   - **Shared prime across two keys** — `gcd(n1, n2)` yields a common factor → both keys fall.
   - **Common modulus** (same `n`, two `e` with gcd 1 on the same message) — combine with Bézout.
   - **Small private exponent `d`** — **Wiener's attack** (continued fractions).
   - **Textbook (no padding)** — malleable: forge/blind via `c' = c·r^e mod n`; deterministic
     encryption enables chosen-ciphertext games.
3. **Automate the triage** with **RsaCtfTool** (`rsactftool --publickey key.pem --uncipher c` runs the
   above battery), then finish by hand once you know which weakness hit.
4. **Recover and use** — with `p,q`: `d = e^-1 mod (p-1)(q-1)`, decrypt `c`, or re-sign to forge a
   token/signature.

## Gotchas
- **Proper padding (OAEP/PSS) with strong random primes ≈ unbreakable** — don't burn time; the win is
  a *misconfiguration*, not the algorithm. Confirm it's textbook/weak first.
- **`e` and `d` are inverses mod φ(n)** — a wrong φ (using `n` instead of `(p-1)(q-1)`) gives a key
  that "looks" right but fails; verify by decrypting a known value.
- **JWT RS256 → key confusion** is a *different* bug (alg swap to HS256) — see `web-auth-jwt`; this
  skill is for weak RSA keys themselves.
- Endianness / block size when converting the integer back to bytes trips people up
  (`long_to_bytes`).

## Verify success
Recovered plaintext that is meaningful (or a forged signature/token the target accepts), and — when
you factored `n` — a private key that correctly decrypts a value you can check.

## References
RsaCtfTool; factordb; Boneh "Twenty Years of Attacks on RSA"; Wiener's attack; pycryptodome.
Related: `web-auth-jwt`, `crypto-oracle-attacks`.
