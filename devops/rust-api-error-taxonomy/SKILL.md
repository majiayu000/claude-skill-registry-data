---
name: rust-api-error-taxonomy
description: Design consistent Rust error types and propagation boundaries for libraries, CLI tools, and long-running services.
---

# Rust Api Error Taxonomy

## Goal

Expose errors that help callers recover without leaking implementation details or flattening important failure distinctions.

## Inputs to inspect

Public Rust APIs, current error enums, internal dependencies, CLI/service boundaries, and caller recovery requirements.

## Workflow

1. List failure modes by layer: invalid caller input, domain rejection, unavailable dependency, serialization, I/O, cancellation, timeout, and invariant violation.
2. Choose typed errors for cases where callers need programmatic handling. Preserve causal chains for debugging while avoiding public exposure of unstable internal implementation types.
3. Define conversion rules between domain errors, infrastructure errors, and presentation errors. Do not erase retryability, source location, or safe-to-display classification.
4. Review `?`, `map_err`, and broad `anyhow` usage at public API boundaries. Keep ergonomic context internally while maintaining an intentional public contract.
5. Add tests for stable error classification, source chaining, redaction of secrets, retry hints, and serialization or CLI exit mapping where relevant.

## Validation checklist

- [ ] Callers can distinguish expected business rejection from an operational fault.
- [ ] Public error contracts do not unintentionally depend on private crate implementation types.
- [ ] Sensitive connection strings, tokens, and user input are excluded from user-facing errors.
- [ ] Cancellation and timeout remain distinguishable from successful empty results.
- [ ] Error changes are considered API compatibility changes and versioned accordingly.

## Required output

Deliver an error taxonomy, proposed public/internal boundary, conversion rules, caller examples, compatibility notes, and test matrix.

## Boundaries and failure handling

Do not collapse all errors to strings too early; do not classify every unexpected failure as retryable.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
