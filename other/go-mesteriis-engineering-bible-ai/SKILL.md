---
name: go
description: "Applies Go rules for packages, explicit errors, interfaces, concurrency, tests, and tooling."
---

# Skill: go

## Purpose

Apply the shared engineering style to Go projects while respecting Go idioms: small packages, explicit errors, simple interfaces, and boring code.

## Inspect First

Before changing Go code, inspect relevant files when present:

- `go.mod`
- `go.sum`
- `Makefile`
- CI files
- `golangci-lint` config
- existing packages and tests

Infer:

- Go version;
- module layout;
- test style;
- lint tooling;
- dependency boundaries;
- context/error conventions.

## Style

- Follow existing package layout.
- Keep packages cohesive.
- Avoid `util`, `common`, and `helpers` dumping grounds.
- Prefer small interfaces defined near consumers.
- Prefer explicit dependencies over package-level mutable globals.
- Keep exported API surface intentional.
- Use `gofmt`/`go fmt` style.

## Errors

- Return errors explicitly.
- Wrap errors with useful context.
- Do not panic for normal operational failures.
- Do not discard errors with `_` unless intentionally safe and obvious.
- Preserve sentinel/domain errors when the project uses them.

## Context

- Pass `context.Context` through request/operation boundaries.
- Do not store context in structs unless the project has a deliberate pattern.
- Respect cancellation and timeouts.
- Avoid starting goroutines without lifecycle management.

## Interfaces

- Accept interfaces, return concrete types when appropriate.
- Define interfaces at the consumer boundary.
- Do not create large interfaces.
- Do not create interfaces only because one day the clouds may demand it.

## Concurrency

- Avoid shared mutable state without synchronization.
- Avoid goroutine leaks.
- Close channels from the sending side.
- Make ownership of channels and goroutines clear.

## Tests and Validation

Common commands, only when configured or clearly available:

```bash
go test ./...
go test -race ./...
go vet ./...
gofmt -w <files>
golangci-lint run
```

Report exact commands and results.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
