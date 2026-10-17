---
name: vector-forge-current
description: Design cryptographic regression vectors for reproducible surviving mutants using operation-specific contracts, independent oracles and complete campaign accounting.
license: CC-BY-SA-4.0
metadata:
  status: experimental-unbenchmarked
---

# Mutation-guided cryptographic vectors

Use for a specific cryptographic implementation, operation and reproducible
test gap. Establish the protocol/API contract and accepted input domain before
generating vectors. Record provider, backend, compiler, build mode, source,
dependencies, tests and vector hashes. Upstream case-study counts are hypotheses
to reproduce, not measured results for this target.

Qualify the actual harness and selected mutation tool in a bounded disposable
environment. Require green unmodified tests, successful test discovery and
nonempty case execution. FFI adapters have their own buffer, length, error and
representation contracts; verify which implementation each test invokes. Keep
cross-package tests, optimized code and assembly exclusions explicit. Adjust
timeouts from baseline measurements and retain timed-out/error outcomes.

Freeze mutant identities and exact edits for before/after comparisons. Keep all
generated, excluded, attempted, completed, killed, survived, untested and failed
counts. A tested-only kill rate is not source coverage or a full campaign pass.
The qualified Python path and uncertainty-aware triage are described in the
Genotoxic improvement overlay; other language integrations need their own
released CLI/schema and runtime qualification.

Map edits to frozen source locations and mathematical operations. Use graph
context to prioritize investigation; zero callers or an unmapped location does
not establish dead code or a false positive. Preserve ambiguous mappings and
every related mutant/removal record. Establish equivalence from the operation's
types, input domain and side effects rather than a syntactic heuristic.

Choose vector families from the actual defect and specification: carry/borrow
boundaries, modulus and order boundaries, reduction, aliasing, malformed
encodings, validation ordering and supported key/message representations.
Use integer, algebraic or independently implemented reference operations to
compute expected results. Identify shared backends and algorithms between
references; agreement between two wrappers over one backend is weak evidence.

State expected acceptance, rejection and output separately for each operation.
Identity points, zero scalars, duplicate aggregate messages and noncanonical
encodings depend on the protocol and API. KEM implicit rejection may return a
defined output rather than an exception. Roundtrip byte equality is appropriate
only for an encoding/API with a canonical roundtrip contract. Assert correct
accepted outputs and documented rejection; unexpected setup/internal failures
remain harness errors, including on malformed inputs.

For a reduced limb model, specify the full-width field/order, radix, reduction
and operation first. Demonstrate that the reduction preserves the property
being tested. Retest exported cases against the actual full-width API and an
appropriate independent oracle. A distinguisher for one injected model fault
does not prove coverage of every implementation of that fault class.

Do not assume Montgomery representation makes selected internal residues
unreachable. When the public API represents every canonical field/scalar value
and the internal mapping is `m = x * R mod q` with invertible `R`, choose
`x = m * R^-1 mod q` and verify conversion through the actual API. Inspect its
normalization, endian, representation and domain contracts first. A mathematical
construction is not evidence that a particular library exposed or executed it.

Design single-fault rejection cases to distinguish targeted validation paths,
alongside realistic combined faults where useful. Identify which unchanged
checks also reject a candidate; otherwise a surviving mutation may remain
undistinguished. Keep regression cases for real defects even if a chosen
mutation operator does not model them or a campaign finds no surviving mutant.

When contributing to current Wycheproof, pin its commit/schema and use the
`vectorgen` envelope workflow and its `fmt --check`/`lint` commands. Verify the
pinned guide and supported Go release before invoking it; do not reuse obsolete
`reformat_json.py` instructions. `vectorgen` assigns case IDs and maintains
counts and formatting. Local API integration still needs schema closure,
custom-format validation, explicit result policies and excluded-ID accounting.

Add the vectors to the real harness, then run the fixed mutant set under the
same source/configuration and resource policy. Record per-ID transitions and
remaining untested/excluded/errors. Also run relevant unmodified integration
tests. Separate measured vector/harness results from constant-time analysis,
security completeness, generic fault-class coverage and coding-agent efficacy.

See [qualification and scope](references/qualification.md). This overlay is
experimental and has no measured coding-agent improvement claim.
