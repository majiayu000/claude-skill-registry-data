---
name: ln-642-layer-boundary-auditor
description: L3 Worker. Audits architectural layer boundaries, detects violations (code in wrong layers), checks pattern coverage. Invoked by ln-640 once per audit.
---

# Layer Boundary Auditor

L3 Worker that audits architectural layer boundaries and detects violations.

## Purpose & Scope

- Read architecture.md to discover project's layer structure
- Detect layer violations (I/O code outside infrastructure layer)
- Check pattern coverage (all HTTP calls use client abstraction)
- Detect error handling duplication
- Return violations list to coordinator

## Input (from ln-640)

```
- architecture_path: string    # Path to docs/architecture.md
- codebase_root: string        # Root directory to scan
- skip_violations: string[]    # Files to skip (legacy)
```

## Workflow

### Phase 1: Discover Architecture

```
Read docs/architecture.md

Extract from Section 4.2 (Top-Level Decomposition):
  - architecture_type: "Layered" | "Hexagonal" | "Clean" | "MVC" | etc.
  - layers: [{name, directories[], purpose}]

Extract from Section 5.3 (Infrastructure Layer Components):
  - infrastructure_components: [{name, responsibility}]

IF architecture.md not found:
  Use fallback presets from common_patterns.md

Build ruleset:
  FOR EACH layer:
    allowed_deps = layers that can be imported
    forbidden_deps = layers that cannot be imported
```

### Phase 2: Detect Layer Violations

```
FOR EACH violation_type IN common_patterns.md I/O Pattern Boundary Rules:
  grep_pattern = violation_type.detection_grep
  forbidden_dirs = violation_type.forbidden_in

  matches = Grep(grep_pattern, codebase_root, include="*.py,*.ts,*.js")

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

### Phase 4: Return Result

```json
{
  "architecture": {
    "type": "Layered",
    "layers": ["api", "services", "domain", "infrastructure"]
  },
  "violations": [
    {
      "type": "layer_violation",
      "severity": "HIGH",
      "pattern": "HTTP Client",
      "file": "app/domain/pdf/parser.py",
      "line": 45,
      "code": "async with httpx.AsyncClient() as client:",
      "allowed_in": "infrastructure/http/",
      "suggestion": "Move to infrastructure/http/clients/"
    }
  ],
  "coverage": {
    "http_abstraction": 75,
    "resilience_wrapper": 60
  },
  "summary": {
    "total_violations": 5,
    "high": 2,
    "medium": 3,
    "low": 0
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
- All violation types from common_patterns.md checked
- Coverage calculated for HTTP abstraction
- Violations list with severity, location, suggestion
- Summary counts returned to coordinator

## Reference Files

- Layer rules: `../ln-640-pattern-evolution-auditor/references/common_patterns.md`
- Scoring impact: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`

---

**Version:** 1.0.0
**Last Updated:** 2026-01-29
