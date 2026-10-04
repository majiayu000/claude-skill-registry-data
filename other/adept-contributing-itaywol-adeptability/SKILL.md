---
id: adept-contributing
description: "How to contribute to the adeptability (adept) Go CLI — build, the required pre-PR gates, conventional commits, and where things live. Apply when changing adept's own source, opening a PR, or adding a harness."
activation: agent
allowed-tools:
  - "Bash"
  - "Read"
  - "Edit"
---

# Contributing to adept

You are working on the `adept` CLI itself (Go 1.25, module
`github.com/itaywol/adeptability`). Read [AGENTS.md](../../AGENTS.md) for architecture and
invariants; this skill is the operational checklist.

## Build & run

```bash
go build ./...
go build -o /tmp/adept ./cmd/adept && /tmp/adept --help
```

## Gates you MUST pass before opening a PR (same as CI)

```bash
gofmt -l .            # must print nothing → fix with: gofmt -w .
go vet ./...
golangci-lint run     # config: .golangci.yml
go test -race ./...
go test -run E2E ./cmd/adept   # end-to-end against a freshly built binary
```

If any gate fails, fix it before pushing — CI runs the identical set on
ubuntu/macos/windows.

## Where things live

| You're changing… | Go there |
| --- | --- |
| public types / interfaces / sentinel errors | `pkg/adept/` (types only — no behavior) |
| canonical field shape | `pkg/adept/` struct tags **and** `pkg/adeptschema/*.schema.json` together |
| a command | `internal/cli/commands_*.go`; wire deps in `internal/cli/deps.go` |
| a harness renderer | `internal/render/<id>/` + golden fixtures in its `testdata/` |
| sync / drift logic | `internal/harness/orchestrator.go` |
| 3-way merge | `internal/merge/` |
| safety scanner | `internal/scan/` |

## Conventional commits (release-please reads these)

`feat:` → minor · `fix:`/`perf:` → patch · `feat!:`/`BREAKING CHANGE:` → major ·
`refactor:`/`docs:`/`chore:`/`test:`/`ci:` → no release. The squash-merge title becomes the
changelog entry, so write it well.

## Conventions

- Wrap errors with context: `fmt.Errorf("doing X: %w", err)`. Match with `errors.Is` against
  the sentinels in `pkg/adept/errors.go` — never on error strings. Add new sentinels there.
- No package-level state, no `init()` side effects: dependencies flow through `*Deps`.
- New behavior ships with tests; bug fixes ship with a regression test. Update golden
  fixtures in the same PR when output changes, and say why in the message.
- Don't hand-edit `CHANGELOG.md`, `.release-please-manifest.json`, or version strings —
  release-please owns them.
