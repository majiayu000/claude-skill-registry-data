---
name: crypto-puzzle-hypothesis
description: Systematic clue extraction, hypothesis ranking, and experiment-led cryptographic puzzle solving for ciphertexts, encoded hint lines, hidden URLs, metadata-based clues, and modern KDF or AEAD guessing. Use when Codex needs to analyze a crypto puzzle, CTF-style encrypted message, suspicious base64 or hex payload, layered clue chain, or “decrypt this line” challenge and should separate confirmed facts from hypotheses, probe common encodings, and test one explicit attack matrix at a time.
---

# Crypto Puzzle Hypothesis

## Overview

Use this skill to solve cryptographic puzzles without drifting into random brute
force or speculative answers. Treat the work like a narrow hypothesis loop:
extract facts, rank clues, run one experiment batch, keep or discard, then move
to the next frontier.

## Quick Start

1. Probe every payload before guessing secrets.

```bash
node scripts/probe_payload.mjs '/rRoSapsG0mYJtfMxKA3LigccFOylL+ZL7stK8x1dk+43Z2sjXhINL+q1BtWBSCQBfnAJXRwYkBNGBxZyinKV+Iz3vSpfRLa6kj='
```

2. Decode suspicious text clue lines before treating them as plaintext.

```bash
node scripts/decode_text_clues.mjs '(96C6 :E 2== 3682}0_>AIqd:\'"'"'"'
```

3. If a decoded clue or metadata clue is a natural-language phrase, search it
   as an exact quote before broad semantic expansion. Record the source,
   quoted context, and nearby named entities as new clue material.

4. Build a ranked hypothesis list using
[references/hypothesis-loop.md](references/hypothesis-loop.md).

5. Only then run a narrow modern-AEAD matrix with a JSON config:

```bash
node scripts/run_aead_matrix.mjs ./matrix.json
```

## Workflow

### 1. Normalize Artifacts First

- Count characters and decoded bytes before inferring algorithms.
- Separate ciphertext lines from clue lines, metadata, and visual context.
- For a readable but oddly specific phrase, run exact-quote lookup before
  treating it as a password candidate.
- Prefer measurable claims like:
  - `base64 decodes to 74 bytes`
  - `line 2 is 28 chars and ROT47 decodes cleanly`
  - `CBC is weak because remaining bytes are not block-aligned`

Use [references/common-framings.md](references/common-framings.md) when the
blob shape matters.

### 2. Classify Each Clue

Treat each clue as one of:

- textual transform clue
- exact quotation clue
- semantic pointer
- metadata clue
- crypto-parameter clue
- likely decoy

Read [references/clue-taxonomy.md](references/clue-taxonomy.md) to decide
whether a string should be treated as:

- a direct password candidate
- a route to another source
- a likely salt or AAD candidate
- a theme confirmation only

### 3. Rank Hypotheses Before Testing

Keep a short frontier with:

- hypothesis
- evidence
- confounds
- next experiment
- discard condition

Prefer hypotheses like:

- `the second line is a transform that points elsewhere`
- `the new description text is an intermediate clue, not the password`
- `13mm is better as metadata than as a direct secret`
- `the added phrase is an exact quotation whose source supplies the next clue family`

Do not treat memetic associations as equal evidence. A famous cultural
association is only a lead until a narrow experiment supports it.

### 4. Test One Attack Surface at a Time

Use this order unless the puzzle strongly contradicts it:

1. direct decoding of clue lines
2. exact-quote lookup for readable clue phrases
3. direct password candidates
4. password plus salt or AAD combinations
5. framing changes
6. KDF changes
7. algorithm-family changes

Do not mutate all variables at once. If a batch fails, know what just got
weaker.

### 5. Update the Frontier Explicitly

After each batch, write a short summary:

- confirmed facts
- discarded hypotheses
- surviving hypotheses
- single best next experiment

If a clue fails as a direct password, downgrade it to:

- intermediate clue
- salt or AAD candidate
- thematic confirmation

Do not keep re-testing it as if nothing changed.

## Scripts

### `scripts/probe_payload.mjs`

Use for quick shape analysis of suspicious strings.

- detects likely base64, base64url, hex, and base32
- prints decoded byte lengths and edge bytes
- helps decide whether the blob looks like AEAD, CBC, or something else

### `scripts/decode_text_clues.mjs`

Use for fast clue triage.

- tries reverse, ROT13, ROT47, URL decode, base64, and hex
- also tries reverse-plus-ROT variants
- good for lines that look “garbled but textual”

### `scripts/run_aead_matrix.mjs`

Use for modern 12-byte nonce AEAD experiments driven by a JSON config.

Current scope:

- framings:
  - `direct12`
  - `salt16_nonce12`
- algorithms:
  - `aes-128-gcm`
  - `aes-192-gcm`
  - `aes-256-gcm`
  - `chacha20-poly1305`
- derivations:
  - `sha256`
  - `sha512-32`
  - `pbkdf2-sha1-10000`
  - `pbkdf2-sha256-10000`
  - `pbkdf2-sha256-100000`
  - `scrypt`

Minimal config shape:

```json
{
  "ciphertext": "...",
  "ciphertextEncoding": "base64",
  "secrets": ["candidate-1", "candidate-2"],
  "salts": ["", "13mm"],
  "aads": ["", "N_0mpxB5iVQ"]
}
```

If this script returns zero authenticated hits, narrow the next hypothesis
instead of blindly expanding the matrix.

## Hard Rules

- Distinguish confirmed facts from hypotheses in the response.
- Do not present the challenge as solved unless a decryption or derivation
  actually works.
- Prefer keep or discard language over vague “maybe all of these”.
- If a clue is clearly an intermediate pointer, say so and stop treating it as
  the final answer.
- Use web search only for source attribution or current public facts; do not let
  web speculation replace local verification.

## Read Next

- [references/hypothesis-loop.md](references/hypothesis-loop.md)
- [references/clue-taxonomy.md](references/clue-taxonomy.md)
- [references/common-framings.md](references/common-framings.md)
