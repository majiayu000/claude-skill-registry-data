---
name: harness-review
description: "Multi-angle code and plan review with security, scope, and UI profiles. Use when reviewing code, plans, PRs, or running pre-merge quality gates."
when_to_use: "review code, review plan, review PR, security audit, pre-merge check, scope analysis, quality gate"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task", "AskUserQuestion"]
argument-hint: "[code|plan|scope|--quick|--codex-closeout|--dual|--team-debate|--security|--ui-rubric]"
context: fork
effort: xhigh
model: opus
agent: reviewer
---

# Harness Review

## Quick Reference

| User Input | Subcommand | Behavior |
|------------|------------|----------|
| "Review this" / "review" | `code` (auto) | Code review (recent changes) |
| "After `harness-plan`" | `plan` (auto) | Plan review |
| "Check scope" | `scope` (auto) | Scope analysis |
| `harness-review code` | `code` | Force code review |
| `harness-review plan` | `plan` | Force plan review |
| `harness-review scope` | `scope` | Force scope analysis |
| `harness-review --dual` | `code` (auto) + Codex parallel | Claude + Codex dual review |
| `harness-review --security` | Security Review | OWASP Top 10 dedicated security review (read-only) |
| `harness-review --ui-rubric` | UI Rubric Review | 4-axis design quality scoring |

## Operating Modes

Maps flags to their reference files. Quick Reference above covers trigger → subcommand routing; this table covers flag → reference dispatch.

| Flag | Reference | Purpose |
|------|-----------|---------|
| `--quick` | [`${CLAUDE_SKILL_DIR}/references/codex-closeout.md`](${CLAUDE_SKILL_DIR}/references/codex-closeout.md) | Lightweight Codex-assisted closeout; stops on clean result |
| `--codex-closeout` | [`${CLAUDE_SKILL_DIR}/references/codex-closeout.md`](${CLAUDE_SKILL_DIR}/references/codex-closeout.md) | Full closeout with final JSON report |
| `--team-debate` | [`${CLAUDE_SKILL_DIR}/references/team-debate.md`](${CLAUDE_SKILL_DIR}/references/team-debate.md) | Multi-agent read-only debate (Spec / Plans / Regression / Skeptic agents) |
| `--opencode` | [`${CLAUDE_SKILL_DIR}/references/opencode-review.md`](${CLAUDE_SKILL_DIR}/references/opencode-review.md) | OpenCode-assisted review via opencode-plugin-cc |
| _(any mode)_ | [`${CLAUDE_SKILL_DIR}/references/governance.md`](${CLAUDE_SKILL_DIR}/references/governance.md) | APPROVE pass criteria, severity table, AskUserQuestion contract |
| _(any mode)_ | [`${CLAUDE_SKILL_DIR}/references/code-review.md`](${CLAUDE_SKILL_DIR}/references/code-review.md) | Eight-lens review flow and verdict rules |

`--team-debate` is required when changes span multiple modules, touch security/auth/release, or when the same issue fails two consecutive post-fix re-reviews (see governance.md).

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--dual` | none | Parallel Claude + Codex review. Details: [`${CLAUDE_SKILL_DIR}/references/dual-review.md`](${CLAUDE_SKILL_DIR}/references/dual-review.md) |
| `--security` | none | OWASP Top 10 security-only review (read-only). Details: [`${CLAUDE_SKILL_DIR}/references/security-profile.md`](${CLAUDE_SKILL_DIR}/references/security-profile.md) |
| `--ui-rubric` | none | 4-axis design quality scoring (0–10). Details: [`${CLAUDE_SKILL_DIR}/references/ui-rubric.md`](${CLAUDE_SKILL_DIR}/references/ui-rubric.md) |
| `--no-commit` | none | Disable auto-commit on APPROVE |

## Review Type Auto-Detection

| Recent Activity | Review Type | Perspectives |
|-----------------|-------------|--------------|
| After `harness-work` | **Code Review** | Security, Performance, Quality, Accessibility, AI Residuals |
| After `harness-plan` | **Plan Review** | Clarity, Feasibility, Dependencies, Acceptance |
| After task addition | **Scope Review** | Scope-creep, Priority, Feasibility, Impact |

## Verdict Framework

Establish severity classification before reviewing. See [`${CLAUDE_SKILL_DIR}/references/verdict-framework.md`](${CLAUDE_SKILL_DIR}/references/verdict-framework.md) for the full severity matrix and AI Residuals classification.

**Rule**: If critical or major findings exist → REQUEST_CHANGES. If only minor/recommendation → APPROVE.

## Code Review Flow

### Step 0: Reviewer Mode Auto-Detection (Browser vs Static)

> **Fork context auto-start (`REVIEW_AUTOSTART`)**: emit this as the very first output token in a forked session before any other processing.
>
> **Fork-context prohibition list** (5 forbidden failure modes):
> 1. Waiting for user confirmation before starting
> 2. Returning empty output when the diff is empty (output `{"verdict":"APPROVE","rationale":"no changes detected"}`)
> 3. Spawning a browser reviewer without checking `reviewer_profile` in the sprint contract
> 4. Writing to `Plans.md` or any `cc:*` marker
> 5. Exiting without emitting a JSON verdict

```
Does the change include UI files (.tsx, .jsx, .vue, .css, .html)?
├─ No  → Static reviewer (proceed to Step 1)
└─ Yes → Does the sprint-contract specify reviewer_profile: "browser"?
    ├─ Yes → Browser reviewer (launch browser-review-runner.sh)
    └─ No  → Is this a visual/design change?
        ├─ Yes → Browser reviewer recommended
        └─ No  → Static reviewer
```

Browser reviewer path: `bash "${CLAUDE_SKILL_DIR}/../../scripts/browser-review-runner.sh" --contract "${CONTRACT_PATH}"`

### Step 1: Collect Change Diff

```bash
CHANGED_FILES="$(git diff --name-only --diff-filter=ACMR "${BASE_REF:-HEAD~1}")"
git diff ${BASE_REF:-HEAD~1} --stat
git diff ${BASE_REF:-HEAD~1} -- ${CHANGED_FILES}
```

### Step 2: Static Scan for AI Residuals

```bash
AI_RESIDUALS_JSON="$(bash "${CLAUDE_SKILL_DIR}/../../scripts/review-ai-residuals.sh" --base-ref "${BASE_REF:-HEAD~1}")"
```

### Step 3: Review from 5 Perspectives

| Perspective | Check Items |
|-------------|-------------|
| **Security** | SQL injection, XSS, credential exposure, input validation |
| **Performance** | N+1 queries, unnecessary re-renders, memory leaks |
| **Quality** | Naming, single responsibility, test coverage, error handling |
| **Accessibility** | ARIA attributes, keyboard navigation, color contrast |
| **AI Residuals** | `mockData`, `dummy`, `fake`, `localhost`, `TODO`, `FIXME`, `it.skip`, hardcoded secrets |

Apply the severity framework from verdict-framework.md to each finding.

### Step 4: Output Review Result

See [`${CLAUDE_SKILL_DIR}/references/result-schema.md`](${CLAUDE_SKILL_DIR}/references/result-schema.md) for the full `review-result.v1` JSON schema.

For `--dual` flag: see [`${CLAUDE_SKILL_DIR}/references/dual-review.md`](${CLAUDE_SKILL_DIR}/references/dual-review.md)
For `--security` flag: see [`${CLAUDE_SKILL_DIR}/references/security-profile.md`](${CLAUDE_SKILL_DIR}/references/security-profile.md)
For `--ui-rubric` flag: see [`${CLAUDE_SKILL_DIR}/references/ui-rubric.md`](${CLAUDE_SKILL_DIR}/references/ui-rubric.md)

### Step 5: Commit Decision

- **APPROVE**: Execute auto-commit (unless `--no-commit`)
- **REQUEST_CHANGES**: Present critical/major findings. Auto-fix via `harness-work` fix loop (up to 3 times), then re-review.

## Plan Review Flow

See [`${CLAUDE_SKILL_DIR}/references/plan-review.md`](${CLAUDE_SKILL_DIR}/references/plan-review.md)

## Scope Review Flow

See [`${CLAUDE_SKILL_DIR}/references/scope-review.md`](${CLAUDE_SKILL_DIR}/references/scope-review.md)

## Anomaly Detection

| Situation | Action |
|-----------|--------|
| Security vulnerability | Immediately REQUEST_CHANGES |
| Suspected test tampering | Warning + fix request |
| Force push attempt | Reject + suggest alternative |

## Codex Environment

> Load [`${CLAUDE_SKILL_DIR}/references/codex-review.md`](${CLAUDE_SKILL_DIR}/references/codex-review.md)
> only when `command -v codex` succeeds **and** the user explicitly requests Codex or duo review.

## OpenCode Environment

> Load [`${CLAUDE_SKILL_DIR}/references/opencode-review.md`](${CLAUDE_SKILL_DIR}/references/opencode-review.md)
> only when `command -v opencode` succeeds **and** the user explicitly requests OpenCode review (e.g., `--opencode`, "use opencode", "opencode review").

↑ Claude will summarize this result. Type a new prompt to redirect or press Enter to continue.

## Related Skills

- `harness-work` — Implement fixes after review
- `harness-plan` — Create and modify plans
- `harness-release` — Release after review passes
