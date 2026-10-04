---
name: go-popular-libraries
description: "Vetted, production-ready Golang libraries and frameworks for common tasks. Helps you choose the right tool for the job."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:05:00 GMT
---

## Selection Criteria

1. **Standard Library First** — If `net/http` or `encoding/json` is enough, don't add a dependency.
2. **Maintenance Status** — Only use libraries with recent commits and active issue management.
3. **Community Adoption** — Favor well-known, battle-tested libraries over obscure ones.
4. **License** — Ensure the license (typically MIT, Apache 2.0, or BSD) is compatible with your project.
5. **Zero Dependency** — Libraries with few or no transitive dependencies are preferred.

## Recommended Libraries by Category

### Web / API
- **Router**: `chi`, `echo`, `gin`, or standard `net/http` (Go 1.22+).
- **Middleware**: `chi/middleware`.
- **Validation**: `go-playground/validator`.

### Database
- **PostgreSQL**: `jackc/pgx` (preferred over `lib/pq`).
- **SQL Helper**: `sqlx`, `squirrel` (query builder).
- **Migrations**: `golang-migrate/migrate`, `pressly/goose`.
- **Redis**: `redis/go-redis`.

### Observability
- **Logging**: `log/slog` (stdlib), `rs/zerolog`, `uber-go/zap`.
- **Metrics**: `prometheus/client_golang`.
- **Tracing**: `go.opentelemetry.io/otel`.

### Testing
- **Assertions**: `stretchr/testify`.
- **Mocking**: `uber-go/mock` (formerly gomock), `vektra/mockery`.

### CLI & Config
- **CLI**: `spf13/cobra`.
- **Config**: `spf13/viper`, `caarlos0/env`.

### Utilities
- **Functional**: `samber/lo` (the "lodash" for Go).
- **Errors**: `samber/oops` (contextual errors), `pkg/errors` (legacy).
- **Concurrency**: `sourcegraph/conc`.

## Anti-patterns

- ❌ **Using ORMs for everything** — GORM is powerful but often hides performance issues. Use `sqlx` or `pgx` for better control.
- ❌ **Deep wrapping** — Using a library that merely wraps a standard library function without adding significant value.
- ❌ **Abandoned libraries** — Check the last commit date before `go get`.
- ❌ **Huge dependency trees** — Be wary of "frameworks" that pull in hundreds of transitive dependencies.
