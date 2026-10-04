---
name: go-nolint-audit
description: >
  Audit Go nolint directives for staleness and lazy justifications.
  Mechanically verifies each suppression with golangci-lint, then runs
  adversarial Red/Blue/White debates on the top candidates for removal.
  Use when inheriting a Go codebase, during periodic cleanup, or when
  nolint count is growing unchecked.
compatibility: >
  Requires Go and golangci-lint. Only applicable to Go projects with
  //nolint directives.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Go Nolint Audit

Audit `//nolint:` directives in Go codebases. Finds suppressions that
are stale (code changed, lint rule no longer triggers) or lazily
justified (the underlying code could be fixed instead of suppressed).
Challenges each justification through adversarial debate rather than
accepting comments at face value.

## Prerequisite check

```bash
go version 2>/dev/null && golangci-lint --version 2>/dev/null
```

If `go` is not installed, stop and report. If `golangci-lint` is
missing:

- Install from <https://golangci-lint.run/welcome/install/>

Do **not** proceed without both tools available.

## Discover nolint directives

```bash
grep -rn '//nolint' --include='*.go' . | grep -v vendor/
```

Match all variants: `//nolint` (bare), `//nolint:rule`,
`//nolint:rule1,rule2`. For each directive, capture:

- File and line number
- Suppressed rule(s), or "bare" if no rule specified
- Justification comment (text after `//nolint:rule //` if present)
- Surrounding code context (~5 lines)

Bare `//nolint` (no rule) suppresses everything — flag for Phase 2
automatically. If zero directives found, report a clean codebase
and stop.

## Phase 1: Mechanical verification

For each directive with a named rule, test whether the suppression
is still needed. Co-enable `nolintlint` alongside the target rule:

```bash
# v2 syntax (preferred):
golangci-lint run --enable-only=<rule>,nolintlint \
  --allow-parallel-runners <file>

# v1 syntax (if v2 unavailable):
golangci-lint run --disable-all --enable=<rule>,nolintlint \
  --allow-parallel-runners <file>
```

If `nolintlint` reports the directive as unused, it is stale. This
avoids modifying source files. For multi-rule directives
(`//nolint:rule1,rule2`), test each rule separately. Run up to 3
parallel shell commands. Always use `--allow-parallel-runners`.

If golangci-lint fails for reasons other than the target rule (build
errors, missing deps), skip the directive and report as "unable to
verify."

Categorize each directive:

- **Stale** — rule no longer triggers. Safe to remove.
- **Active** — rule still triggers. Moves to Phase 2.

Report stale directives immediately. If all are stale, skip Phase 2.
Bare `//nolint` directives skip Phase 1 — they cannot be verified
against a specific rule.

## Phase 2: Adversarial debate

Score **all** discovered directives (not just the Phase 1 sample) on
two dimensions (1-5). For large codebases (50+ directives), sample
5-10 across different rules for Phase 1, but score the full list
here to find the worst offenders:

- **Fixability** — how easy to fix the code instead of suppressing?
  - 5 = trivial (extract function, rename, add constant)
  - 3 = moderate (restructure logic, split function)
  - 1 = architectural change required
- **Justification quality** — how convincing is the comment?
  - 5 = no comment, or vague ("complexity is inherent", "needed")
  - 3 = explains situation but not why fixing is worse
  - 1 = specific, compelling reason

**Score** = Fixability x Justification quality. Consult
`references/go-nolint-patterns.md` for scoring guidance.

Debate the **top 3** by score:

- **Red (remove)**: argues the nolint should be removed and the code
  fixed. Must propose a concrete diff. Challenges the justification.
- **Blue (keep)**: argues the nolint is correct. Must add reasoning
  beyond the existing comment. Points out risks of the proposed fix.
- **White (judge)**: evaluates on evidence. Decides: **remove**,
  **keep**, or **rewrite justification**.

### Debate rules

- Red and Blue must cite specific code, not generalities
- Red must provide a concrete diff, not just "this could be simpler"
- Blue cannot simply repeat the existing justification
- White's decision is final

## Output format

### Phase 1

```text
Stale (safe to remove):
  file.go:42  //nolint:errcheck — rule no longer triggers
  file.go:87  //nolint:mnd — rule no longer triggers

Unable to verify:
  file.go:99  //nolint:gosec — golangci-lint build error
```

### Phase 2

For each debated directive:

**#N: file.go:line — //nolint:rule**

**Current code** (with nolint):
[5-10 lines of surrounding code]

**Justification**: "original comment"
**Lint warning when removed**: [exact golangci-lint output]

**Red (remove)**: [argument + concrete diff]
**Blue (keep)**: [argument with specific reasoning]
**White (verdict)**: REMOVE | KEEP | REWRITE JUSTIFICATION
[reasoning]

[If REMOVE: repeat diff for easy application]
[If REWRITE: full replacement line with improved justification]

### Summary

| # | File:Line | Rule | Verdict | Effort |
| - | --------- | ---- | ------- | ------ |
| 1 | location | rule | verdict | effort |
| 2 | location | rule | verdict | effort |
| 3 | location | rule | verdict | effort |

Stale: N (remove immediately)  |  Unable to verify: N
