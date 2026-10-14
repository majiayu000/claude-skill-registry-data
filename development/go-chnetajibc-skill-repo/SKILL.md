---
name: go
description: "Go: small consumer-defined interfaces, composition, explicit errors/context, goroutines/channels/mutexes, modules/workspaces. Prefer simple code over enterprise abstraction."
---

# go

Simple, explicit, boring Go: small packages, returned errors, structured concurrency.

## Activate when

- Writing, reviewing, or testing Go; module, concurrency, or HTTP decisions.

## Do NOT activate for

- Generic API design (see architecture/api-design); deployment (see cloud/*).

## Inspection

Read go.mod (release, deps), package layout (`cmd/`, `internal/`, domain packages), interface sizes, error handling patterns, and concurrency primitives in use.

## Decision rules

- Packages small and purpose-named; `internal/` for non-shared code; exported surface deliberate.
- Interfaces defined by consumers, kept tiny (1–3 methods); accept interfaces, return structs. Package boundary ≠ type boundary ≠ interface boundary: a package groups a capability, a type models data, an interface decouples a seam, and a runtime dependency (goroutine, network call) is the thing that actually needs bounding.
- Errors are values: wrap with context (`%w`), sentinel errors for caller decisions, no panics in libraries; `context.Context` carries deadlines/cancellation, never business data.
- Concurrency: goroutines + channels or `errgroup` with limits; `sync` primitives for tight sharing; no unbounded spawn; graceful shutdown via context.
- HTTP: stdlib server + middleware chain; handlers thin, logic in packages; timeouts on server and client.

## Procedure

1. Detect Go release from go.mod; research stdlib behavior for that release when uncertain.
2. Place code per language-modularity (Go section); keep interfaces consumer-side.
3. Table-driven tests; race detector on (`-race`); benchmarks for perf claims; `go vet` clean.
4. Verify: `go build ./...`, `go vet`, `go test -race ./...` green; `gofmt` clean; shutdown drill for servers.

## Failure modes

- Interface-per-struct ritual; `interface{}`/any soup; ignored errors (`_ =`); context carrying business values; goroutine leaks; init-function magic; enterprise layering with one implementation.

## Escalation

Version facts → research/documentation-search (registry: go); modules/proxies → package-management.

## References

- Registry: `../../research/documentation-search/references/framework-registry.yaml` (go).
- Related: `../../architecture/language-modularity/`, `../../backend/concurrency/`.
