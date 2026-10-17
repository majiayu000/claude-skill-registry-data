---
name: wycheproof-crypto-current
description: Integrate pinned Wycheproof vectors into cryptographic API regression tests, with explicit operation, result policies and provider-domain coverage accounting.
license: CC-BY-SA-4.0
metadata:
  status: experimental-unbenchmarked
---

# Wycheproof regression integration

Use externally specified vectors to check an existing cryptographic API. Choose
the primitive, operation, key representation and implementation before selecting
files. Authentication decryption, encryption and signature verification have
different expected behavior; an encryption success does not test rejection of a
modified authentication tag.

Pin the reviewed C2SP repository commit and exact vector/schema hashes. Current
files live under `testvectors_v1`; do not assume the project supplies executable
language harnesses or a tagged release. A submodule records a commit and needs a
deliberate update. Fetch with HTTP failure handling, verify bytes before atomic
publication, and keep inputs fixed throughout a comparison.

Validate the selected file against its schema and local reference closure before
calling the provider. Use the declared schema dialect, prohibit network schema
retrieval, and implement relevant custom formats: generic JSON Schema validators
can silently accept unknown formats. Hex byte strings need even-length, strict
hex encoding. Parse supported DER/PEM key structures with the provider and verify
that alternate representations describe the same key. Do not require invalid
signature vectors to have a valid signature length.

Require a nonempty selection, agreement with `numberOfTests`, unique positive
case IDs, supported algorithm/schema pairing and consistent group metadata.
Missing or malformed data is an integration failure. Returning `[]` on a missing
file can turn a parametrized test into an apparently successful empty run.

Declare API-domain restrictions before execution. Separate unsupported inputs
from rejected cryptographic inputs, retaining every excluded ID and reason.
Report selected, eligible, attempted, completed and excluded counts. A provider
subset passing is not the full vector file passing.

For each eligible case:

- `valid`: the operation must succeed with the specified output.
- `invalid`: the operation must produce the documented rejection for that API.
- `acceptable`: consult the algorithm's notes and choose an explicit policy.
  Where either acceptance or rejection is permitted, an accepted result must
  still have the specified output. Record this separately from valid/invalid
  results; do not leave an assertion-free test body.

Catch documented rejection exceptions only. Unexpected type, setup, resource or
internal failures are harness/provider errors, including for invalid inputs.
Preserve their diagnostics and fail the run. Unknown result labels fail input
validation.

For Python `cryptography` AESGCM, the qualified 50.0.2 API accepts 8..128-byte
nonces and uses a 128-bit tag. Its decryption input is `ct + tag`; compare accepted
plaintext with `msg`. Import `InvalidTag` from `cryptography.exceptions` and catch
it around decryption. A malformed or unauthenticated input's rejection must not
be inferred from successfully encrypting its expected plaintext. Qualify other
GCM tag sizes or nonce domains with an appropriate API rather than filtering
them invisibly.

For Ed25519, import the declared public key and verify `sig` against `msg`.
`InvalidSignature` is the documented rejection. Raw, DER, PEM and JWK fields can
provide independent key-consistency checks. Signature length is measured in
decoded bytes; a fixed hex-character count is not a generic EdDSA contract.

Exercise the adapter before relying on its totals: missing files, empty runs,
duplicate IDs/counts, malformed encodings, unsupported schema references/formats,
unknown results, incorrect accepted output and unexpected provider exceptions.
Include controls for acceptable outcomes if the selected real files lack them,
and label those controls as synthetic. Require every eligible ID to reach a
completed result. Record provider/runtime versions, exclusions and failures with
the input hashes.

Review vector/provider updates into new pins and rerun integration controls.
Treat newly discovered mismatches as evidence to investigate, rather than
changing expected results or deleting cases to obtain a pass. Wycheproof checks
known failure classes; it does not establish constant-time behavior, complete
cryptographic safety or better coding-agent performance.

See [qualification and primary contracts](references/qualification.md). Original
instructions and their license remain included as provenance.
