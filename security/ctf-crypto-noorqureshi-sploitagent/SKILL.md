---
name: ctf-crypto
description: >
  CTF crypto challenge playbook — read the provided encryption script like a spec, attack RSA
  parameter weaknesses, XOR/multi-time-pad oracles, and homemade ciphers with math tooling
  (z3, sympy, sage). Load when the handout is .py/.sage math, n/e/c values, or an "encryption
  service" on nc. Signals: "crypto" category, chall.py with Crypto.Util.number, e=3 or e=65537,
  "encrypted_flag", XOR with a key, nc service that encrypts your input.
domain: ctf
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
cwe: [CWE-327, CWE-780]
tools: [python-pycryptodome, z3, sympy, sage, rsactftool, factordb, xortool, cyberchef]
schema_version: 1
---

# CTF crypto challenges

## When it applies
The handout is a short encryption script (`chall.py`, rarely sage), a set of numbers
(`n, e, c` / intercepted ciphertexts), or an `nc` service that encrypts/signs things for you.
This skill covers the CTF shapes — reading the script for the flaw, XOR games, homemade ciphers,
and math tooling. For the deep attack mechanics it defers to `crypto-rsa-attacks` and
`crypto-oracle-attacks`; run the RSA battery there first.

## Why it works
CTF crypto is a *code review against math*: the script is short, self-contained, and contains
exactly one mistake the author planted — a reused nonce, a factorable `n`, an invertible
homegrown round function, or an oracle the service hands you. Find the one line that looks
"clever" and the challenge is usually done; the rest is algebra.

## Method
1. **Read the script as a spec, top to bottom.** Note exactly what's given (printed values) and
   what's hidden (keys, seeds, flag). The flaw is almost always in: key/nonce generation
   (`random` instead of `secrets`, timestamp seeds, `getPrime` with small bits, reused `k`),
   the composition (same key twice, encrypt-then-leak-something), or the padding (raw RSA, ASCII
   armor that leaks length).
2. **Triage encodings before crypto.** Half of "crypto" challenges are encoding stacks: base64/32/
   85, hex, morse, brainfuck, base-N with a custom alphabet, repeated base64. CyberChef's magic
   wand or a quick decode loop settles these in minutes — don't reach for sage on a base85.
3. **RSA → run the known battery.** Extract `n, e, c`; hand the key to RsaCtfTool + factordb,
   then check the CTF-specific shapes explicitly (`crypto-rsa-attacks` for mechanics):
   - Multiple keys/ciphertexts in one file → `gcd` pairwise (shared prime), common modulus
     (same `n`, two `e`), or Håstad broadcast (same message, small `e`, several `n`).
   - `p` and `q` generated from a weak PRNG / shared high bits / `q = next_prime(p)` → Fermat or
     regenerate the PRNG stream.
   - Extra printed values (`d mod (p-1)`, `p+q`, `dp`, partial bits of `p`) → Coppersmith-style
     recovery (sage) or direct algebra; these "hint leaks" are the intended path.
4. **XOR challenges.**
   - Single-byte XOR: brute all 256 keys, score by English frequency (`xortool` automates).
   - Repeating-key XOR: guess key length by Hamming distance / index of coincidence, solve each
     column as single-byte.
   - **Multi-time pad** (same keystream XORs several messages, classic `otp` reuse): crib-drag —
     XOR two ciphertexts and guess words ("the ", "flag{") at each position; each confirmed crib
     extends the keystream.
   - XOR with a known plaintext anywhere (a known header, the flag format `flag{`) recovers
     keystream bytes directly.
5. **Encryption services are oracles — script them.** `nc` service that encrypts your input:
   - Your input prepended to the flag, ECB → byte-at-a-time flag recovery (`crypto-oracle-attacks`).
   - Same plaintext always → same ciphertext: codebook lookup / chosen-plaintext mapping.
   - Decrypt-anything-but-the-flag → malleability games: bit-flip CBC, RSA blinding
     (`c·r^e mod n`, unblind the result).
   - It always helps to send structured probes: all-zero blocks, single-byte deltas, length sweeps
     (leaks block size and mode).
6. **Homegrown ciphers → model, don't guess.** Custom rounds (add-rotate-xor, matrix mods,
   LFSRs, "Feistel-ish"): symbolically execute or invert them.
   - Linear operations over GF(2) → write as linear equations, solve with z3 or sage.
   - Small state (LFSR) → Berlekamp–Massey from a known keystream.
   - S-box + permutation networks → differential or just brute the tiny key space the author used.
   - Ask: *is every step invertible given the key? Then the only question is the key space* —
     brute 16/24/32-bit keys before doing anything clever.
7. **Bring the math tools.** z3 for constraint-shaped problems (flag bytes satisfying check
   equations); sympy for modular algebra and small discrete logs; sage for lattices (LLL /
   Coppersmith / hidden-number problems); `long_to_bytes`/`bytes_to_long` endianness discipline
   throughout.

## Gotchas
- **The printed "leak" is intentional.** If the script hands you `hint = p ^ q` or
  `leak = d & ((1<<512)-1)`, that's the solve path — stop looking for a second bug.
- **Python `random` is not crypto** — `random.seed(time.time())` or Mersenne Twister output
  visible anywhere → clone the state (624 consecutive 32-bit outputs fully recover MT19937).
- **`e` and `phi` mistakes** — wrong totient (using `n` for `(p-1)(q-1)`) makes a key that looks
  right but fails; verify by decrypting a known value (`crypto-rsa-attacks`).
- **Multi-prime RSA** (`n = pqr`) — factorization tools still work; remember `phi = (p-1)(q-1)(r-1)`.
- **Encoding is not encryption** — if "ciphertext" decodes cleanly to printable text, keep
  peeling encodings before assuming a cipher.
- **Byte-vs-int conversion bugs in *your* solver** — leading zero bytes vanish in
  `bytes_to_long`; pad the recovered plaintext back to the expected length.

## Verify success
The recovered plaintext contains the flag in the event's format, and you can re-derive it
deterministically (script reproduces the key/plaintext from the given artifacts, not from luck).

## References
Mechanics: `crypto-rsa-attacks` (factordb, Fermat, Wiener, Håstad), `crypto-oracle-attacks`
(padding oracle, ECB byte-at-a-time, length extension); tooling: z3, sage (LLL/Coppersmith),
xortool, CyberChef. Triage via `ctf-methodology`.
