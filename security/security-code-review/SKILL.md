---
name: "security-code-review"
description: "Run a repeatable static code review for concrete bugs, vulnerabilities, and likely-issue patterns, against the full codebase or a specific change set (PR/branch/commit range). Trigger phrases: security code review, review code for vulnerabilities, scan for bugs, code security scan, review-security."
argument-hint: "[scope: PR number, branch name, or commit range — omit for full codebase]"
user-invocable: true
aliases: ["review-security"]
---

> **Copilot note**: The Copilot specialist subagent for this capability lives at `.github/agents/review-security.agent.md` (`name: "security-reviewer"`). It is invoked by the `code-review` orchestrator and runs the OWASP checklist inline. For standalone use from Copilot, use `/security-code-review` which delegates to this skill.


## Instructions

Contract: `specs/008-adversarial-security-review/contracts/skill-commands.md` (`/security-code-review`).
Requirements satisfied: FR-001, FR-002, FR-007, FR-010, FR-011.

### 1. Read trigger-mode config (FR-011)

Read `specs/008-adversarial-security-review/review-config.json` and check the `codeReview.trigger` value. Today the only valid value is `"on-demand"`, which this manual invocation satisfies — proceed. If a future value other than `"on-demand"` appears and this invocation is not a manual maintainer request, stop and tell the user the configured trigger mode doesn't match this invocation.

### 2. Resolve scope (FR-002)

Parse `$ARGUMENTS`:
- **Empty** → scope is the full codebase. `scope_label = "full"`, `is_full = true`.
- **A PR number** (e.g. `42`) → run `gh pr diff <number> --name-only` to get the changed file list. `scope_label = "pr-<number>"`, `is_full = false`.
- **A branch name or commit range** (e.g. `main..HEAD`, `feature/xyz`) → run `git diff --name-only <range or base>...HEAD` (or against `main` if a single branch name was given) to get the changed file list. `scope_label = "<the given ref>"`, `is_full = false`.

If scope resolution yields zero changed files, tell the user and stop — do not silently review the full codebase when a scope was explicitly requested.

### 3. Start a run

```bash
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  start-run --capabilities code --scope "<scope_label>" --trigger manual
```

Capture the returned `id` as `RUN_ID`.

### 4. Perform the review (judgment call — this is the Agent-invocation step)

Use the `Agent` tool (a general-purpose or code-review-oriented subagent) to review the resolved file set — either the entire repository under `src/` and `tests/` (full scope) or exactly the changed files from step 2 (scoped) — for:
- Concrete bugs (logic errors, null/resource-handling mistakes, race conditions).
- Security vulnerabilities (injection, unsafe deserialization, missing authZ/authN checks, secrets in code, insecure defaults).
- Likely-issue patterns even without a published CVE (per spec.md Assumptions: "known or likely issues" includes pattern-based risk flags, e.g. missing input validation).

Ask the subagent to return a structured list, one entry per finding, each with: exact file path + line number, a one-line title, a fuller description, and a severity (`critical`/`high`/`medium`/`low`).

**Do not skip this step and do not fabricate findings** — if the subagent finds nothing, that is a valid (and expected) outcome, not a failure.

### 5. Persist findings

For each finding returned in step 4:

```bash
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  upsert-finding --run-id "$RUN_ID" --source code \
  --title "<title>" --description "<description>" --severity "<severity>" \
  --evidence "<file path>:<line>"
```

### 6. Finalize the run

```bash
.specify/scripts/bash/security-findings-store.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  finalize-run --run-id "$RUN_ID" --full <true if is_full else false>
```

Only pass `--full true` for a full-codebase run — a PR-scoped run must never auto-resolve findings outside the files it looked at (it has no basis to claim those are fixed).

### 7. Regenerate the report and drop a dated snapshot into the repo

```bash
.specify/scripts/bash/security-report-render.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  --out specs/008-adversarial-security-review/findings/report.md

.specify/scripts/bash/security-report-render.sh \
  --findings-dir specs/008-adversarial-security-review/findings \
  --capability code --snapshot-date "$(date -u +%Y%m%d)" \
  --out "specs/008-adversarial-security-review/findings/$(date -u +%Y%m%d)-code-review.md"
```

The dated file is a git-tracked, point-in-time snapshot of just this capability's findings for today — running this capability again later the same day overwrites today's dated file (date granularity, not per-run); a different day gets a new file. `report.md` remains the always-current cross-capability view and is unaffected by this.

Show the user the `## Code Review` section of the resulting report. If it says "No findings from this capability have been recorded yet," state that explicitly as a zero-findings result (Acceptance Scenario 3) — never present empty/ambiguous output.

### 8. Independence check (FR-010)

If asked to demonstrate FR-010 (e.g. during validation), confirm `specs/008-adversarial-security-review/findings/findings.json` and `runs.json` contain no `dependency`- or `adversarial`-sourced entries when this is the only capability that has ever been run — this capability must work correctly with zero dependency on the other two ever having run.

## User Input

```text
$ARGUMENTS
```
