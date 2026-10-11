---
name: mvsep-api-contract
description: Check or change MVSEP endpoint integration, response parsing, transfer behavior, and English API documentation in this repository.
---

# MVSEP API contracts

Use repository-root paths below. Read only the files relevant to the affected endpoint.

Reuse [find-docs](../find-docs/SKILL.md) for library API details and [testing](../testing/SKILL.md) for test design. This skill adds MVSEP contract and source locations.

## Find the contract

- `doc/mvsep_api_endpoints.md` is an English reference captured on 2026-06-27, not proof of current server behavior. When changing remote contracts, verify the relevant upstream documentation or a sanitized captured response. Preserve the capture date when translating documentation.
- `src-tauri/src/main.rs` contains Tauri commands, remote parsing, and task orchestration. Match its command arguments/events with `src/app/backend/gateway.ts`, `src/app/types.ts`, and the affected frontend service.
- `test-api/src/file_transfer.rs` implements streaming transfers, resume, cancellation, output naming, and structured errors. Read its signatures before copying README examples.
- `test-api/src/db/` contains separate algorithm, task, and user-configuration stores. Follow the affected repository methods and migrations rather than treating the stores as interchangeable.

Distinguish create responses (`data.hash`) from result responses (`data.files`). Check whether the actual payload uses `link` or `url` before changing download parsing. Retrieve algorithm IDs, parameter options, and defaults from the algorithms endpoint rather than inventing them.

## Verify the change

Use local fixtures for response parsing and a local HTTP server for transfer behavior where practical. A task creation call uploads user data and may spend credits; make such calls only within the user's authorized scope. Never put tokens or unredacted authenticated responses in committed fixtures or logs.

Choose checks appropriate to the change:

```bash
cargo test --manifest-path test-api/Cargo.toml
cargo test --manifest-path src-tauri/Cargo.toml
npm run build
```

For public Rust API documentation, run both:

```bash
cargo doc --manifest-path test-api/Cargo.toml --no-deps
cargo test --manifest-path test-api/Cargo.toml --doc
```

Keep public API prose and examples in English. Retain wire keys, status values, types, and required/optional distinctions. Examples labeled `json` must parse as JSON; use prose outside the block for annotations. State which checks ran and distinguish local contract verification from live API validation.
