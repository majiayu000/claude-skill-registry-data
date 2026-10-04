---
name: agent-ready-go
description: >
  Prepares Go applications to work effectively with AI coding agents. Use when
  setting up a new Go project or retrofitting an existing one to ensure:
  structured JSON logging (slog/Zap/ZeroLog/Logrus), machine-readable command
  output, thorough golangci-lint configuration, non-interactive CLI design with
  --yes flags, structured error handling with meaningful exit codes, proper
  context.Context propagation, graceful shutdown, health check endpoints, and a
  standardized Makefile. Triggers when a user asks to make their Go app
  "agent-ready," "AI-friendly," wants to improve agent tooling/observability in
  a Go project, or needs to audit an existing Go project against agent-readiness
  best practices.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Agent-Ready Go

Make Go applications work effectively with AI coding agents by ensuring all
tooling produces machine-readable output, errors are structured, and commands
run non-interactively by default.

## Workflow

Making a Go app agent-ready involves these steps:

1. **Audit** — identify gaps against the agent-readiness checklist
2. **Structured logging** — add/configure slog, Zap, ZeroLog, or Logrus with JSON output
3. **Machine-readable output** — ensure all commands can emit JSON
4. **Linting** — add `.golangci.yml` with thorough config
5. **Testing** — ensure `go test -race -count=1 -timeout=5m` with coverage thresholds
6. **Error handling** — structured errors, meaningful exit codes
7. **Non-interactive design** — `--yes`/`-y` flags, env vars over prompts
8. **Makefile** — standardize `build`, `test`, `lint`, `cover` targets

For greenfield projects, apply all steps. For existing projects, run the audit
first and address only what's missing.

## Step 1: Audit

Run this checklist against the project. Address each ❌:

- [ ] Structured logger configured (slog / Zap / ZeroLog / Logrus)
- [ ] Logger outputs JSON when not a TTY or when `LOG_FORMAT=json`
- [ ] CLI commands support `--json` or `--output json` flag
- [ ] `.golangci.yml` exists with a thorough linter set
- [ ] `go test -race` passes
- [ ] Code coverage ≥ 80% enforced
- [ ] `go vet ./...` passes clean
- [ ] All errors wrapped with context (`fmt.Errorf("...: %w", err)`)
- [ ] Exit codes: 0 = success, non-zero = failure (no panics in CLI entry)
- [ ] `context.Context` threaded through all I/O-bound functions
- [ ] Interactive prompts have `--yes`/`-y` bypass flag
- [ ] `Makefile` with `build`, `test`, `lint`, `cover`, `ci` targets
- [ ] Graceful shutdown on SIGTERM/SIGINT (HTTP services)
- [ ] Health check endpoints (`/healthz`, `/readyz`) for HTTP services
- [ ] `govulncheck ./...` passes clean
- [ ] `NO_COLOR` respected; no ANSI codes in non-TTY output
- [ ] Config loaded from env vars with validation at startup

## Step 2: Structured Logging

See [references/logging.md](references/logging.md) for setup patterns for slog,
Zap, ZeroLog, and Logrus.

Key requirements:

- Use JSON format when `!isatty(os.Stdout.Fd())` or `LOG_FORMAT=json`
- Include fields: `level`, `ts`, `msg`, plus context fields
- Never use `fmt.Println` for operational log output
- Log to **stderr**; keep stdout clean for machine-readable data

## Step 3: Machine-Readable Output

Agents parse stdout to validate results. Every non-trivial command must support
JSON output.

```go
var outputJSON bool
cmd.Flags().BoolVar(&outputJSON, "json", false, "output results as JSON")

if outputJSON {
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    _ = enc.Encode(result)
} else {
    fmt.Printf("Created: %s\n", result.Name)
}
```

Rule: structured data → stdout; progress/human messages → stderr.

```go
fmt.Fprintln(os.Stderr, "Processing...")  // progress to stderr
json.NewEncoder(os.Stdout).Encode(result) // data to stdout
```

## Step 4: Linting

Copy [assets/.golangci.yml](assets/.golangci.yml) to the project root, then:

```bash
golangci-lint run ./...
```

Requires golangci-lint v1.59+ (v1.x series).

See [references/testing.md](references/testing.md) for linter explanations and
tuning guidance.

## Step 5: Testing

See [references/testing.md](references/testing.md) for full testing setup.

```bash
go test -race -count=1 -timeout=5m -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | tail -1
```

Enforce minimum coverage in CI:

```bash
COVERAGE=$(go tool cover -func=coverage.out | tail -1 | awk '{print $3}' | tr -d '%')
[ $(echo "$COVERAGE >= 80" | bc -l) -eq 1 ] || { echo "Coverage ${COVERAGE}% < 80%"; exit 1; }
```

## Step 6: Error Handling

See [references/error-handling.md](references/error-handling.md) for structured
error patterns and exit code conventions.

Quick rules:

- Always wrap: `fmt.Errorf("loading config: %w", err)`
- CLI `main()` catches all errors and exits with appropriate code
- Never call `os.Exit` deep in business logic — return errors up
- Never `panic` outside of `init()` / package-level setup

## Step 7: Non-Interactive Design

See [references/non-interactive.md](references/non-interactive.md) for patterns.

Any prompt that blocks agent execution must have a `--yes`/`-y` bypass:

```go
if !yes {
    confirmed, _ := promptConfirm("Delete all records?")
    if !confirmed {
        return nil
    }
}
// proceed
```

## Step 8: Makefile

Copy [assets/Makefile](assets/Makefile) to the project root. Adjust
`BINARY_NAME` and `MAIN_PKG` for the project.

Standard targets: `make build`, `make test`, `make lint`, `make cover`,
`make ci` (runs full pipeline).

## Resources

| File | Contents |
| ---- | -------- |
| [references/logging.md](references/logging.md) | slog, Zap, ZeroLog, Logrus JSON setup |
| [references/testing.md](references/testing.md) | Race detector, coverage, golangci-lint tuning |
| [references/error-handling.md](references/error-handling.md) | Structured errors, exit codes, context |
| [references/non-interactive.md](references/non-interactive.md) | `--yes` flags, env vars, stdin detection |
| [references/services.md](references/services.md) | HTTP graceful shutdown, health checks, OTel, request ID |
| [references/config.md](references/config.md) | Configuration management, env var parsing, validation |
| [assets/.golangci.yml](assets/.golangci.yml) | Production-ready linter config |
| [assets/Makefile](assets/Makefile) | Standard build/test/lint/cover targets |
