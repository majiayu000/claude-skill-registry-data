---
name: compatibility-audit
disable-model-invocation: true
description: 'Audits ycc compatibility for ycc maintainers only. Use when checking generated bundle drift, verifying install assumptions, or comparing target feature gaps.'
argument-hint: '[--target=claude|cursor|codex|opencode|omp|all] [--json] [--fail-fast] [--dry-run]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/compatibility-audit/scripts/audit-install-assumptions.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/compatibility-audit/scripts/audit-target-features.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/report-bundle-drift.sh:*)'
  - 'Bash(./scripts/validate.sh:*)'
---

# compatibility-audit

This skill audits the health of every generated compatibility target for the
`ycc` plugin — Claude, Cursor, Codex, opencode, and omp (oh-my-pi) — and produces a structured,
per-target triage report. It detects bundle drift between the `ycc/` source
tree and the generated bundles, validates install assumptions (path conventions,
shebang lines, executable bits), and surfaces feature-capability gaps using the
shared capability matrix. It never bumps versions, never commits, and never
modifies any file.

## When to use

- You want to know whether the Cursor or Codex bundles are in sync with the
  `ycc/` source tree.
- You are preparing a release and need a pre-flight compatibility snapshot
  before running `/ycc:bundle-release`.
- A CI job reported a bundle validation failure and you need a structured
  breakdown.
- You suspect a newly added skill or agent was not propagated to all targets.
- You want to confirm that install-path assumptions (e.g. the plugin-root
  variable references) are consistent across all generated artifacts.
- You want to identify which features are unavailable on a specific target due
  to platform capability limits.

## Arguments

Parse `$ARGUMENTS` for:

- **--target** (optional, default `all`) — restrict the audit to a single
  target. Accepted values: `claude`, `cursor`, `codex`, `opencode`, `omp`, `all`. When `all` is
  specified, phases 2–5 run once per target in the set `{claude, cursor, codex, opencode, omp}`.
  `omp` has no generated tree or generator yet: skip Phases 2 and 3 for it and
  report them as `not generated yet` rather than failures.
- **--json** (flag, default off) — emit the final triage report as a
  machine-readable JSON envelope instead of Markdown. Per-target sections are
  preserved inside the envelope as structured objects.
- **--fail-fast** (flag, default off) — stop after the first target that
  reports any error or drift. Do not proceed to remaining targets. Surface the
  failure immediately.
- **--dry-run** (flag, default off) — print the full audit plan (which scripts
  will be invoked, in what order, against which targets) and then STOP without
  running anything.

## Phases

### Phase 0: Load capability matrix

Read
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/target-capability-matrix.md`.

This document defines which features (skills, agents, slash commands, hooks)
are available on each target. Load it into context before any per-target work
begins. If the file is missing, surface a clear error and STOP — the matrix is
required for Phase 5.

### Phase 1: Parse arguments and resolve target set

Parse `$ARGUMENTS` as described above. Resolve `--target` to a concrete list:

- `all` → `[claude, cursor, codex, opencode, omp]`
- any single value → a one-element list

If `--dry-run` was passed, print the resolved target list, the scripts that
would be invoked for each target (Phases 2–5), and the output format
(`--json` or Markdown). Then STOP without invoking anything.

### Phase 2: Bundle drift detection (per target)

The reporter requires a source checkout containing `ycc/skills` and
`scripts/generate_*.py`, not an installed bundle. It discovers the checkout or
accepts `--repo-root=/path/to/checkout`.

For each target `<t>` in the resolved list, invoke:

```
${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/report-bundle-drift.sh --target=<t> --format=json
```

Capture the JSON output. A non-zero exit means drift was detected or the
script itself failed. On failure, surface the full stderr. If `--fail-fast` is
active, STOP after the first non-zero exit.

### Phase 3: Validate generated bundle (per target)

For each target `<t>`, invoke:

```
./scripts/validate.sh --only <t>
```

Capture stdout and stderr. A non-zero exit means validation failed for that
target. Surface the full output. If `--fail-fast` is active, STOP after the
first non-zero exit.

### Phase 4: Audit install assumptions (per target)

For each target `<t>`, invoke:

```
${CLAUDE_PLUGIN_ROOT}/skills/compatibility-audit/scripts/audit-install-assumptions.sh --target=<t> --format=json
```

This script checks path conventions, shebang lines, executable permissions, and
plugin-root variable reference consistency for all artifacts belonging to
`<t>`. Capture JSON output. On non-zero exit, surface stderr. If `--fail-fast`
is active, STOP after the first failure.

### Phase 5: Audit target feature gaps (global)

Run once, not per-target:

```
${CLAUDE_PLUGIN_ROOT}/skills/compatibility-audit/scripts/audit-target-features.sh --format=json
```

This script cross-references the capability matrix loaded in Phase 0 against
the actual contents of each generated bundle to identify features that exist in
the source tree but are absent or degraded on one or more targets. Capture JSON
output. On non-zero exit, surface stderr and continue to Phase 6 with partial
data — do not STOP, because feature-gap data is informational, not a hard
failure.

### Phase 6: Synthesize triage report

Combine the outputs from Phases 2–5 into a structured per-target report.

**Markdown output (default):**

Produce one section per target. Within each section, list drift findings,
validation results, install-assumption issues, and feature gaps as separate
subsections. Conclude with a per-target verdict: `PASS`, `WARN`, or `FAIL`.
Do not emit a single aggregate verdict — see the Anti-parity stance section.

**JSON output (`--json`):**

Wrap the per-target objects in a top-level envelope:

```json
{
  "schema": "compatibility-audit/v1",
  "targets": {
    "claude":  { "drift": {...}, "validation": {...}, "install": {...}, "features": {...}, "verdict": "PASS|WARN|FAIL" },
    "cursor":  { "drift": {...}, "validation": {...}, "install": {...}, "features": {...}, "verdict": "PASS|WARN|FAIL" },
    "codex":   { "drift": {...}, "validation": {...}, "install": {...}, "features": {...}, "verdict": "PASS|WARN|FAIL" },
    "opencode":{ "drift": {...}, "validation": {...}, "install": {...}, "features": {...}, "verdict": "PASS|WARN|FAIL" },
    "omp":     { "drift": {...}, "validation": {...}, "install": {...}, "features": {...}, "verdict": "PASS|WARN|FAIL" }
  },
  "audited_at": "<ISO-8601 timestamp>"
}
```

Omit targets that were excluded via `--target`.

## Output format

A typical Markdown report looks like this:

```
## compatibility-audit report

### claude

- Drift: none detected
- Validation: passed
- Install assumptions: all checks passed
- Feature gaps: none

Verdict: PASS

---

### cursor

- Drift: 2 skills missing from .cursor-plugin/ (bundle-author, compatibility-audit)
- Validation: FAILED — .cursor-plugin/rules/ycc.mdc missing section [skills]
- Install assumptions: 1 script missing executable bit (audit-install-assumptions.sh)
- Feature gaps: slash commands not supported on Cursor (expected, per capability matrix)

Verdict: FAIL

---

### codex

- Drift: none detected
- Validation: passed
- Install assumptions: all checks passed
- Feature gaps: hooks not supported on Codex (expected, per capability matrix)

Verdict: WARN
```

Note: `WARN` indicates expected capability gaps documented in the capability
matrix, not actionable failures. `FAIL` indicates drift, validation errors, or
install issues that must be resolved before release.

## Anti-parity stance

Each target operates under a different runtime contract. Cursor does not support
slash commands; Codex does not support hooks. These are expected, documented
gaps — not failures. This skill reports results in per-target sections and
assigns a per-target verdict. It does NOT produce a single aggregate pass/fail
across all targets, because collapsing cross-target results into one verdict
obscures which target needs attention and why.

For guidance on reading per-target verdicts and distinguishing expected gaps
from actionable failures, see
`${CLAUDE_PLUGIN_ROOT}/skills/compatibility-audit/references/reading-the-report.md`.

## Notes

- This skill does not bump versions, does not commit, and does not modify any
  file. It is a read-only diagnostic tool.
- To act on the findings — bump versions, regenerate bundles, tag a release —
  use `/ycc:bundle-release`.
- The capability matrix at
  `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/target-capability-matrix.md`
  is the authoritative source for what is and is not expected on each target.
  If a gap appears in the report but is documented in the matrix, it is a `WARN`
  not a `FAIL`.
