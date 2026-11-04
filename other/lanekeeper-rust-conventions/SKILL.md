---
name: lanekeeper-rust-conventions
description: How to write Rust in the Lanekeeper monorepo. Covers crate ownership, ports and in-memory fakes, error handling, async rules (bounded everything, timeouts, spawn_blocking plus rayon), the Secret wrapper, sqlx patterns (offline mode, keyset pagination, EXPLAIN snapshots), audit-in-transaction with outbox publishing, tracing without content, the testing tiers, and the dependency rules. Use this skill for any Rust change in crates/ — a new crate, endpoint, port implementation, query, background job, agent or sentinel code, or a test — even small ones. Most review failures in this repo come from skipping one of these conventions.
---

# Rust conventions for Lanekeeper

AGENTS.md lists the rules. This skill shows how to follow them in code, so that implementations look the same across agents and the reviewer agent can check them quickly. Templates are in `references/patterns.md`; copy from there rather than inventing new shapes.

## Before you write code

1. **Find your crate and owned paths** in your prompt's metadata table. Edit only those, plus tests, benches and fixtures under them.
2. **Find the ports you implement or consume** in `docs/interfaces.md`. Depend on `crates/ports` traits, never on a sibling crate's concrete types. In tests, use `ports::fakes`, behind the `fakes` feature.
3. **Find the S# and P# your prompt lists.** Every one needs a test or a benchmark you can point to in the PR.

## Shape of a crate

- `lib.rs` starts with `#![forbid(unsafe_code)]` and a doc comment that names the owning prompt.
- **Public API:**
  - feature crates expose `pub fn router(state: AppState) -> axum::Router`, plus service structs that implement ports;
  - nothing else is public unless another crate needs it through a port.
- **Errors:**
  - one `thiserror` enum per module boundary;
  - map errors to `application/problem+json` at the edge, in `crates/hub`'s error layer;
  - never put internal details (SQL, paths, stack traces) in a response;
  - log them, with the request id, instead.

## Async rules (the ones reviewers check first)

- **No blocking in async code.** Filesystem walks, hashing, parsing, diffing, gix calls and rayon batches all run inside `tokio::task::spawn_blocking`. Inside that, use rayon for CPU-heavy work.
- **Every external call has a timeout.** Wrap it in `tokio::time::timeout`. Retries use exponential backoff with full jitter and a maximum attempt count.
- **Everything is bounded:**
  - `tokio::sync::mpsc::channel(n)`, never `unbounded_channel`;
  - moka caches have a weigher and a maximum capacity;
  - queries have a `LIMIT`;
  - request bodies have a size limit.
- **Cancellation is safe.** A dropped future must not leave half-written state. Use transactions, and write to temp files then rename.
- **Large content uses `Bytes`, not `Vec<u8>` copies.** Blobs move through the system without cloning.

## Secrets

- Wrap tokens, session ids, keys and webhook URLs in `Secret<T>`, from `crates/domain`. It redacts itself in `Debug`/`Display` and zeroizes on drop.
- Compare secrets with `subtle::ConstantTimeEq`.
- Decrypt GitHub tokens only inside the owning user's request, and drop the plaintext before the response is built.
- Never put any secret into a `tracing` field, an error or an audit event. The log-capture tests will catch it, but don't rely on them.

## Database (sqlx)

- **Queries:** use `sqlx::query!` and `query_as!` so they're checked at compile time. After changing a query, run `cargo sqlx prepare --workspace` and commit the `.sqlx/` folder.
- **Pagination:** keyset only, never `OFFSET`. See the template in `references/patterns.md`.
- **Hot queries:** add an `EXPLAIN (FORMAT JSON)` snapshot test asserting there's no sequential scan on large tables (P12).
- **State changes:** one transaction that holds the change, `audit.record(&mut tx, …)` and `bus.publish_in_tx(&mut tx, …)`, then commit. Nothing is fanned out before the commit (D80).
- **Migrations:** these are contracts. Use the `lanekeeper-contract-change` skill.

## Tracing and metrics

- One `tracing` span per request or job, carrying the request id, user id (never the email in hot logs), swimlane and path.
- Never log file contents, doc text, tokens, or environment-variable values.
- Add RED metrics (rate, errors, duration) for new routes and jobs, with low-cardinality labels: route templates, not raw paths.

## Testing tiers

| Tier | Tooling | When |
|---|---|---|
| Unit | `#[test]`, proptest | Pure logic, validators, mappers |
| Golden | insta | Engine outputs, rendered views, API shapes |
| Integration | testcontainers Postgres 16 with pgvector | Repositories, transactions, audit chain, outbox |
| Conformance | `ports::conformance::<port>(impl)` | Every real port implementation |
| Fuzz | cargo-fuzz | Every parser or validator at a trust boundary |
| Benchmark | criterion, registered in `perf/budgets.toml` | Every hot path named by a P# |

Rules for all tiers:

- Test error paths, not just the happy path.
- No sleeps in tests. Inject a `Clock`, and use `tokio::time::pause`.
- Don't mock what you own. Use the port fakes.

## Dependencies

- **Prefer what's already in the workspace.** AGENTS.md lists the approved stack.
- **A new crate needs** a one-line justification in the PR, a pinned version at least 14 days old, a clean `cargo deny check`, and an entry under `[workspace.dependencies]`. Member crates use `dep.workspace = true`.

## Finish line

Run, in this order:

1. `cargo fmt --all`
2. `cargo clippy --all-targets -- -D warnings`
3. `cargo test --workspace`
4. `cargo sqlx prepare --check --workspace`
5. `just verify-NN`
6. `cargo xtask bench-check`

Paste the outputs into the PR, as AGENTS.md describes.
