---
name: rust-review
description: Review Rust code or diffs for correctness, soundness, API compatibility, and maintainability. Use for review or audit requests; produce evidence-backed findings without rewriting code unless requested.
---

# Rust review

Review the requested file, crate, or diff and the surrounding contracts it affects. Follow repository instructions and the requested review format. This skill is independently usable; no companion skill is required.

## Establish scope and evidence

Inspect relevant callers, tests, Cargo manifests, toolchain/MSRV, supported features, and CI commands. Identify actual consumers and compatibility commitments; a `lib.rs` alone does not establish a published API. For a diff, attribute findings to changes or their consequences; keep unrelated pre-existing issues separate.

Run applicable repository checks when available. Otherwise start with `cargo fmt --check`, `cargo clippy --all-targets`, and relevant tests. Respect supported feature combinations and targets; do not assume `--all-features` is valid. Keep review-only work read-only except normal build/test artifacts. Do not apply formatting, fix code, change lint configuration, post reviews, or create commits without authorisation for those actions. Summarise relevant diagnostics and distinguish pre-existing failures from regressions.

## Review in risk order

1. Correctness: reachable bad-input paths, overflow/truncation, state transitions, error propagation, resource cleanup, and externally visible behaviour.
2. Soundness: pointer/reference invariants, unsafe boundaries, foreign ABI, aliasing, lifetime, thread access, and unwind behaviour. A safety comment supports review; its presence or absence does not establish soundness.
3. Concurrency: lock order, guards across suspension, blocking executor work, cancellation, bounded work, and shutdown ownership. Evaluate the actual runtime and invariants rather than banning particular types.
4. API contracts: compatibility, ownership, visibility, standard trait laws, feature behaviour, and errors callers can act on. Verify equality, hashing, and ordering agree semantically; custom ordering can agree with derived equality.
5. Maintainability: avoidable complexity, misleading documentation, and missing behavioural coverage with a credible consequence. Keep style preferences non-blocking and respect established conventions.

Read [references/risk-checks.md](references/risk-checks.md) before assessing unsafe/FFI, concurrency, custom trait contracts, or public API evolution. Ordinary reviews need not load it. Verify uncertain language rules or source citations against primary documentation; do not invent guideline identifiers.

## Report actionable findings

Each finding needs a precise location, triggering condition, concrete consequence, and smallest useful remedy. Include a short code change when it clarifies the remedy; do not force a patch where reasoning is clearer. Group repeated instances of the same failure mode. If an assumption determines validity, verify it or state the uncertainty instead of presenting it as fact.

Severity follows impact and reachability: demonstrated soundness defects, data loss, security failures, and contract-breaking behaviour outrank idiom or naming. An invariant-protected panic, intentional shared ownership, public data struct, or documented poison-recovery policy is not automatically a defect. Do not infer undefined behaviour from a style violation or classify a truncating cast as a panic.

Do not invent findings, fill a quota, or require a praise section. For clean code, say no actionable findings were found and state meaningful coverage limits. Follow the host's severity/location format when provided; otherwise use a concise list ordered by risk. End with checks actually run and material gaps. Cite a named rule only when verified and useful; evidence of the failure takes priority over guideline compliance.

## Attribution

Adapted from Morgan Linton's BeautifulRust; see [NOTICE.md](NOTICE.md) for provenance and [LICENSE](LICENSE) for the retained MIT notice.
