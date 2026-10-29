---
name: rng-attacks
description: Use when assessing random number generation on an
  authorized engagement. Covers weak PRNGs, seed prediction, VM
  snapshot issues, and reviewing randomness sources in code. Also use
  when tokens, keys, or nonces look predictable.
version: 1.0.0
domain: crypto
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [crypto-fundamentals, ecc-crypto-attacks, web-sqli]
tools:
  - name: Python
    version: "3.12"
---

Bad randomness breaks everything built on it: predictable tokens,
recoverable keys, and guessable session IDs. This skill covers
authorized assessment: spotting weak generators, testing token
predictability, and reviewing entropy sources. Test on systems you
may assess, with harmless proofs.

## Quick Workflow

1. Find what needs randomness: tokens, keys, nonces, session IDs,
   and password resets.
2. Identify the generator: OS CSPRNG, language secure random, or
   something weaker.
3. Test predictability: collect outputs and look for patterns.
4. Check seeding: time based, PID based, or fixed seeds are
   findings.
5. Review VM and container entropy: fresh clones share state.
6. Check for nonce and IV reuse that implies RNG failure.
7. Prove impact with a prediction on a test account, not a victim.
8. Recommend the OS CSPRNG everywhere, with no custom mixing.

## 1. Generator review and prediction test

```bash
# Search for weak generators
grep -rn "Math.random()\|rand()\|srand\|Random()" \
  --include="*.js" --include="*.py" --include="*.php" --include="*.java" \
  src/ | grep -v -i "test" | head -20
# Math.random for tokens, rand() for keys, srand(time) = findings
# Safe: crypto.randomBytes, secrets module, SecureRandom, getrandom
```

```python
#!/usr/bin/env python3
"""Token predictability screen (authorized test endpoint)."""
import collections

# Collect reset tokens for your own test accounts
toks = ["a3f9...", "b7e1..."]  # fill from captured test traffic
print("checks:")
print("1. length and alphabet (short numeric = brute forcible)")
print("2. sequential or time correlated?")
print("3. does the token change per request (no reuse)?")
# Statistical: chi-square on nibbles is a quick randomness smell test
```

## 2. Seed and entropy review

```bash
# VM snapshot issue: cloned VMs with the same RNG state generate the
# same "random" keys. Check: does first boot seed from fresh entropy?
# Containers: check /proc/sys/kernel/random/entropy_avail at keygen time
cat /proc/sys/kernel/random/entropy_avail
# Review key generation ceremonies: where, when, and on what entropy
```

## Edge cases

- The generator is fine but the token is too short. That is a
  brute force issue, not RNG; rate limiting is the fix.
- Custom "mixing" of multiple sources. Usually harmless but
  unreviewed; recommend the plain OS CSPRNG instead.
- Deterministic builds need deterministic randomness. Use a seeded
  DRBG documented as non security, separate from security RNG.

## Escalation

- Predictable tokens confirmed: demonstrate account takeover on
  your test account, then report as critical.
- Weak PRNG in key generation: the keys are compromised by design;
  recommend rotation after fixing the generator.

## Detection and defender view

Defenders detect RNG failures through duplicate keys or nonces in
the wild, token prediction reports, and audits of the generator
choice. The fix is boring: use the OS CSPRNG (getrandom,
BCryptGenRandom, SecRandomCopyBytes), never seed it yourself, and
review every randomness call site. Post incident, rotate everything
the weak generator produced.

## Key references

- CWE-330 (Use of Insufficiently Random Values).
- CWE-338 (Use of Cryptographically Weak PRNG).
- NIST SP 800-90A: DRBG constructions.
