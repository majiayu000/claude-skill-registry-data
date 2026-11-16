---
name: go-review
description: Review Go code for language-level defects, including goroutine leaks, data races, unchecked or shadowed errors, context misuse, nil map writes, defer in loops, and unsafe concurrency patterns, and report findings with severity and file locations. Use when asked to review Go code, a Go diff, package, or service for Go-specific correctness and concurrency problems. Do not use for general reviews that also need security and maintainability coverage (use agent-kit:code-review), for non-Go code, for SQL data-access review (use agent-kit:go-sql-review), for writing new handlers (use agent-kit:go-http-api), or for fixing a known bug (use agent-kit:debugging); this skill reports and does not edit code.
---

# Go review

Report findings without modifying code unless the user asks for fixes. Read project instructions and `go.mod` for the Go version first; loop variable semantics changed in Go 1.22.

## 1. Determine the scope

Review the files, package, or diff the user named; otherwise the uncommitted changes and the current branch against its base. Read callers and tests for enough context.

## 2. Check

**Errors**

- Ignored errors (`_ =` or unchecked returns from `Close`, `Write`, `json.Unmarshal`), `err` shadowed with `:=` in an inner scope so the outer check sees `nil`, and errors compared with `==` instead of `errors.Is` after wrapping.
- `panic` used for ordinary errors in library code; `log.Fatal` outside `main`.

**Concurrency**

- Goroutines with no exit path: blocked sends on unbuffered channels nobody reads, missing `ctx.Done()` in loops. Channels closed by a receiver or closed twice.
- Data races: maps or slices written from several goroutines without a mutex, `sync.WaitGroup.Add` called inside the goroutine, copying structs that contain a `sync.Mutex`. Suggest `go test -race` to confirm.
- Before Go 1.22, closures in loops capturing the loop variable.

**Context and resources**

- Before Go 1.23, `time.After` in long loops keeps each timer alive until it fires; use `time.NewTimer` with `Stop` or `Reset`.
- `context.Background()` used where a request context exists, `cancel` from `WithTimeout` not deferred, contexts stored in structs.
- `defer` inside a loop holding files or locks until the function returns; HTTP response bodies not closed; `http.Client` without a timeout.

**Correctness**

- Writes to a nil map, nil pointer dereferences after an error path, slices aliased through `append` on a shared backing array, integer conversion overflow, and `time.Time` compared with `==`.
- Interfaces holding a typed nil pointer compared with `nil`.

## 3. Verify and report

Confirm findings by tracing the code; run `go vet ./...`, `go build ./...`, and `go test -race ./...` when available. Report findings ordered by severity (critical, high, medium, low) with `file:line`, the problem, a concrete triggering scenario, and a fix. If there are no findings, say so and list what was checked.

## Examples

- Use: "Review internal/worker for concurrency bugs." "Check my Go changes for goroutine leaks."
- Skip: "Review the SQL in store.go." (agent-kit:go-sql-review) "Add a /health endpoint." (agent-kit:go-http-api)
