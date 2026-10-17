---
name: rust-pro-max
description: "Rust development intelligence. 14 domains, 11 stacks, 300+ entries. Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check Rust code. Domains: pattern, crate, error, perf, test, concurrency, traits, arch, idiom, anti, tooling, module, unsafe. Stacks: web-axum, web-actix, web-rocket, web-warp, cli, grpc, database, async-runtime, auth, wasm, embedded. Integrations: arch_system generator."
---

# Rust Pro Max - Backend Generator

## When User Requests Rust Work

Follow this workflow for every Rust-related task:

### 1. Analyze Requirements
Extract from the user's request:
- **Project type**: REST API, CLI, microservice, library, WebAssembly, Embedded
- **Domain**: web, database, gRPC, messaging
- **Scale**: small project, enterprise, library

### Default Stack (always use unless user specifies otherwise)
| Component | Default | Crate |
|-----------|---------|-------|
| **Database** | **PostgreSQL** | `sqlx` (async, compile-time checked) |
| **Router/Web** | Axum | `axum` + `tokio` |
| **Serde** | JSON Serialization | `serde` + `serde_json` |
| **Tracing** | Logging | `tracing` + `tracing-subscriber` |
| **Config** | ENV limits/Config | `figment` or `dotenvy` |
| **Error Handling**| General | `thiserror` (lib) / `anyhow` (app) |
| **Deploy** | Docker Compose | `Dockerfile` + `docker-compose.yml` |

**Project structure**: Domain-driven layout:
```
src/main.rs
src/lib.rs
src/config/      — env config & setup
src/domain/      — structs + traits
src/handlers/    — HTTP handlers (Axum)
src/services/    — business logic
src/repository/  — SQLx queries and DB access
migrations/      — SQL migration files
```

### 2. Generate Architecture System (REQUIRED for new projects)
```bash
python3 skills/rust/scripts/search.py "<project description>" --arch-system -p "ProjectName"
```
This gives you: architecture, crates, error strategy, patterns, structure, testing approach.

### 3. Supplement with Domain Searches
Based on the project needs, search relevant domains:
```bash
# Patterns for the task
python3 skills/rust/scripts/search.py "builder pattern newtype" --domain pattern

# Crates recommendations
python3 skills/rust/scripts/search.py "web api authentication" --domain crate

# Concurrency patterns
python3 skills/rust/scripts/search.py "tokio channel pipeline" --domain concurrency

# Performance tips
python3 skills/rust/scripts/search.py "zero copy clone" --domain perf

# Testing patterns
python3 skills/rust/scripts/search.py "mocking traits" --domain test
```

### 4. Stack Guidelines
If using a specific framework/stack:
```bash
python3 skills/rust/scripts/search.py "middleware authentication" --stack web-axum
python3 skills/rust/scripts/search.py "clap subcommands config" --stack cli
python3 skills/rust/scripts/search.py "connection pool sqlx" --stack database
```

### 5. Implement
Apply all recommendations from the search results:
- Use recommended architecture and project structure
- Apply patterns (Builder, Newtype, Typestate, etc.)
- Follow error handling strategy (`thiserror` vs `anyhow`)
- Implement proper concurrency patterns with `tokio`
- Add tests using proper mocking and standard `#[test]`

### 6. Always Generate Docker Files
Every web project MUST include these files:

**Dockerfile** (multi-stage build):
```dockerfile
# Builder stage
FROM rust:1.80-alpine AS builder
WORKDIR /app
RUN apk add --no-cache musl-dev
COPY Cargo.toml Cargo.lock ./
# Dummy build to cache dependencies
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release && rm -rf src
COPY src ./src
COPY migrations ./migrations
RUN cargo build --release

# Runtime stage
FROM alpine:3.20
RUN apk add --no-cache ca-certificates tzdata
COPY --from=builder /app/target/release/app /usr/local/bin/app
COPY migrations /app/migrations
WORKDIR /app
EXPOSE 8080
CMD ["app"]
```

## Pre-Delivery Checklist

Before delivering Rust code, verify:
- [ ] `cargo check` passes
- [ ] `cargo clippy -- -D warnings` catches no issues
- [ ] `cargo test` passes
- [ ] No `.unwrap()` or `.expect()` used in production paths (use `?` operator)
- [ ] Appropriate borrowing vs owning used where applicable
- [ ] Types are separated into DTOs vs Domain models
- [ ] Error domains handled via Enums with `#[derive(Error)]` (`thiserror`)
- [ ] Asynchronous bounds correctly handled

## Quick Domain Reference

| Domain | When to Search |
|--------|---------------|
| `pattern` | Need a design pattern (builder, typestate, newtype) |
| `crate` | Choosing a library/crate for a use case |
| `error` | Error handling strategy, anyhow vs thiserror |
| `perf` | Performance optimization, zero-copy, allocations |
| `test` | Testing approach, property testing, mocking |
| `concurrency` | Tokio, Async-std, channels, atomics |
| `traits` | Trait design, bounds, associated types |
| `arch` | Project structure, hexagonal, workspaces |
| `idiom` | Rust conventions, naming, style |
| `anti` | Avoiding common mistakes, lifetime misuse |
| `tooling` | Rust tools, cargo, clippy, fmt |
| `module` | Modules, visibility, workspaces |
| `unsafe` | FFI, unsafe Rust guidelines |

## Resources

- **scripts/**: BM25 search engine, architecture system generator
- **data/**: 14 domains and 11 stacks with curated Rust entries
