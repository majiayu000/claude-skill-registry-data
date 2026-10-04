---
name: jade-core-scanner
description: >-
  Production-grade scanner that reads a breaking-changes manifest, scans workspace
  sources against rule patterns using regex, injects deterministic inline
  // JADE-FLAG:<rule_id> markers into matched source lines, and writes flag index
  and scan summary artifacts. Fully idempotent — re-running never duplicates tags.
  Use after manifest is ready and before build gate verification.
when_to_use: >-
  Use when the user says "scan workspace", "tag sources", "run scanner", "inject
  flags", "jade-scanner", or after jade-core-orchestrator reaches SCAN_READY.
arguments: [workspace_path, artifacts_path]
argument-hint: "[workspace-dir] [artifacts-dir]"
allowed-tools: Bash(python3 *)
paths: "**/*.java"
---

# JADE Scanner — Deterministic Source Tagger

## Objective

Read the breaking-changes manifest, match every rule pattern against workspace source files
via regex, and inject inline `// JADE-FLAG:<rule_id> <reason> <confidence>` markers exactly
once per matched location. Write a flag index and a human-readable scan summary.

## Core constraints

- **Idempotent.** Re-running on already-tagged sources must not create duplicate flags.
- **No prompt payload handoff.** Scanner writes artifacts to disk; never dump source contents into context.
- **Atomic file writes.** Only touching files that contain a new match; using temp-file + rename.
- **Deterministic.** Same manifest + same workspace + same graph → byte-identical output every time (no volatile timestamps).

## Required inputs

- `{artifacts}/01-breaking-changes-manifest.json`
- `{artifacts}/02-linter-findings.json` (optional — merged with manifest rules if present)
- `{artifacts}/03.5-knowledge-graph.json` (optional — enriches each flag with advisory graph impact metadata when present and valid)
- `{workspace}` — directory tree of source files to scan (e.g., `migration-runs/sample/workspace`)

## Produced outputs

- `{artifacts}/04-flag-index.json` — every injected flag with file/line/rule/confidence, plus additive `graph` impact metadata when a valid graph is available
- `{artifacts}/04-scan-summary.json` — per-rule and per-confidence counts, total files touched
- Tagged source files under `{workspace}` (modified in-place; only files with new matches)

---

## Inline marker format

```
// JADE-FLAG:<rule_id> <reason> <confidence>
```

The scanner inserts this comment on the line **after** the matched line. If the matched
line already ends with a comment the exact rule_id was already injected on, the scanner
skips that location.

**Example — before scan:**

```java
Vector agents = new Vector();
```

**Example — after scan:**

```java
Vector agents = new Vector();
// JADE-FLAG:RAW_TYPES Raw collection instantiation (Vector) HIGH
```

---

## Phase 0: Validate inputs

```bash
python3 .claude/skills/jade-scanner/scripts/scan_and_tag.py \
  --workspace "{workspace}" \
  --artifacts "{artifacts}" \
  --dry-run
```

A dry-run exits 0 when the manifest is valid and the workspace is readable. It writes
nothing. If it fails, fix the manifest or workspace path before proceeding.

---

## Phase 1: Full scan

```bash
python3 .claude/skills/jade-scanner/scripts/scan_and_tag.py \
  --workspace "{workspace}" \
  --artifacts "{artifacts}"
```

The scanner:

1. Loads `01-breaking-changes-manifest.json` and validates every rule and pattern.
2. Loads `02-linter-findings.json` (if present) and merges its entries as additional
   rules with rule_id prefixed `LINT:`.
3. Walks the workspace, collecting only files whose extensions match at least one
   pattern's `target_extensions` list.
4. For each candidate file, loads its contents into memory and tests every pattern
   line-by-line.
5. When a pattern matches, checks whether a `JADE-FLAG:<rule_id>` comment already
   exists on the matched line or the line immediately after. If yes → skip (idempotent).
   If no → insert the flag comment on the next line and record the flag.
6. Writes modified files back via temp-file + atomic rename.
7. Writes `04-flag-index.json` (every flag) and `04-scan-summary.json` (aggregate stats).

---

## Phase 2: Verify

After the scan completes, check the exit code and confirm outputs exist:

```bash
test -f {artifacts}/04-flag-index.json && echo "PASS" || echo "FAIL"
test -f {artifacts}/04-scan-summary.json && echo "PASS" || echo "FAIL"
python3 -c "import json; d=json.load(open('{artifacts}/04-flag-index.json')); print(f'Flags: {len(d[\"flags\"])}')"
```

A second run must produce the exact same flag count (zero new injections):

```bash
python3 .claude/skills/jade-scanner/scripts/scan_and_tag.py \
  --workspace "{workspace}" \
  --artifacts "{artifacts}"
# Exit code 0, summary.total_new_flags == 0, summary.idempotent_skips == previous total
```

---

## Manifest schema (01-breaking-changes-manifest.json)

```json
{
  "rules": [
    {
      "id": "RAW_TYPES",
      "name": "Raw Types to Generics",
      "severity": "HIGH",
      "patterns": [
        {
          "type": "regex",
          "pattern": "new\\s+(Vector|Hashtable|ArrayList|HashMap|LinkedList|HashSet)\\s*\\(\\)",
          "target_extensions": [".java"],
          "reason": "Raw collection instantiation",
          "confidence": "HIGH"
        }
      ]
    }
  ]
}
```

Pattern types supported: `regex`. Each `target_extensions` entry must include the leading dot.

---

## Flag index schema (04-flag-index.json)

```json
{
  "run_id": "sample-run",
  "workspace": "migration-runs/sample/workspace",
  "total_flags": 42,
  "total_files_scanned": 847,
  "flags": [
    {
      "rule_id": "RAW_TYPES",
      "file": "workspace/jade/core/Agent.java",
      "line": 142,
      "confidence": "HIGH",
      "reason": "Raw collection instantiation (HashMap)",
      "graph": {
        "source_artifact": "03.5-knowledge-graph.json",
        "node_exists": true,
        "declaration": "jade.core.Agent",
        "impact_files": ["jade/core/Container.java"],
        "artifact_diagnostics": {"parse_failures": 0, "unresolved_types": 0, "ambiguous_symbols": 0}
      }
    }
  ]
}
```

---

## Scan summary schema (04-scan-summary.json)

```json
{
  "run_id": "sample-run",
  "workspace": "migration-runs/sample/workspace",
  "total_files_scanned": 847,
  "total_new_flags": 42,
  "idempotent_skips": 0,
  "by_rule": {
    "RAW_TYPES": {
      "name": "Raw Types to Generics",
      "severity": "HIGH",
      "count": 30
    },
    "ENHANCED_FOR": {
      "name": "Enhanced For Loops",
      "severity": "MEDIUM",
      "count": 12
    }
  },
  "by_confidence": {
    "HIGH": 30,
    "MEDIUM": 12,
    "LOW": 0
  }
}
```

---

## Constraints

1. Never modify files outside `{workspace}`.
2. Never inject a flag comment that already exists on the matched line or adjacent line.
3. Never insert a flag into a comment block or Javadoc — only match within active code.
4. Respect `.gitignore` exclusions when present under `{workspace}`.
5. Exit non-zero on manifest parse errors or unreadable workspace.
6. Always write artifacts via temp-file + atomic rename.

## Exit criteria

- `scan_and_tag.py` exits 0.
- `04-flag-index.json` and `04-scan-summary.json` are valid JSON.
- A second identical run produces zero new flags and equal `idempotent_skips`.
