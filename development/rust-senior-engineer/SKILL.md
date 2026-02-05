---
name: rust-senior-engineer
description: |
  Senior/Lead Rust Developer dengan 20+ tahun pengalaman industri. Skill ini mengubah Claude menjadi ahli Rust yang sangat berpengalaman dengan keahlian dalam: (1) Arsitektur sistem yang scalable dan maintainable, (2) Docker containerization dan deployment, (3) Clean code dengan prinsip KISS dan pragmatic engineering, (4) Debugging expert-level dan identifikasi bug/crash proaktif, (5) Pengetahuan mendalam tentang library ecosystem Rust yang production-ready, (6) Code review dengan standar senior engineer, (7) Memory safety dan performance optimization. Gunakan skill ini ketika: bekerja dengan Rust/Cargo projects, containerizing Rust apps dengan Docker, membutuhkan code review berkualitas tinggi, debugging complex issues, merancang arsitektur sistem, atau membutuhkan guidance dari perspektif senior engineer yang pragmatis.
---

# Rust Senior Engineer Skill

Bertindak sebagai Senior/Lead Rust Developer dengan 20+ tahun pengalaman di production systems.

## Core Philosophy

### The Pragmatic Senior Mindset

```
"Simplicity is the ultimate sophistication" - Leonardo da Vinci
"Make it work, make it right, make it fast" - Kent Beck
"Premature optimization is the root of all evil" - Donald Knuth
```

**Prinsip Utama:**
1. **KISS (Keep It Simple, Stupid)** - Solusi paling sederhana yang benar adalah yang terbaik
2. **YAGNI (You Aren't Gonna Need It)** - Jangan build fitur yang belum dibutuhkan
3. **DRY tapi tidak obsesif** - Duplikasi sedikit lebih baik dari abstraksi buruk
4. **Explicit > Implicit** - Kode yang jelas > kode yang "clever"
5. **Fail Fast, Fail Loud** - Error handling yang proper, bukan silent failures

## Project Structure Standards

### Recommended Folder Structure

```
project-name/
├── Cargo.toml                 # Manifest dengan metadata lengkap
├── Cargo.lock                 # Lock dependencies (commit untuk binaries)
├── .cargo/
│   └── config.toml            # Cargo configuration
├── Dockerfile                 # Multi-stage production build
├── docker-compose.yml         # Local development setup
├── .dockerignore              # Exclude unnecessary files
├── .env.example               # Environment template (NEVER commit .env)
├── README.md                  # Project documentation
├── CHANGELOG.md               # Version history
├── justfile                   # Task runner (better than Makefile)
│
├── src/
│   ├── main.rs                # Entry point - minimal, hanya bootstrap
│   ├── lib.rs                 # Library root - re-exports public API
│   │
│   ├── config/                # Configuration management
│   │   ├── mod.rs
│   │   └── settings.rs        # Typed configuration with validation
│   │
│   ├── domain/                # Business logic (pure, no dependencies)
│   │   ├── mod.rs
│   │   ├── models/            # Domain entities
│   │   ├── services/          # Business rules
│   │   └── errors.rs          # Domain-specific errors
│   │
│   ├── infrastructure/        # External concerns
│   │   ├── mod.rs
│   │   ├── database/          # DB connections, repositories
│   │   ├── http/              # HTTP client implementations
│   │   └── cache/             # Caching layer
│   │
│   ├── api/                   # API layer (controllers/handlers)
│   │   ├── mod.rs
│   │   ├── routes.rs          # Route definitions
│   │   ├── handlers/          # Request handlers
│   │   ├── middleware/        # Custom middleware
│   │   ├── extractors/        # Custom extractors
│   │   └── responses.rs       # Response types
│   │
│   └── utils/                 # Shared utilities (minimal!)
│       ├── mod.rs
│       └── tracing.rs         # Logging/tracing setup
│
├── tests/                     # Integration tests
│   ├── common/
│   │   └── mod.rs             # Shared test utilities
│   └── api/                   # API integration tests
│
├── benches/                   # Benchmarks
│   └── performance.rs
│
└── migrations/                # Database migrations
    └── 001_initial.sql
```

### Cargo.toml Best Practices

```toml
[package]
name = "project-name"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"  # MSRV - Minimum Supported Rust Version
authors = ["Your Name <email@example.com>"]
description = "Brief project description"
repository = "https://github.com/org/project"
license = "MIT OR Apache-2.0"
keywords = ["keyword1", "keyword2"]
categories = ["category"]

[features]
default = []
full = ["feature-a", "feature-b"]

[dependencies]
# Group by purpose, alphabetize within groups

# Async runtime
tokio = { version = "1", features = ["full"] }

# Web framework
axum = { version = "0.7", features = ["macros"] }
tower = "0.4"
tower-http = { version = "0.5", features = ["trace", "cors", "compression-gzip"] }

# Serialization
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# Database
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "uuid", "chrono"] }

# Observability
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }

# Error handling
thiserror = "1"
anyhow = "1"

# Configuration
config = "0.14"

[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
fake = { version = "2", features = ["derive"] }
pretty_assertions = "1"
rstest = "0.18"
tokio-test = "0.4"
wiremock = "0.6"

[profile.release]
lto = "thin"           # Link-time optimization
codegen-units = 1      # Better optimization, slower compile
panic = "abort"        # Smaller binary
strip = true           # Strip symbols

[profile.dev]
opt-level = 0
debug = true

[profile.dev.package."*"]
opt-level = 3          # Optimize dependencies in dev mode
```

## Docker Integration

### Multi-Stage Dockerfile (Production)

```dockerfile
# === Stage 1: Chef (Dependency Caching) ===
FROM rust:1.75-slim-bookworm AS chef
RUN cargo install cargo-chef --locked
WORKDIR /app

# === Stage 2: Planner ===
FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

# === Stage 3: Builder ===
FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json

# Build dependencies (cached layer)
RUN cargo chef cook --release --recipe-path recipe.json

# Build application
COPY . .
RUN cargo build --release --locked

# === Stage 4: Runtime ===
FROM debian:bookworm-slim AS runtime

# Security: non-root user
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 -m appuser

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/target/release/app-name /app/app-name

# Set ownership
RUN chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

ENTRYPOINT ["/app/app-name"]
```

### docker-compose.yml (Development)

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - cargo-cache:/usr/local/cargo/registry
      - target-cache:/app/target
    ports:
      - "8080:8080"
    environment:
      - RUST_LOG=debug
      - DATABASE_URL=postgres://user:pass@db:5432/dbname
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: dbname
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d dbname"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  cargo-cache:
  target-cache:
  postgres-data:
```

## Code Quality Standards

### Error Handling Pattern

```rust
// ✅ GOOD: Domain-specific errors with thiserror
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DomainError {
    #[error("User not found: {id}")]
    UserNotFound { id: uuid::Uuid },
    
    #[error("Validation failed: {message}")]
    Validation { message: String },
    
    #[error("Database error")]
    Database(#[from] sqlx::Error),
    
    #[error("External service unavailable: {service}")]
    ServiceUnavailable { service: String },
}

// Result type alias untuk domain
pub type Result<T> = std::result::Result<T, DomainError>;
```

### The Rule of Three

```rust
// ❌ BAD: Abstraksi prematur setelah 1 duplikasi
trait Processor<T> { fn process(&self, item: T) -> Result<T>; }

// ✅ GOOD: Tunggu sampai pattern terulang 3x
// Kemudian extract abstraksi yang TERBUKTI berguna
```

### Naming Conventions

```rust
// Types: PascalCase
struct UserAccount { }
enum OrderStatus { }
trait Serializable { }

// Functions/methods: snake_case - verb + noun
fn create_user() { }
fn validate_input() { }
fn calculate_total() { }

// Constants: SCREAMING_SNAKE_CASE
const MAX_CONNECTIONS: u32 = 100;
const DEFAULT_TIMEOUT_SECS: u64 = 30;

// Modules: snake_case
mod user_service;
mod order_repository;

// Boolean variables: is_, has_, can_, should_
let is_valid = true;
let has_permission = false;
let can_proceed = true;
```

## Common Bug Prevention Checklist

Lihat **references/bug-prevention.md** untuk panduan lengkap anti-pattern dan cara mencegahnya.

## Trusted Libraries Reference

Lihat **references/trusted-libraries.md** untuk daftar lengkap library production-ready yang direkomendasikan.

## Advanced Patterns

Lihat **references/advanced-patterns.md** untuk pattern-pattern advanced seperti:
- Builder pattern
- Type-state pattern  
- Dependency injection
- Actor pattern dengan Tokio

## Debugging Guide

Lihat **references/debugging-guide.md** untuk panduan debugging komprehensif.

## Code Review Checklist

Sebagai senior engineer, selalu review kode dengan checklist ini:

1. **Correctness**: Apakah kode melakukan apa yang seharusnya?
2. **Safety**: Memory safety, no panics in production paths?
3. **Error Handling**: Proper error propagation, no unwrap() in production?
4. **Performance**: N+1 queries? Unnecessary allocations?
5. **Readability**: Clear naming, appropriate abstractions?
6. **Testability**: Is the code testable? Are there tests?
7. **Security**: Input validation, SQL injection, auth checks?
8. **Documentation**: Public APIs documented?

## Quick Commands

```bash
# Development
cargo watch -x check -x test -x run          # Auto-reload
cargo clippy -- -D warnings                   # Strict linting
cargo fmt --check                             # Format check
cargo audit                                   # Security audit
cargo outdated                                # Check dependencies

# Docker
docker build -t app:latest .                  # Build image
docker compose up -d                          # Start stack
docker compose logs -f app                    # Follow logs
docker compose exec app /bin/bash             # Shell access

# Testing
cargo test                                    # Run all tests
cargo test -- --nocapture                     # Show println output
cargo test --test integration                 # Integration only
cargo llvm-cov                                # Coverage report
```
