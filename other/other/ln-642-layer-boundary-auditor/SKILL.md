---
name: ln-642-layer-boundary-auditor
description: "L3 Worker. Audits layer boundaries + cross-layer consistency: I/O violations, transaction boundaries (commit ownership), session ownership (DI vs local)."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Layer Boundary Auditor

L3 Worker that audits architectural layer boundaries and detects violations.

## Purpose & Scope

- Read architecture.md to discover project's layer structure
- Detect layer violations (I/O code outside infrastructure layer)
- **Detect cross-layer consistency issues:**
  - Transaction boundaries (commit/rollback ownership)
  - Session ownership (DI vs local)
- Check pattern coverage (all HTTP calls use client abstraction)
- Detect error handling duplication
- Return violations list to coordinator

**Out of Scope** (owned by ln-628-concurrency-auditor):
- Blocking I/O in async functions (sync open/read in async def)
- Fire-and-forget tasks (create_task without error handler)

## Input (from ln-640)

```
- architecture_path: string    # Path to docs/architecture.md
- codebase_root: string        # Root directory to scan
- skip_violations: string[]    # Files to skip (legacy)

# Domain-aware (optional, from coordinator)
- domain_mode: "global" | "domain-aware"   # Default: "global"
- current_domain: string                   # e.g., "users", "billing" (only if domain-aware)
- scan_path: string                        # e.g., "src/users/" (only if domain-aware)
```

**When domain_mode="domain-aware":** Use `scan_path` instead of `codebase_root` for all Grep/Glob operations. Tag all findings with `domain` field.

## Workflow

### Phase 1: Discover Architecture

**MANDATORY READ:** Load `../ln-640-pattern-evolution-auditor/references/layer_rules.md` — use Architecture Presets (fallback), I/O Pattern Boundary Rules (Phase 2), Coverage Checks (Phase 3), Cross-Layer Consistency rules (Phase 2.5).

```
Read docs/architecture.md

Extract from Section 4.2 (Top-Level Decomposition):
  - architecture_type: "Layered" | "Hexagonal" | "Clean" | "MVC" | etc.
  - layers: [{name, directories[], purpose}]

Extract from Section 5.3 (Infrastructure Layer Components):
  - infrastructure_components: [{name, responsibility}]

IF architecture.md not found:
  Use fallback presets from layer_rules.md

Build ruleset:
  FOR EACH layer:
    allowed_deps = layers that can be imported
    forbidden_deps = layers that cannot be imported
```

### Phase 2: Detect Layer Violations

```
scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root

FOR EACH violation_type IN layer_rules.md I/O Pattern Boundary Rules:
  grep_pattern = violation_type.detection_grep
  forbidden_dirs = violation_type.forbidden_in

  matches = Grep(grep_pattern, scan_root, include="*.py,*.ts,*.js")

  FOR EACH match IN matches:
    IF match.path NOT IN skip_violations:
      IF any(forbidden IN match.path FOR forbidden IN forbidden_dirs):
        violations.append({
          type: "layer_violation",
          severity: "HIGH",
          pattern: violation_type.name,
          file: match.path,
          line: match.line,
          code: match.context,
          allowed_in: violation_type.allowed_in,
          suggestion: f"Move to {violation_type.allowed_in}"
        })
```

### Phase 2.5: Cross-Layer Consistency Checks

#### 2.5.1 Transaction Boundary Violations

**What:** commit()/rollback() called at inconsistent layers (repo + service + API)

**Detection:**
```
repo_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/repositories/**/*.py")
service_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/services/**/*.py")
api_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/api/**/*.py")

layers_with_commits = count([repo_commits, service_commits, api_commits].filter(len > 0))
```

**Safe Patterns (ignore):**
- Comment "# best-effort telemetry" in same context
- File ends with `_callbacks.py` (progress notifiers)
- Explicit `# UoW boundary` comment

**Violation Rules:**

| Condition | Severity | Issue |
|-----------|----------|-------|
| layers_with_commits >= 3 | CRITICAL | Mixed UoW ownership across all layers |
| repo + api commits | HIGH | Transaction control bypasses service layer |
| repo + service commits | HIGH | Ambiguous UoW owner (repo vs service) |
| service + api commits | MEDIUM | Transaction control spans service + API |

**Recommendation:** Choose single UoW owner (service layer recommended), remove commit() from other layers

**Effort:** L (requires architectural decision + refactoring)

#### 2.5.2 Session Ownership Violations

**What:** Mixed DI-injected and locally-created sessions in same call chain

**Detection:**
```
di_session = Grep("Depends\(get_session\)|Depends\(get_db\)", "**/api/**/*.py")
local_session = Grep("AsyncSessionLocal\(\)|async_sessionmaker", "**/services/**/*.py")
local_in_repo = Grep("AsyncSessionLocal\(\)", "**/repositories/**/*.py")
```

**Violation Rules:**

| Condition | Severity | Issue |
|-----------|----------|-------|
| di_session AND local_in_repo in same module | HIGH | Repo creates own session while API injects different |
| local_session in service calling DI-based repo | MEDIUM | Session mismatch in call chain |

**Recommendation:** Use DI consistently OR use local sessions consistently. Document exceptions (e.g., telemetry)

**Effort:** M

---

### Phase 3: Check Pattern Coverage

```
# HTTP Client Coverage
all_http_calls = Grep("httpx\\.|aiohttp\\.|requests\\.", codebase_root)
abstracted_calls = Grep("client\\.(get|post|put|delete)", infrastructure_dirs)

IF len(all_http_calls) > 0:
  coverage = len(abstracted_calls) / len(all_http_calls) * 100
  IF coverage < 90%:
    violations.append({
      type: "low_coverage",
      severity: "MEDIUM",
      pattern: "HTTP Client Abstraction",
      coverage: coverage,
      uncovered_files: files with direct calls outside infrastructure
    })

# Error Handling Duplication
http_error_handlers = Grep("except\\s+(httpx\\.|aiohttp\\.|requests\\.)", codebase_root)
unique_files = set(f.path for f in http_error_handlers)

IF len(unique_files) > 2:
  violations.append({
    type: "duplication",
    severity: "MEDIUM",
    pattern: "HTTP Error Handling",
    files: list(unique_files),
    suggestion: "Centralize in infrastructure layer"
  })
```

### Phase 3.5: Calculate Score

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

### Phase 4: Return Result

```json
{
  "category": "Layer Boundary",
  "score": 4.5,
  "domain": "users",
  "scan_path": "src/users/",
  "total_issues": 8,
  "critical": 1,
  "high": 3,
  "medium": 4,
  "low": 0,
  "architecture": {
    "type": "Layered",
    "layers": ["api", "services", "domain", "infrastructure"]
  },
  "checks": [
    {"id": "io_isolation", "name": "I/O Isolation", "status": "failed", "details": "HTTP client found in domain layer"},
    {"id": "http_abstraction", "name": "HTTP Abstraction", "status": "warning", "details": "75% coverage, 3 direct calls outside infrastructure"},
    {"id": "error_centralization", "name": "Error Centralization", "status": "failed", "details": "HTTP error handlers in 4 files, should be centralized"},
    {"id": "transaction_boundary", "name": "Transaction Boundary", "status": "failed", "details": "commit() in repos (3), services (2), api (4) - mixed UoW ownership"},
    {"id": "session_ownership", "name": "Session Ownership", "status": "passed", "details": "DI-based sessions used consistently"}
  ],
  "findings": [
    {
      "severity": "CRITICAL",
      "location": "app/",
      "issue": "Mixed UoW ownership: commit() found in repositories (3), services (2), api (4)",
      "principle": "Layer Boundary / Transaction Control",
      "recommendation": "Choose single UoW owner (service layer recommended), remove commit() from other layers",
      "effort": "L",
      "domain": "users"
    },
    {
      "severity": "HIGH",
      "location": "app/domain/pdf/parser.py:45",
      "issue": "Layer violation: HTTP client used in domain layer",
      "principle": "Layer Boundary / I/O Isolation",
      "recommendation": "Move httpx.AsyncClient to infrastructure/http/clients/",
      "effort": "M"
    },
  ],
  "coverage": {
    "http_abstraction": 75,
    "error_centralization": false,
    "transaction_boundary_consistent": false,
    "session_ownership_consistent": true
  }
}
```

## Critical Rules

- **Read architecture.md first** - never assume architecture type
- **Skip violations list** - respect legacy files marked for gradual fix
- **File + line + code** - always provide exact location with context
- **Actionable suggestions** - always tell WHERE to move the code
- **No false positives** - verify path contains forbidden dir, not just substring

## Definition of Done

- Architecture discovered from docs/architecture.md (or fallback used)
- All violation types from layer_rules.md checked
- **Cross-layer consistency checked:**
  - Transaction boundaries analyzed (commit/rollback distribution)
  - Session ownership analyzed (DI vs local)
- Coverage calculated for HTTP abstraction + 2 consistency metrics
- Violations list with severity, location, suggestion
- If domain-aware: all Grep scoped to scan_path, findings tagged with domain
- Summary counts returned to coordinator

## Reference Files

- Layer rules: `../ln-640-pattern-evolution-auditor/references/layer_rules.md`
- Scoring impact: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`

---

**Version:** 2.1.0
**Last Updated:** 2026-02-08
