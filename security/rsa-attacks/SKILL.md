---
name: rsa-attacks
description: Use when you face an RSA challenge or misconfigured RSA on an
  authorized test, CTF, or code review and need an operator workflow for the
  classic attacks. Covers parameter sanity checks (key size, public
  exponent), Hastad broadcast attack on small e, common modulus attack,
  batch GCD for shared prime factors, Wiener attack on small private
  exponents, textbook RSA without padding, and automation with RsaCtfTool
  1.7.x plus manual OpenSSL 3.x and SageMath 10.x recovery. Use when you
  have RSA public keys, ciphertexts, or parameters that look weak, or when
  the crypto-fundamentals skill identified RSA as the primitive.
version: 1.0.0
domain: crypto
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [crypto-fundamentals, padding-oracle]
tools:
  - name: Python
    version: "3.12"
  - name: OpenSSL
    version: 3.x
  - name: SageMath
    version: 10.x
  - name: RsaCtfTool
    version: 1.7.x
---

RSA fails in practice long before the math does: tiny exponents, shared
primes across keys, missing padding, and small private exponents all
reduce it to arithmetic puzzles. This skill is the operator's checklist
for those failures on authorized targets: inspect the parameters, match
them to the known attack, recover the private key or plaintext, and
verify by decrypting. It assumes you can already recognize RSA as the
primitive (see crypto-fundamentals). All work targets systems you have
written permission to test, such as CTF challenges or client systems in
scope.

## Quick Workflow

1. Collect every parameter: n, e, ciphertexts, and any extra values
   (dp, dq, additional keys, signatures).
2. Sanity check: key size, public exponent value, and whether n looks
   like a product of two primes.
3. Run RsaCtfTool in auto mode for the quick wins while you think.
4. Match the parameters to a specific attack: small e broadcast, common
   modulus, shared factor, small d, or no padding.
5. Recover the private key or the plaintext with the matched technique.
6. Decrypt and verify: the plaintext should be readable or structured.
7. Document the exact weakness and the fix for the report.

## 1. Parameter collection and sanity checks

Gather n, e, and c as integers. CTF challenges hand them over; on a
pentest you extract them from certificates, JWT keys, or application
configs.

```bash
# Extract RSA parameters from a PEM public key
openssl rsa -pubin -in key.pub -text -noout | head -20

# From an X.509 certificate
openssl x509 -in cert.pem -text -noout | grep -A3 'Public-Key'

# Quick Python triage of parameters
python3 <<'EOF'
n = 0x00  # paste the modulus
e = 65537
print("n bits:", n.bit_length())
print("e:", e)
print("n mod e:", n % e)
EOF
```

Red flags at triage:

- e = 3: broadcast attack territory, and textbook RSA is likely.
- n under 512 bits: factor it directly, no cleverness needed.
- Several n values given together: try batch GCD for shared primes.
- dp, dq, or qinv leaked alongside n: private key reconstructs
  immediately.
- Same plaintext encrypted under two different keys: common modulus
  territory.

```bash
# Factor small n directly (under ~512 bits, fast)
python3 -c "
from math import gcd
# factorDB or yafu for larger; sage factor() for medium
"
# SageMath for serious factoring attempts
sage -c "print(factor(0x00))"  # paste n
```

## 2. RsaCtfTool auto mode

Run the automated tool first. It tries dozens of known attacks in
seconds and often solves the challenge while you read the parameters.

```bash
# Auto attack on a public key plus ciphertext
python3 RsaCtfTool.py --publickey key.pub --uncipher c.bin --private

# Private key recovery only
python3 RsaCtfTool.py --publickey key.pub --private -o recovered.pem

# Decrypt with explicit n and e
python3 RsaCtfTool.py -n 0xABC... -e 3 --uncipherfile c.bin
```

If RsaCtfTool solves it, still understand which attack fired (it prints
the attack name). The report needs the weakness class, not just the
recovered key.

## 3. Hastad broadcast attack (small e)

When the same message is encrypted with e = 3 under three or more
different moduli, the Chinese Remainder Theorem recovers m^3, and the
integer cube root is the message. No factoring required.

```python
#!/usr/bin/env python3
"""Hastad broadcast attack: e=3, same plaintext, 3+ different moduli."""
from math import gcd

def crt(remainders, moduli):
    M = 1
    for m in moduli: M *= m
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        inv = pow(Mi, -1, m)
        x += r * Mi * inv
    return x % M

def iroot(k, n):
    # integer k-th root via binary search
    lo, hi = 0, 1 << ((n.bit_length() // k) + 1)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** k < n: lo = mid + 1
        else: hi = mid
    return lo

# c_list[i] = m^3 mod n_list[i], all with e = 3
c_list = []  # paste ciphertexts
n_list = []  # paste moduli
assert len(c_list) >= 3 and all(gcd(a, b) == 1 for a in n_list for b in n_list if a != b)
m_cubed = crt(c_list, n_list)
m = iroot(3, m_cubed)
print("recovered m:", hex(m))
print(bytes.fromhex(hex(m)[2:]))
```

Requirements: at least e ciphertexts under pairwise coprime moduli,
same plaintext, no padding (or PKCS#1 v1.5 with e=3 can still work via
the related Coppersmith variant, which is advanced follow-up).

## 4. Common modulus attack

Same n, two different exponents e1 and e2, same plaintext: the extended
Euclidean algorithm recovers m without factoring n.

```python
#!/usr/bin/env python3
"""Common modulus: c1 = m^e1 mod n, c2 = m^e2 mod n, recover m."""
from math import gcd

def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

n = 0x00   # shared modulus
e1, e2 = 0, 0  # the two public exponents
c1, c2 = 0x00, 0x00

g, a, b = egcd(e1, e2)
assert g == 1
# handle negative exponents with modular inverses
c1p = pow(c1, a, n) if a > 0 else pow(pow(c1, -1, n), -a, n)
c2p = pow(c2, b, n) if b > 0 else pow(pow(c2, -1, n), -b, n)
m = (c1p * c2p) % n
print("recovered m:", hex(m))
```

This bites when a system reuses one modulus with per-user exponents,
or when a challenge hands you two encryptions of the flag.

## 5. Shared prime factors (batch GCD)

When many RSA keys are generated with weak randomness, two moduli
share a prime. The GCD of the pair reveals it instantly, and the
technique scales to thousands of keys with a product tree.

```python
#!/usr/bin/env python3
"""Pairwise GCD across a list of moduli to find shared primes."""
from math import gcd

moduli = []  # paste all n values
for i in range(len(moduli)):
    for j in range(i + 1, len(moduli)):
        g = gcd(moduli[i], moduli[j])
        if g != 1:
            print(f"shared factor between key {i} and {j}: {hex(g)}")
            p = g
            q = moduli[i] // p
            print(f"  key {i}: p={hex(p)} q={hex(q)}")
```

```bash
# For large key sets, use the batch GCD approach:
# build a product tree of all moduli, then take remainders.
# Tools: sage batch_gcd scripts, or the 'rsa_gcd' style implementations.
# On a pentest, weak embedded devices (routers, IoT) are the classic source.
```

Once p is known, q = n // p, phi = (p-1)(q-1), d = e^-1 mod phi, and
the key is fully recovered. Then decrypt normally.

## 6. Wiener attack (small private exponent)

If d < n^0.25 / 3, the private exponent leaks through continued
fraction expansion of e/n. RsaCtfTool tries this automatically; the
manual version confirms understanding.

```bash
# RsaCtfTool includes Wiener; also try in Sage
python3 RsaCtfTool.py --publickey key.pub --private --attack wiener
```

```python
# Continued fraction convergents of e/n, test each denominator as d
def convergents(num, den):
    # yields (k, d) convergent pairs
    cf = []
    while den:
        q = num // den
        cf.append(q)
        num, den = den, num - q * den
    convs = []
    for i in range(1, len(cf) + 1):
        n_, d_ = 1, 0
        n1, d1 = cf[0], 1
        # (simplified: full implementation tracks two previous)
        pass
    return convs
```

In practice, use the tool for Wiener and reserve manual effort for
verifying the recovered d by test-decryption. Small-d keys also fall
to Boneh-Durfee (d < n^0.292) via lattice methods in Sage, which is
the escalation when Wiener fails.

## 7. Textbook RSA without padding

Without padding (PKCS#1 OAEP or v1.5), RSA is malleable: ciphertexts
can be multiplied, and chosen-ciphertext tricks decrypt.

```python
# Malleability: c' = c * (2^e) mod n decrypts to 2*m mod n
# If you have a decryption oracle, ask for c' and halve the result.
n, e = 0x00, 65537
c = 0x00
c_blinded = (c * pow(2, e, n)) % n
# send c_blinded to the oracle, get m_blinded = 2*m mod n
# m = m_blinded * inv(2, n) % n
```

Also: small message with e=3 and no padding is just an integer cube
root (single-modulus Hastad). And deterministic textbook RSA lets you
test plaintext guesses by re-encrypting, which breaks semantic
security outright.

## 8. Decrypt and verify

```python
#!/usr/bin/env python3
"""Decrypt once p and q are known."""
from Crypto.Util.number import long_to_bytes  # pycryptodome, or manual

def decrypt(n, e, c, p, q):
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    blen = (m.bit_length() + 7) // 8
    return m.to_bytes(blen, 'big')

# p, q from any attack above; c the ciphertext
pt = decrypt(n, e, c, p, q)
print(pt)
```

Faster for repeated decryptions: use CRT with dp = d mod (p-1) and
dq = d mod (q-1). For CTF flags, the plaintext usually starts with a
known prefix; check for it as your correctness signal.

## Edge cases

- RsaCtfTool solves nothing and parameters look normal. The key may
  be fine and the challenge expects a protocol attack (padding
  oracle, Bleichenbacher) rather than a math attack. Pivot to the
  padding-oracle skill.
- n is prime, not a product. Then "RSA" is degenerate: phi = n-1
  and d computes directly. Challenges sometimes do this as a trick.
- e is even or shares a factor with phi. Key generation is broken;
  try small factors of e or treat it as a Rabin-like variant.
- Ciphertext is larger than n or negative. Normalize: c mod n before
  any attack math.
- Multiple test cases share e=3 but different plaintexts. Broadcast
  needs the SAME plaintext; different plaintexts need Coppersmith
  (Sage `small_roots`), which is the advanced escalation.
- The private key uses CRT parameters (dp, dq, qinv) that leaked.
  Reconstruct p and q from them directly instead of attacking n.

## Escalation

- Wiener fails but d still looks small: Boneh-Durfee lattice attack
  in Sage (works up to d < n^0.292). Needs Sage and patience.
- Partial key exposure: if you know some high or low bits of p
  (from a side channel or a leak), Coppersmith's method in Sage
  recovers the rest from roughly half the bits.
- n has three or more prime factors (multi-prime RSA): trial divide
  small factors first, then apply the standard attacks per factor.
- The challenge is actually Rabin (e=2): decryption gives four
  candidates; pick by padding structure or known prefix.
- Nothing mathematical works: re-examine the protocol. RSA key
  transport without OAEP, PKCS#1 v1.5 decryption oracles
  (Bleichenbacher), and signature forgery on e=3 are protocol
  attacks, not factoring attacks.

## Detection and defender view

Defenders rarely detect RSA math attacks in progress; they prevent
them by generating keys correctly. The durable defenses are: use
2048-bit or larger keys from a proper CSPRNG, use standard public
exponent 65537, always use OAEP padding for encryption and PSS for
signatures, never reuse a modulus across keys, and never expose CRT
parameters or decryption oracles. For code review, grep for raw
`pow(m, e, n)` style encryption, hardcoded small e values, and custom
padding schemes; each is a finding. Key rotation after any suspected
weak generation (embedded devices, VMs with poor entropy at first
boot) closes the batch-GCD window.

## Key references

- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): weak RSA
  parameters.
- CWE-330 (Use of Insufficiently Random Values): shared primes from
  bad RNG.
- CWE-780 (Use of RSA Algorithm without OAEP): textbook RSA.
- MITRE ATT&CK T1552.004 (Unsecured Credentials: Private Keys): when
  recovered keys grant access.
- RsaCtfTool: https://github.com/RsaCtfTool/RsaCtfTool
- OpenSSL documentation: https://docs.openssl.org/
- SageMath documentation: https://doc.sagemath.org/

## See also

- `ctf-crypto-challenges-rsa-attacks`: Use it instead for the competition version, framed as an ordered attack checklist against challenge RSA parameters.
