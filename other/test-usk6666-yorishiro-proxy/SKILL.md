---
description: "Run Go tests"
user-invokable: true
---

# /test

A skill for running Go tests.

## Default Behavior

```bash
make test
```

## Argument Patterns

- `/test` — Run tests for all packages (`make test`)
- `/test ./internal/connector/...` — Run specified packages only (`make ensure-ui && go test -race -v ./internal/connector/...`)
- `/test -cover` — Run with coverage (`make test-cover`)
- `/test -run TestName` — Run only a specific test (`make ensure-ui && go test -race -v -run TestName ./...`)

## Steps

1. Parse arguments
2. If `-cover` is specified, run `make test-cover`
3. If no arguments, run `make test`
4. If a package or `-run` flag is specified, run `make ensure-ui && go test -race -v <args>`
5. Display results and highlight any failures
