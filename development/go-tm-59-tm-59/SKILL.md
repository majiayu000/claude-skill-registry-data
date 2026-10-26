---
name: go
description: Use when writing Go — command-line tools, small HTTP services with the standard library or Echo, WebAssembly builds with TinyGo, table-driven tests and single static binaries. Also use when choosing between Go's standard library and a framework, when a WASM build is too large, or when configuration should come from flags versus environment variables.
---

# Go

Default: current Go release, modules, standard library first (`flag`, `net/http`, `encoding/json`, `log/slog`), `go test`, `go vet`, `gofmt`.

## Setup

1. `go mod init example.com/tool`; keep `go.mod`'s `go` line at the version you test with.
2. Layout: `cmd/<tool>/main.go` for binaries, `internal/` for code no one else should import. Do not create `pkg/` by habit.
3. A user-level install (unpack the official tarball into a home directory) is enough; add it to `PATH` only for the shell that needs it.

## Command-line tools

- `flag` handles most tools; switch to a library only for nested subcommands.
- Let configuration come from a flag with an environment-variable default, e.g. `-file` defaulting to `$APP_DATA`; document both in `-h` with an example.
- Print an actionable message on empty input ("no records yet — add one with ...") rather than an empty table.
- Exit codes: `os.Exit(1)` for failures, `2` for usage errors.

## HTTP services

- Start with `net/http` and the method-aware `ServeMux` patterns (`GET /items/{id}`); add a framework only when middleware needs grow.
- Always set server timeouts (`ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`); the zero value means none.
- Pass `context.Context` from the request into every downstream call.

## WebAssembly

- Standard Go WASM includes the runtime and is several MB. TinyGo produces binaries in the hundreds of KB for compute-only code; check that the packages you use are supported by TinyGo before choosing it.
- Expose functions with `syscall/js` (or `//export` in TinyGo) and keep the JS/WASM boundary coarse: pass a whole problem, not one number per call.

## Testing

- Table-driven tests with `t.Run(name, ...)`; include argument-count and empty-input cases.
- `go test -race ./...` for anything with goroutines.
- Use `t.TempDir()` and `t.Setenv()`; they clean up automatically.

## Verification loop

1. `gofmt -l .` prints nothing; `go vet ./...` is clean.
2. `go test ./...` passes (with `-race` where relevant).
3. `go build` the binary and run it with `-h` and with a real input.

## Pitfalls

- **Loop variable capture** changed in Go 1.22 (each iteration has its own variable); old code and old toolchains differ — the `go` line in `go.mod` decides.
- **Nil interfaces:** an interface holding a typed nil pointer is not `nil`.
- **Maps are not safe for concurrent writes**; guard with a mutex or use channels.
- **`defer` in loops** runs at function end, not iteration end; wrap the body in a function.
- **JSON:** unexported fields are ignored silently; use struct tags and `DisallowUnknownFields` for strict input.
- **Time:** `time.Now()` includes a monotonic reading; compare with `Sub`, format with layouts based on `2006-01-02`.
