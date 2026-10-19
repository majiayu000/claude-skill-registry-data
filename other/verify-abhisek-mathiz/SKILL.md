---
name: verify
description: Verify a Mathiz change end-to-end before committing — which builds, tests, and live flows to run for each area of the codebase. Use before committing any nontrivial change.
---

# Verifying changes in this repo

Always: `CGO_ENABLED=0 go build ./... && go vet ./...`, then the matrix below.
`gofmt -w` only the files you touched. Known-unrelated failure: the
`internal/selfupdate` suite fails in proxied sandboxes — everything else
must pass.

| You changed | Run |
|---|---|
| Domain engine (`session`, `mastery`, `spacedrep`, `problemgen`, `gems`, `lessons`, `diagnosis`, `skillgraph`) | `go test ./internal/...` — the engine is fully unit-tested with mocks. Skill graph edits: `go test ./internal/skillgraph/` FIRST (a bad seed panics every test binary). |
| `internal/store` or `ent/schema` | `make generate` if schemas changed; `go test ./internal/store/` on SQLite **and** on Postgres (`MATHIZ_TEST_DATABASE_URL=...`, bootstrap via `saas-e2e` skill's `pg-local.sh`); interface changes → also the five mock-owning packages (see `add-event-type` skill). |
| `internal/saas/**`, `cmd/serve.go` | `go test -race -count=2 ./internal/saas/...` (concurrency-heavy: game manager, play slots). Then the `saas-e2e` skill for a real browser pass over the affected flow. |
| `web/**` | `cd web && npm run build` (runs `tsc` — this is the type check). Then the `saas-e2e` skill: drive the changed page in Chromium and screenshot it; the SPA has no unit tests, the browser flow is the test. |
| TUI screens (`internal/screens`, `internal/app`, `internal/ui`) | `go test ./internal/screens/...`; visually: `MATHIZ_LLM_PROVIDER=mock ./bin/mathiz` needs a TTY — in headless sandboxes run it inside `tmux` or `script -c`. |
| `cmd/` (CLI) | `make mathiz && ./bin/mathiz stats --db /tmp/smoke.db` is a cheap no-TTY smoke (opens store, migrates, renders). |

## Judgment calls

- Anything touching owner scoping or authz: add/extend a two-owner isolation
  test and a cross-tenant 404 API test — passing single-owner tests prove
  nothing about leaks.
- Race detector is not optional for `saas` changes; it caught real bugs here
  (`tea.Program.Kill` vs startup, session-cap check-then-act).
- A screenshot from the `saas-e2e` flow is the deliverable for UI claims —
  "it builds" is not "it works".
- Money paths (`internal/saas/credits`, `internal/saas/billing`, `Charge`
  hooks): idempotency IS the test — replay the same webhook event / ledger
  source and assert the balance is unchanged; also cover insufficient
  balance (must write nothing, surface 402). `TestBillingLifecycle` in
  `internal/saas/server/billing_api_test.go` is the pattern; the
  `add-billing-provider` skill has the full checklist.
