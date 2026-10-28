---
name: rust-port
description: Port existing C, C++, Python, Go, JavaScript, or TypeScript code to Rust while preserving its agreed observable behaviour. Use for requested Rust migrations or rewrites, not conceptual language comparisons or unrelated Rust edits.
---

# Rust port

Port the behaviour into idiomatic Rust. Keep the work within the requested module, interfaces, and deployment constraints. This skill is independently usable; an installed Rust writing skill may supplement it but is not required.

## Establish compatibility

Read the source, callers, tests, build configuration, and relevant data formats before editing. Identify the public operations, input domain, output bytes and ordering, error/absence semantics, numeric ranges, encoding, resource ownership, concurrency, and external interfaces that callers observe. Distinguish requirements from incidental implementation structure.

Run the original tests when practical and record the source revision and environment. If tests are missing, establish characterisation cases before replacing the implementation. Existing tests are evidence, not a complete definition of the supported contract.

Preserve specified behaviour and understood quirks unless the user authorises a change. Do not silently narrow accepted Unicode, whitespace, numeric ranges, missing values, or input sizes because Rust's defaults differ. Record a proposed difference and obtain agreement before relying on it; writing it in porting notes does not authorise it. If the contract is ambiguous, ask about the material ambiguity while progressing on independent parts. Do not reproduce source undefined behaviour or introduce Rust unsoundness to imitate it; identify the gap and establish defined behaviour.

## Translate evidence before implementation

Port the source tests first, keeping a traceable mapping to their Rust coverage. Test grouping can change if every original assertion and behaviour remains accounted for. Add boundary cases for semantic differences the translation could introduce, including empty/invalid inputs, ordering ties, overflow, and cleanup after partial failure.

Design Rust types and signatures from that contract, then implement against the tests. Prefer ownership and RAII, `Option` for absence, `Result` for expected failure, and enums for meaningful state distinctions. Preserve error data callers use; do not collapse distinct missing states or failure categories. Public errors in a std-based library implement `Display` and `std::error::Error`; explain the compatible alternative for other targets. Use borrowed slices or strings according to the actual data, not merely the source's spelling.

Before translating a language's representations, read only its relevant guide:

- [C and C++](references/c-and-cpp.md): bytes, pointers, ABI, buffers, and lifetimes.
- [Python](references/python.md): Unicode, integers, ordering, and exceptions.
- [Go, JavaScript, and TypeScript](references/go-and-javascript.md): nil/missing states, numbers, iteration, and concurrency.

Keep ordinary ports safe. Where an ABI or demonstrated requirement needs unsafe code, isolate it behind a sound boundary and document the invariants. Do not retain raw pointers simply because the source used them.

## Keep the design proportionate

Prefer standard Rust facilities when they satisfy the agreed contract. Use a small compatibility adapter where required, rather than recreating an entire source runtime. Avoid speculative builders, traits, public operations, and dependencies. Keep an existing algorithm unless a concrete requirement justifies a change, and verify any replacement preserves the agreed behaviour.

Investigate disproportionate growth as a design signal; do not enforce arbitrary source-to-Rust line-count ratios. Choose differential tests and fuzzing according to the input surface and risk. Do not dismiss discovered divergences as exotic without checking whether they are supported inputs.

## Verify and hand over

Run the project's documented Rust formatting, lint, build, and test checks with the supported edition, MSRV, features, and targets. If none are documented, start with `cargo fmt --check`, `cargo clippy --all-targets`, and `cargo test`; run builds or integration checks for the affected deliverables. Fix failures introduced by the port and distinguish existing failures or unavailable checks. Do not claim a command ran or passed when it did not.

When the original is executable, compare it with the port on representative and boundary inputs, covering returned values, error categories, ordering, and relevant side effects. Passing examples do not prove equivalence over every input. Report any remaining compatibility gaps explicitly.

Write concise `PORTING.md` notes, or use the repository's established migration document, with:

- API and test mappings, including how each original behaviour is covered.
- Preserved quirks, approved differences, and unresolved compatibility gaps.
- Verification commands and their actual results, including unavailable checks.

Check these notes against the final code before returning. Keep speculative improvements separate from the compatibility claim.

## Attribution

Adapted from Morgan Linton's BeautifulRust. See [NOTICE.md](NOTICE.md) for provenance and [LICENSE](LICENSE) for the retained MIT notice.
