---
name: xxhash-python
description: Use for writing, reviewing, debugging, or testing fast non-cryptographic hashing in Python with python-xxhash, including algorithm and seed selection, bytes encoding, streaming updates, digest representation, cross-system reproducibility, checksums, bucketing, and collision-aware identity. Do not use for passwords, signatures, MACs, authentication, adversarial integrity, or any cryptographic requirement.
argument-hint: "[xxhash checksum, fingerprint, partitioning, streaming, or compatibility task]"
---

# xxhash Python

Hashing is a protocol. Fix the algorithm, input byte encoding/framing, seed,
digest width, and output representation before writing code. xxHash is fast and
non-cryptographic; collisions and adversarial forgery remain possible.

## Boundary

Use this skill when the project imports `xxhash` or explicitly requests xxHash
for checksums, cache keys, deduplication candidates, sampling, or partitioning.
Do not use it for credentials, password storage, tokens, digital signatures,
HMAC, tamper-proof artifacts, untrusted integrity decisions, or security
boundaries. Use a cryptographic hash/MAC/password KDF as the actual requirement
dictates.

## Know the contract objects

| Object | Meaning | Use |
|---|---|---|
| `xxh32` / `xxh64` | Legacy-width stateful hash constructors | Compatibility with an existing declared protocol. |
| `xxh3_64` / `xxh3_128` (`xxh128`) | XXH3 stateful variants | New non-security protocols after compatibility/width choice. |
| One-shot functions | Stateless digest/hex/int functions over one bytes value | Small materialized inputs and explicit output form. |
| Streaming object | Mutable state with `update`, `digest`, `hexdigest`, `intdigest`, `copy`, `reset` | Incremental files/streams without loading all bytes. |
| Seed | Public deterministic algorithm parameter | Namespacing/compatibility, not a secret key or collision defense. |
| Digest representation | bytes, lowercase hex text, or integer | Must be fixed at storage/wire boundaries. |

Read [the hash contract](references/hash-contract.md) before hashing structured
values, text, files, or identifiers shared across systems.

## Ordered workflow

1. Classify the requirement as non-adversarial checksum, lookup key,
   deduplication candidate, bucketing, sampling, or security. Stop and leave
   xxHash when authenticity or collision resistance matters.
2. Recover any existing protocol from stored digests, other languages, schemas,
   fixtures, algorithm name, width, seed, byte order, and text encoding. Never
   upgrade an algorithm silently.
3. Define a one-to-one byte serialization for the logical input. Encode text
   explicitly; frame multiple fields with lengths or a canonical serializer.
4. Choose width from collision consequences and population size. A wider digest
   lowers accidental collision probability but never makes xxHash cryptographic.
5. Use one-shot hashing for a materialized bytes object; stream chunks for large
   files/streams. Chunk boundaries must not affect the digest.
6. Choose bytes, hex, or integer output at the boundary and keep it consistent.
7. Test an authoritative vector, chunk invariance, seed/encoding sensitivity,
   and collision handling at the application layer.

## Decision table

| Condition | Action |
|---|---|
| Existing digests/protocol | Match its exact algorithm, seed, framing, and representation. |
| New local non-security fingerprint | Prefer an installed XXH3 variant with sufficient width; record its exact name. |
| Small bytes payload | Use a one-shot helper when available in the pinned package. |
| Large file/stream | Create one hash object and call `update` for each bytes chunk. |
| Text input | Normalize only if the domain requires it, then `.encode("utf-8")`. |
| Multiple fields | Length-prefix or canonical-serialize them; never concatenate ambiguously. |
| Hash used as unique identity | Store/compare the original key or verify content on a digest match. |
| Hash controls a partition | Specify unsigned integer derivation and modulo/rendezvous rule; changing node count/algorithm reshards data. |
| Untrusted party can choose input and collision matters | Do not use xxHash for the decision. |

## Canonical anchors

```python
import xxhash


def fingerprint_text(value: str) -> str:
    payload = value.encode("utf-8")
    return xxhash.xxh3_128(payload, seed=0).hexdigest()
```

```python
from pathlib import Path

import xxhash


def fingerprint_file(path: Path) -> str:
    digest = xxhash.xxh3_128(seed=0)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

Verify these constructors in the installed python-xxhash version before use.
The same input bytes, algorithm, and seed produce the same digest whether
updated once or in chunks.

## Structured input framing

Naive concatenation is ambiguous: `("ab", "c")` and `("a", "bc")` both become
`b"abc"`. Encode field type/order and lengths, or use an already-specified
canonical serialization:

```python
def frame(parts: list[bytes]) -> bytes:
    return b"".join(len(part).to_bytes(8, "big") + part for part in parts)
```

Do not sort fields unless order is semantically irrelevant and the protocol
states that normalization. Avoid platform-dependent `repr`, native integer byte
order, locale encodings, and nondeterministic mapping/set iteration.

## Collision and concurrency rules

- A digest match is a candidate match, not proof of equality. Compare original
  keys/content when false equality is consequential.
- Width selection is a probability/risk decision. Never promise “collision
  free,” including for 128 bits.
- Seeds are public deterministic parameters. They can separate namespaces but
  do not make the hash keyed or secure.
- Do not share one streaming object across threads to combine unordered chunks.
  Even where internal state is protected, update order determines the digest.
- `digest()` returns bytes, `hexdigest()` text, and `intdigest()` an integer.
  Do not infer byte order by casting; follow the package's documented
  representation.

Read [streaming and testing](references/streaming-testing.md) and [the security
boundary](references/security-boundary.md).

## Version grounding and completion

Inspect `xxhash.VERSION`, `xxhash.XXHASH_VERSION`, and available constructors in
the project environment. The package was not installed in this foundry during
authoring, so runtime examples are official-source-grounded but unexecuted here.
Completion requires a named algorithm/width/seed, deterministic byte framing,
fixed output representation, chunk-invariant tests, a collision resolution
path where identity matters, and an explicit non-cryptographic boundary.

## References

- [Hash contract and framing](references/hash-contract.md)
- [Streaming and testing](references/streaming-testing.md)
- [Security boundary](references/security-boundary.md)
