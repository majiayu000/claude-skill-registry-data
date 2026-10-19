---
name: add-event-type
description: Add or extend an event type in Mathiz's event-sourced store (ent schema + EventMixin + owner scoping + repo + test mocks). Use when persisting a new kind of learner event or adding fields/queries to an existing one.
---

# Adding or extending an event type

Events are append-only, owner-scoped (multi-tenant), and ordered by a global
sequence. Follow every step — the failure mode of a missed step is a silent
cross-tenant data leak or five broken test packages.

## Checklist

1. **Schema** — `ent/schema/<name>_event.go`: embed `EventMixin` (gives
   `sequence`, `timestamp`, `owner_id`); plain fields only, **no ent edges**;
   new fields on existing schemas need `Default(...)` so old rows migrate.
   ```go
   func (XxxEvent) Mixin() []ent.Mixin { return []ent.Mixin{EventMixin{}} }
   ```
2. **Codegen** — `make generate` (never hand-edit generated `ent/*.go`;
   a hook blocks it).
3. **Store types** — `internal/store/repo.go`: add `XxxEventData` (write
   shape) and, if readable, `XxxEventRecord` (hydrated shape); add methods to
   the `EventRepo` interface.
4. **Repo impl** — `internal/store/<name>_event.go`:
   - Append: `seq, _ := r.seq.Next(ctx)` then builder with
     `SetSequence(seq).SetOwnerID(r.owner)` — **owner stamping is manual and
     mandatory**.
   - Query: ALWAYS start with `.Where(xxxevent.OwnerID(r.owner))` and support
     `QueryOpts` (Limit/After/Before/From/To). Aggregate in SQL (ent
     `GroupBy`+`Aggregate`), never load-all-and-count — these run per HTTP
     request in SaaS mode.
   - Raw SQL (rare): must be portable SQLite+Postgres; use
     `r.ownerPlaceholder()` for the bind marker.
5. **Test mocks** — interface changes break five hand-written mocks; add
   stubs in: `internal/gems/service_test.go`,
   `internal/mastery/service_test.go`, `internal/spacedrep/scheduler_test.go`,
   `internal/session/planner_test.go`,
   `internal/screens/session/session_test.go`.
6. **Owner-isolation test** — extend
   `internal/store/owner_scope_test.go`: two owners, writer's data invisible
   to the other. Use `testOwner(t, ...)` so the suite also passes against
   persistent Postgres.
7. **Verify** —
   ```bash
   go vet ./... && go test ./internal/store/ ./internal/gems/ ./internal/mastery/ \
     ./internal/spacedrep/ ./internal/session/ ./internal/screens/session/
   # And against real Postgres (see saas-e2e skill for pg-local.sh):
   MATHIZ_TEST_DATABASE_URL="postgres://postgres@127.0.0.1:5433/mathiz_test?sslmode=disable" \
     go test ./internal/store/
   ```

## Who writes events

Both drivers persist the same events — if you add a write, wire it in both:
- TUI: `internal/screens/session/session.go`
- Game: `internal/saas/game/manager.go`

Snapshot changes are separate: `store.SnapshotData` + each service's
`SnapshotData()` method + `saveSnapshot` in both drivers.
