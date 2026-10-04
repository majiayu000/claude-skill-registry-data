---
name: rust-python-sdk
description: Use this skill when implementing or designing the Rust SDK, PyO3/Maturin bindings, Python package, pandas/numpy/Arrow interoperability, errors, type mappings, build workflow, tests, or notebook-first API for mine-rs.
---

# Rust and Python SDK skill

Use this skill for tasks touching Rust crates, PyO3 bindings, Python packaging or the user-facing Python SDK.

## Source of truth

Read these files first:

1. `docs/references/python-sdk-design.md`
2. `docs/references/repository-strategy.md`
3. `docs/references/architecture.md`
4. `AGENTS.md`

## Ownership model

- Rust owns mining logic.
- `mine-sdk` is the public Rust facade.
- `mine-python` is the PyO3/Maturin native binding crate.
- `python/miners` is the user-facing Python package.
- Python ergonomics may wrap Rust objects, but must not duplicate core calculations.

## Python UX goals

Design for:

- Notebooks.
- pandas/numpy interoperability.
- Arrow/Parquet workflows.
- Clear exceptions.
- Type hints.
- Discoverable methods.
- Explicit mining assumptions.

## Procedure

1. Implement or design core behavior in Rust first when it is domain logic.
2. Expose stable public types/functions through `mine-sdk`.
3. Map Rust errors into specific Python exceptions.
4. Keep PyO3 conversion code in `mine-python`.
5. Keep pure Python ergonomics, helpers and type hints in `python/miners`.
6. Add Rust tests for deterministic behavior.
7. Add Python tests for bindings, conversions and UX.
8. Document examples as conceptual unless they are executable.

## Interoperability checklist

For data interchange, decide:

- Is the source pandas, numpy, Arrow, CSV or Parquet?
- Are types preserved?
- Is metadata preserved outside the dataframe when needed?
- Are copies acceptable, or should zero-copy be pursued?
- How are nulls and invalid values handled?
- Are column names and units explicit?

## Error handling

Avoid generic catch-all behavior. Prefer explicit error types for:

- IO errors.
- Schema errors.
- Grid errors.
- Validation errors.
- Reblocking errors.
- Planning errors.
- Numeric/tolerance errors.

## Gotchas

- Do not make Python depend on agentic runtime packages.
- Do not expose internal crate details if `mine-sdk` can provide a stable facade.
- Do not let examples imply that APIs exist before implementation.
- Do not hide required mining columns behind guesses if ambiguity affects results.
