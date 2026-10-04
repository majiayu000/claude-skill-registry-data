---
id: adept-writing-tests
description: "How to write tests in the adept Go codebase — table-driven tests with testify, golden fixtures under testdata/, the cmd/adept e2e harness, temp-dir/HOME isolation, and coverage gates. Apply when adding or changing Go tests here. (matches: **/*_test.go)"
activation: agent
allowed-tools:
  - "Read"
  - "Grep"
  - "Edit"
  - "Write"
  - "Bash"
---

# Writing tests for adept

## Defaults

- **Table-driven** tests with `github.com/stretchr/testify/require`. One `t.Run(tc.name, …)`
  per case; name cases for the behavior they pin.
- Put unit tests in the same package (`package foo`) for white-box access; use
  `package foo_test` when you want to assert only the public surface.
- Use `t.TempDir()` for any filesystem work — never write into the repo or a shared path.
- No network in unit tests. Use `net/http/httptest` for HTTP clients, and the package's
  interfaces + fakes for `git`, the registry, and the LLM provider (see how `Deps` is wired).

## Golden fixtures

Renderers are pinned by golden files in each `internal/render/<id>/testdata/`. When you
change rendered output **on purpose**:

1. Update the fixture in the same PR.
2. Explain why in the commit message.

Never loosen an assertion to make a diff pass — fix the code or update the golden deliberately.

## End-to-end tests

`cmd/adept/*_test.go` build the real binary and drive commands against temp dirs with an
isolated environment:

```go
env := []string{
    "PATH=" + os.Getenv("PATH"),
    "HOME=" + t.TempDir(),          // isolate user config
    "ADEPT_LIBRARY=" + libRoot,     // isolate the library
}
```

Guard the slow ones so `go test -short` skips them:

```go
if testing.Short() { t.Skip("skipping e2e under -short") }
```

Assert on **observable behavior** — exit codes, files on disk, stdout/JSON — not internals.
Exit codes: `0` clean · `1` error · `2` drift/dirty or merge conflict.

## Run them

```bash
go test ./...                  # fast
go test -race ./...            # CI gate
go test -run E2E ./cmd/adept   # e2e only
go test -cover ./...           # per-package coverage
```

## Coverage gates

Keep ≥80% on `internal/render`, `internal/status`, `internal/budget`, `internal/locks`, and
`internal/canonical`. Prefer tests that would actually catch a regression (error paths, edge
cases, round-trips) over coverage-padding happy-path calls.
