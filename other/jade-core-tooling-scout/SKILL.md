---
name: jade-core-tooling-scout
description: >-
  Detects what can be auto-assisted by OpenRewrite, PMD, and Checkstyle before
  manual scanner work. Probes tool availability, runs each tool against the
  legacy workspace using a modern JDK, collects findings, and merges results
  into the breaking-changes manifest with provenance. Never rewrites code —
  discovery and reporting only.
when_to_use: >-
  Use when the user says "tooling scout", "what can be automated", "run tooling
  analysis", "check OpenRewrite recipes", "lint before migration", "auto-fix
  discovery", or the orchestrator reaches TOOLING_SCOUT_READY phase.
arguments: [modern_jdk_path]
argument-hint: "[path-to-modern-jdk-11-or-17]"
context: fork
allowed-tools: Bash(python *) Bash(java *) Bash(mvn *) Bash(gradle *) Bash(which *) Read Write
paths: "artifacts/*.json"
env: MODERN_JAVA_HOME=$modern_jdk_path
---

# JADE Tooling Scout

## Objective

Discover what migration work can be auto-assisted by static analysis tooling
(OpenRewrite, PMD, Checkstyle) **before** any manual scanner or code edits
execute.  Never rewrite code — only probe, run, and report.

## Runtime decoupling

The tooling engine runs on a **modern JDK** (`MODERN_JAVA_HOME`, Java 11/17+)
while the **analysis target** is the legacy JADE workspace (Java 1.5/1.6
source level).  This decoupling means:

| Layer | JDK |
|---|---|
| Engine (OpenRewrite, PMD, Checkstyle) | `MODERN_JAVA_HOME` (Java 11/17+) |
| Analysis target (source code) | Legacy workspace (Java 1.5/1.6) |

The modern JDK is **only** used to execute the tooling binaries; the tools
themselves are configured to analyze Java 1.5/1.6 source level code.
The legacy workspace is never compiled with the modern JDK — tools that
require compilation must use the workspace's own JDK.

## Required inputs

| Artifact | Source |
|---|---|
| `artifacts/00-run-config.json` | Created by orchestrator in INIT phase |
| `artifacts/01-breaking-changes-manifest.json` | Created during MANIFEST_READY phase |

The run-config provides `workspace_path` and `artifacts_path`.
The manifest provides the initial rule set that findings will be merged into.

## Outputs

| Artifact | Description |
|---|---|
| `artifacts/02-tooling-scout-report.json` | Summary of tools probed, available, and findings |
| `artifacts/02-linter-findings.json` | Raw violations from each tool |
| `artifacts/01-breaking-changes-manifest.json` | **Updated in-place** — new rules merged with provenance |

## Step-by-step

### Step 1: Validate inputs

Run the bundled script with `--validate` to check that all inputs exist and the
modern JDK is a valid Java 11+ installation:

```bash
python .claude/skills/jade-tooling-scout/scripts/tooling_scout.py --validate \
  --modern-jdk $MODERN_JAVA_HOME
```

Exit codes:
- `0` — all inputs valid, tools ready for probing
- `2` — missing or invalid input (configuration error)
- `3` — modern JDK unusable (wrong version, missing javac)

### Step 2: Probe tool availability

```bash
python .claude/skills/jade-tooling-scout/scripts/tooling_scout.py --probe \
  --modern-jdk $MODERN_JAVA_HOME
```

This checks for:
- **OpenRewrite** — Maven plugin or Gradle plugin presence in workspace, or
  `mvn`/`gradle` wrapper availability.  Also checks for existing rewrite
  configuration files (`rewrite.yml`, `rewrite.yaml`).
- **PMD** — `pmd` binary on PATH, or bundled PMD zip, or Maven plugin.
- **Checkstyle** — `checkstyle` jar or Maven/Gradle plugin configuration.

Unavailable tools are logged and skipped — the scout never fails because a
tool is missing.

### Step 3: Run tools and collect findings

```bash
python .claude/skills/jade-tooling-scout/scripts/tooling_scout.py --run \
  --modern-jdk $MODERN_JAVA_HOME
```

For each available tool:

**OpenRewrite**: Run `--dry-run` against the workspace to list applicable
recipes. Do NOT apply any recipe. Capture the recipe list and categorize as:
- `applicable` — recipe matches at least one source file
- `not_applicable` — recipe registered but no matches found

**PMD**: Scan `**/*.java` with rulesets relevant to the migration jump
(source_version → target_version).  Capture violation: file, line, rule,
priority.

**Checkstyle**: Scan with a minimal checkset targeting migration-relevant
patterns (unused imports, deprecation markers, raw types, etc.).
Capture violation: file, line, check, severity.

### Step 4: Generate reports

The `--run` step produces:
- `artifacts/02-tooling-scout-report.json` — structured summary
- `artifacts/02-linter-findings.json` — raw, machine-readable findings

Schema for `02-tooling-scout-report.json`:

```json
{
  "run_id": "string",
  "modern_jdk": "string",
  "available_tools": ["openrewrite", "pmd", "checkstyle"],
  "unavailable_tools": ["..."],
  "findings_summary": {
    "openrewrite": {
      "recipes_total": 0,
      "recipes_applicable": 0,
      "recipes_not_applicable": 0
    },
    "pmd": {
      "violations_total": 0,
      "rulesets_used": ["category/java/bestpractices.xml"]
    },
    "checkstyle": {
      "violations_total": 0,
      "checks_triggered": ["UnusedImports"]
    }
  },
  "manifest_merge_count": 0,
  "updated_at": "ISO-8601"
}
```

Schema for `02-linter-findings.json`:

```json
{
  "run_id": "string",
  "source_version": "string",
  "target_version": "string",
  "workspace_path": "string",
  "openrewrite": {
    "available": true,
    "version": "string|null",
    "recipes": [
      {
        "name": "org.openrewrite.java.UpgradeToJava6",
        "status": "applicable|not_applicable",
        "description": "string"
      }
    ]
  },
  "pmd": {
    "available": true,
    "version": "string|null",
    "violations": [
      {
        "file": "path/relative/to/workspace",
        "line": 0,
        "rule": "string",
        "ruleset": "string",
        "priority": 0,
        "description": "string"
      }
    ]
  },
  "checkstyle": {
    "available": true,
    "version": "string|null",
    "violations": [
      {
        "file": "path/relative/to/workspace",
        "line": 0,
        "check": "string",
        "severity": "error|warning|info",
        "message": "string"
      }
    ]
  }
}
```

### Step 5: Merge into manifest

```bash
python .claude/skills/jade-tooling-scout/scripts/tooling_scout.py --merge \
  --modern-jdk $MODERN_JAVA_HOME
```

Reads `01-breaking-changes-manifest.json`, appends new rule entries derived
from tool findings.  Each new entry includes:

```json
{
  "rule_id": "tooling:openrewrite:UpgradeToJava6",
  "source": "tooling-scout",
  "provenance": {
    "tool": "openrewrite",
    "tool_version": "x.y.z",
    "detected_at": "ISO-8601",
    "confidence": "high|medium|low"
  },
  "description": "Auto-detectable recipe: UpgradeToJava6 (1 match)",
  "auto_fixable": true
}
```

Merge rules:
- Never remove existing manifest entries.
- Entries with the same `rule_id` are deduplicated (last writer wins).
- `auto_fixable: true` means a tool can apply the fix automatically.
- `auto_fixable: false` means linter flagged it but no automatic rewrite exists.

### Step 6: Report to orchestrator

The `--all` flag runs the full pipeline (validate → probe → run → merge) and
returns the appropriate exit code:

```bash
python .claude/skills/jade-tooling-scout/scripts/tooling_scout.py --all \
  --modern-jdk $MODERN_JAVA_HOME
```

Exit code `0` means the orchestrator can transition to `TOOLING_SCOUT_READY`.

## Graceful handling of missing tools

| Situation | Behavior |
|---|---|
| OpenRewrite not installed | Skip, log reason, mark `available: false` |
| PMD binary not found | Skip, log reason, mark `available: false` |
| Checkstyle jar not found | Skip, log reason, mark `available: false` |
| Modern JDK not usable | Exit code 3, do not modify any artifacts |
| Config file missing | Exit code 2, print missing path |
| All tools unavailable | Still produce reports (empty findings), exit 0 |

The scout **never fails** because a tool is absent.  It fails only due to
configuration errors or an unusable modern JDK.

## Constraints

1. Never rewrite or modify source code.
2. Never compile the workspace with the modern JDK.
3. Run tools in read-only / dry-run mode only.
4. Append to manifest; never remove existing entries.
5. All outputs include UTC timestamps and run provenance.
6. Tool stdout/stderr is captured but not echoed (append to findings where
   useful).

## Exit criteria

- `artifacts/02-tooling-scout-report.json` exists and is valid JSON
- `artifacts/02-linter-findings.json` exists and is valid JSON
- `artifacts/01-breaking-changes-manifest.json` has new `tooling-scout` sourced
  entries (if tools found applicable results)
- Exit code is 0 (even if no tools were available)
