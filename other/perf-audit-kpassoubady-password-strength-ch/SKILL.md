---
name: perf-audit
description: Full-repo performance audit — discovers all performance-sensitive files (JS, Java, Ruby, Go), analyzes them in parallel batches, and produces a prioritized hotspot report.
agent: perf-audit
argument-hint: "[target-directory] [all|js-only|java-only|ruby-only|go-only]"
pass-full-context: true
pass-conversation-history: true
---

# /perf-audit

Full-repo performance audit across all JS, Java, Ruby, and Go files.

Audit scope: $ARGUMENTS

## Usage

- `/perf-audit` — audit all performance-sensitive files in the current repository
- `/perf-audit src/` — audit a specific subdirectory only
- `/perf-audit java-only` — audit only Java files
- `/perf-audit src/ ruby-only` — audit Ruby files under `src/`
- `/perf-audit go-only` — audit only Go files

Reads **entire files** (not just diffs) — use this for a codebase-wide health check, not for reviewing changes. For diff-based review, use `/code-reviewer` or `/review-pr` instead.

Produces a prioritized report with:
- Hotspot map (files and directories ranked by issue density)
- Systemic pattern detection (same anti-pattern in 3+ files → team-level fix recommendation)
- All findings ranked by severity (Critical / Major / Minor)

Ruby and Go files are analyzed with endpoint-scale context — per-request anti-patterns (N+1, goroutine leaks, missing timeouts) are escalated accordingly.

Output is written to `claude-agents-output/perf-audit-<date>/perf-audit-report.md`.
