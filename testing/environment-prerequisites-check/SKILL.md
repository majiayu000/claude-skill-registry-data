---
name: environment-prerequisites-check
description: >
  Use this at the start of any phase before launching agent waves, or when
  guardrails report SKIP / FAIL due to missing tools. Covers the language-
  adapter toolchain, SDK-pipeline-specific tools (security/supply-chain
  scanners, perf benchmarking, container runtime for integration tests),
  shared infrastructure (jq, git, Docker), and per-MCP availability.
  Triggers: prerequisites, phase-start, govulncheck, osv-scanner, staticcheck, benchstat, pip-audit, mypy, pytest, ruff, testcontainers, Docker, toolchain, missing tool.
version: 1.1.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [prerequisites, phase-start, language-pluggable, multi-tenant-saas]
cross_language_ok: true
---

<!-- The "phase-start prereq check" concept is language-neutral; the actual tool list resolves from the active language adapter's toolchain manifest (`go.json:toolchain` or `python.json:toolchain`). Tables below show Go and Python prerequisites side-by-side; the consumer-side frontend prerequisites (Node/Vitest/Playwright) apply to multi-tenant SaaS consumer apps that depend on the SDK. The leakage scripts honor `cross_language_ok: true`. -->


# environment-prerequisites-check


## SDK-pipeline additions — Go pack (checked when `target_language: go`)

| Tool | Phase needed | Install | Impact if missing |
|------|--------------|---------|--------------------|
| `go` (>=1.26) | all | https://go.dev/dl | HARD BLOCK |
| `govulncheck` | design, testing | `go install golang.org/x/vuln/cmd/govulncheck@latest` | G32 fails |
| `osv-scanner` | design | `go install github.com/google/osv-scanner/cmd/osv-scanner@latest` | G33 fails |
| `staticcheck` | impl | `go install honnef.co/go/tools/cmd/staticcheck@latest` | G44 downgrades to MEDIUM |
| `benchstat` | testing | `go install golang.org/x/perf/cmd/benchstat@latest` | benchmark delta fallback to raw diff |

## SDK-pipeline additions — Python pack (checked when `target_language: python`)

| Tool | Phase needed | Install | Impact if missing |
|------|--------------|---------|--------------------|
| `python` (>=3.12) | all | https://www.python.org/downloads | HARD BLOCK |
| `pip-audit` | design, testing | `pip install pip-audit` | G32-py fails |
| `safety` | design | `pip install safety` | G33-py fails |
| `mypy` (>=1.0) | impl | `pip install mypy` | G42-py fails (strict typing) |
| `ruff` | impl | `pip install ruff` | G43-py / G44-py fail |
| `pytest` (>=8) | testing | `pip install pytest pytest-asyncio` | G60-py fails |
| `pytest-benchmark` | testing | `pip install pytest-benchmark` | benchmark delta fallback |
| `pytest-repeat` | testing | `pip install pytest-repeat` | G63-py flake check fails |

## Shared (every pack)

| Tool | Phase needed | Install | Impact if missing |
|------|--------------|---------|--------------------|
| Docker / Podman | testing | OS package | testcontainers integration tests skipped |
| `jq` | feedback (baseline-manager) | OS package | baseline recompute uses language-native fallback |
| `git` (>=2.40) | all | OS package | HARD BLOCK (Rule 21) |

---



# Environment Prerequisites Check

Phase leads MUST verify runtime tool availability before launching agent
waves. Missing runtimes cause cascading guardrail failures that produce
zero quality signal.

## When to Use
- At the START of any phase (before Wave 1)
- When guardrails report SKIP or FAIL due to missing tools
- Used by: implementation-lead, testing-lead, frontend-lead, detailed-design-lead

## Origin
Feedback run-2: Missing runtimes caused cascading guardrail failures across
4 phases — Go runtime missing in implementation/testing, Node.js missing in
frontend (11 guardrails skipped, 100% skip rate), gcc missing in implementation.

## Go Phase Prerequisites

| Tool | Required By | Check Command | Install |
|------|------------|---------------|---------|
| `go` (1.26+) | All Go phases | `go version` | Download from golang.org |
| `gcc` | CGO-enabled builds, race detector | `gcc --version` | `apt install build-essential` |
| `golangci-lint` | lint-check guardrail | `golangci-lint --version` | `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest` |
| `gosec` | security-scan guardrail | `gosec --version` | `go install github.com/securego/gosec/v2/cmd/gosec@latest` |
| `go-mutesting` | mutation-score-gate | `go-mutesting --version` | `go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest` |
| `migrate` | migration-check guardrail | `migrate --version` | `go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest` |

## Frontend Phase Prerequisites

| Tool | Required By | Check Command | Install |
|------|------------|---------------|---------|
| `node` (20+) | All frontend phases | `node --version` | Download from nodejs.org |
| `npm` (9+) | Dependency management | `npm --version` | Bundled with Node.js |
| `tsc` | tsc-check guardrail | `npx tsc --version` | `npm install typescript` |
| `vitest` | vitest-check, coverage-gate | `npx vitest --version` | `npm install vitest` |
| `playwright` | E2E tests | `npx playwright --version` | `npx playwright install` |

## Verification Script Template

```bash
#!/bin/bash
# Phase prerequisites check — run before Wave 1
set -e
PHASE=$1
MISSING=()

check_tool() {
  if ! command -v "$1" &>/dev/null; then
    MISSING+=("$1")
    echo "FAIL: $1 not found (required for: $2)"
  else
    echo "PASS: $1 ($($1 --version 2>/dev/null | head -1))"
  fi
}

case "$PHASE" in
  implementation|testing)
    check_tool go "compilation, tests"
    check_tool gcc "race detector, CGO"
    check_tool golangci-lint "lint guardrail"
    ;;
  frontend)
    check_tool node "build, tests"
    check_tool npm "dependencies"
    ;;
esac

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "BLOCKER: ${#MISSING[@]} tools missing. Guardrails will produce zero quality signal."
  exit 1
fi
echo "All prerequisites satisfied."
```

## Missing Tool Impact Matrix

| Missing Tool | Guardrails Affected | Impact |
|-------------|-------------------|--------|
| `go` | compile-check, test-check, coverage-check, lint-check, all Go guardrails | 100% guardrail skip |
| `gcc` | race detector, CGO builds | Security: race conditions undetected |
| `golangci-lint` | lint-check | Code quality unverified |
| `node` | All frontend guardrails (11 total) | 100% frontend quality gate skip |
| `gosec` | security-scan | OWASP vulnerabilities undetected |

## Phase Lead Protocol

1. Run prerequisites check script at phase start
2. If tools are missing:
   a. Log a `"type":"event"` decision entry with severity "high" listing missing tools
   b. Estimate scope impact (how many guardrails will be affected)
   c. Decide: proceed with degraded quality gates OR block until tools are available
   d. If proceeding, log the decision with explicit risk acceptance
3. Include prerequisites status in the phase report

## MCP dependencies (optional, non-blocking)

MCP servers extend agent capability but are never on the correctness path. Phase leads check availability at phase start; any MCP unavailable → WARN entry in the decision log; pipeline proceeds with the documented fallback.

| MCP | Purpose | Health check | Fallback on miss |
|-----|---------|--------------|-------------------|
| `mcp__neo4j-memory__*` | Cross-run knowledge graph (feedback) | `docker ps --filter name=claude-neo4j --format '{{.Status}}'` returns "Up..." | JSONL writes under `evolution/knowledge-base/` and `runs/<id>/feedback/` (see `mcp-knowledge-graph` skill) |
| `mcp__serena__*` | Phase 0.5 type-aware symbol scans (Mode B/C) | Serena LSP index fresh (index timestamp newer than last `$SDK_TARGET_DIR` mtime) | Grep-based symbol extraction, flagged lower confidence |
| `mcp__code-graph__*` | Call-graph queries | Neo4j reachable at `bolt://localhost:7687` | Static `grep`/`go/ast`-based call-graph, marked degraded |
| `mcp__context7__*` | Current library docs at design time | Trivial `resolve-library-id` response within 5s | Rely on in-repo docs + agent training cutoff, emit WARN |

**Policy**: any MCP unavailable → WARN; pipeline proceeds. A missing MCP is NEVER a BLOCKER. Guardrail `G04 mcp-health` records the verdict at phase start; agents consult that verdict instead of probing per-call.
