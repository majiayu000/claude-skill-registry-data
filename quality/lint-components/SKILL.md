---
name: lint-components
description: Validates Garura components (plays, agents, skills) against structural, semantic, and cross-reference rules. Reads quality profile to classify violation severities.
user-invocable: false
model: sonnet
allowed-tools: Bash, Read
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

## Purpose

Run the deterministic Node.js component linter against `core/components/` and produce a structured lint report artifact. Reads the project quality profile to classify ERROR violations as blockers and WARNING violations as informational per the profile's maintainability and security targets.

## Input

STM input contract:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project_root` | string | Yes | Absolute path to the repository root |
| `output_path` | string | Yes | STM path where the lint report artifact will be written |

Example:
```yaml
stm:
  input:
    project_root: /path/to/repo
  output:
    lint_report: .garura/project/issues/{issue}/evidence/{play}/lint-report.yaml
```

## Process

1. **Check node_modules.** From `{project_root}`, check whether `core/tools/lint-components/node_modules/` exists. If not, run:
   ```bash
   npm install --silent
   ```
   in `core/tools/lint-components/`. This installs the `js-yaml` dependency required by the linter.

2. **Run the linter.** Execute:
   ```bash
   node core/tools/lint-components/index.js --target core/components --output json
   ```
   Capture stdout as the raw JSON output. The tool exits 0 if no errors; exits 1 if any errors are found (errors > 0). Both exit codes are expected — do NOT treat exit code 1 as a fatal failure.

3. **Parse JSON output.** Parse the captured stdout as JSON. Shape:
   ```json
   {
     "violations": [
       { "file": "...", "rule": "...", "severity": "error|warning|info", "message": "...", "line": 0 }
     ],
     "summary": { "errors": 0, "warnings": 0, "infos": 0 }
   }
   ```

4. **Read quality profile.** Read `.garura/product/specification/quality-profile.yaml`. Extract the `status` field and the maintainability and security target levels. If the file does not exist, log `quality_profile_status: not_found` in the output artifact and proceed with default classification: ERROR → blocker, WARNING → informational.

5. **Classify violations by severity.** Apply quality-profile-derived policy:
   - Violations with `severity: error` → classified as `blocker` (blocking issues that prevent merge/ship)
   - Violations with `severity: warning` → classified as `informational` (tracked but non-blocking)
   - Violations with `severity: info` → classified as `informational`

6. **Log quality profile status.** Record the `status` field from the quality profile (e.g., `DRAFT`, `APPROVED`) in the output artifact as `quality_profile_status`.

7. **Write lint report to STM output path.** Write a structured YAML artifact:
   ```yaml
   generated_at: <ISO timestamp>
   quality_profile_status: <status from profile, or "not_found">
   summary:
     errors: <count>
     warnings: <count>
     infos: <count>
     blockers: <count of error violations>
     informational: <count of warning + info violations>
   pass: <true if errors == 0, false otherwise>
   violations:
     - file: <path>
       rule: <rule id>
       severity: <error|warning|info>
       classification: <blocker|informational>
       message: <message>
       line: <line number>
   ```

## Output

**Lint report artifact** written to `{output_path}`:

| Field | Description |
|-------|-------------|
| `generated_at` | ISO timestamp of when the lint was run |
| `quality_profile_status` | Status field from quality profile, or `not_found` |
| `summary.errors` | Count of error-severity violations |
| `summary.warnings` | Count of warning-severity violations |
| `summary.infos` | Count of info-severity violations |
| `summary.blockers` | Count of blocker-classified violations (= errors) |
| `summary.informational` | Count of informational violations (= warnings + infos) |
| `pass` | `true` if no errors found; `false` otherwise |
| `violations` | Array of all violations with classification |

**Return value:** The output artifact path.

## Constraints

- Must not modify any components under `core/components/` — read-only analysis only.
- Template validation (`--validate-templates`) is off by default. Do not pass this flag unless explicitly instructed.
- Quality profile path must be resolvable: `.garura/product/specification/quality-profile.yaml`. If absent, fall back to default classification and log `quality_profile_status: not_found`.
- Do not fail the skill if the linter exits with code 1 — that is the expected exit code when violations are found. Only fail on exit code 2 (fatal/unexpected error).
- Run from `{project_root}` so relative paths in the linter resolve correctly.
