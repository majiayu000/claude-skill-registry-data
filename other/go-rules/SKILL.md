---
name: go-rules
description: "Go conventions for this project. Use when reading, writing, or reviewing files matching `**/*.go`, `**/go.mod`. Do not use for other files."
---

# Go conventions

- Match the project's Go version in `go.mod`, its module layout, and its linters (`golangci-lint` configuration if present). Keep code `gofmt`-formatted and `go vet` clean.
- Return errors instead of panicking; wrap them with context using `fmt.Errorf("...: %w", err)` and check them with `errors.Is` and `errors.As`. Never ignore a returned error without a comment saying why.
- Pass `context.Context` as the first parameter of functions that do I/O or may block, and respect cancellation. Do not store contexts in structs.
- Every goroutine needs a way to stop (context cancellation, a closed channel, or a `sync.WaitGroup` the caller waits on). Protect shared state with a mutex or confine it to one goroutine.
- `defer` closing of files, response bodies, and rows right after the error check, and unlocking right after locking. For files you write, check the error from `Close`.
- Prefer the standard library and the project's existing dependencies. Do not add modules without saying so.
- Run `go build ./...`, `go vet ./...`, and `go test ./...` (with `-race` where the project uses it) after changes.
