---
description: "Build the Go project"
user-invokable: true
---

# /build

A skill for building the Go project.

## Default Behavior

```bash
make build
```

This internally runs `go vet ./...` → `go build -o bin/yorishiro-proxy ./cmd/yorishiro-proxy`.

## Argument Patterns

- `/build` — Run `make build`
- `/build clean` — Run `make clean && make build`

## Steps

1. Parse arguments
2. If `clean` is specified, run `make clean` first
3. Run `make build`
4. On success, display the binary path; on failure, report the error
