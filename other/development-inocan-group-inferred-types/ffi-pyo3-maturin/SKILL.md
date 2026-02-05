---
name: ffi-pyo3-maturin
description: Build or modify the Rust↔Python FFI using PyO3+maturin. Use for binding builds, smoke tests, and boundary validation workflow.
---

# PyO3 + maturin FFI Workflow

## Build

- `cd packages/python_viterbo && uv run maturin develop --manifest-path ../rust_viterbo/Cargo.toml`

## Test

- `cd packages/python_viterbo && uv run pytest -q tests/smoke`

## Contract and expectations

- See: `packages/rust_viterbo/docs/ffi-contract.md`
- Keep wrappers thin and convert types near the boundary.
- Validate inputs at the boundary, return structured errors.
- Avoid breaking Python-facing APIs without coordination.
