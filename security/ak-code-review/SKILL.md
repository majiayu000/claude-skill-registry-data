---
name: ak-code-review
description: "Review code for bugs, regressions, maintainability, reliability and verification gaps with evidence."
when_to_use: "Invoke for pending changes, a PR number, a commit hash or a codebase scan."
category: workflow
keywords: [review, quality, verification, reliability]
argument-hint: "[#PR | COMMIT | --pending | codebase [parallel]] [--ultra] [--advice] [--yagni]"
metadata:
  author: agentkit
  version: "2.0.3"
  workflow:
    follows: [ak-test]
    precedes: [ak-ship]
---

# Code review

Review the requested scope against its specification, regression paths, security and
repository conventions. Review-only does not authorize edits, posting or merging. Resolve
current source/revision and use evidence; scores never substitute for checks or findings.

## Input Modes

Auto-detect from arguments. If ambiguous or no arguments, prompt via `ask_user capability`.

| Input | Mode | What Gets Reviewed |
|-------|------|--------------------|
| `#123` or PR URL | **PR** | Full PR diff fetched via `gh pr diff` |
| `abc1234` (7+ hex chars) | **Commit** | Single commit diff via `git show` |
| `--pending` | **Pending** | Staged + unstaged changes via `git diff` |
| *(no args, recent changes)* | **Default** | Recent changes in context |
| `codebase` | **Codebase** | Full codebase scan |
| `codebase parallel` | **Codebase+** | Parallel multi-reviewer audit |

**Resolution details:** `references/input-mode-resolution.md`

### No Arguments

If invoked WITHOUT arguments and no recent changes in context, use `ask_user capability` with header "Review Target", question "What would you like to review?":

| Option | Description |
|--------|-------------|
| Pending changes | Review staged/unstaged git diff |
| Enter PR number | Fetch and review a specific PR |
| Enter commit hash | Review a specific commit |
| Full codebase scan | Deep codebase analysis |
| Parallel codebase audit | Multi-reviewer codebase scan |


## Select the operation

- Review-only: compare spec/acceptance and quality, returning actionable findings with
  file/line, impact and evidence; use `references/spec-compliance-review.md` as needed.
- Receive feedback: `references/code-review-reception.md`; verify a finding before accepting it.
- Authorized fixes: repair confirmed findings in scope, then review the changed revision.
- Codebase scan: `references/codebase-scan-workflow.md`; parallel uses
  `references/parallel-review-workflow.md` when explicitly selected and supported.
- `--ultra` / `--advice`: `references/advanced-modes.md`; preserve their explicit checkpoints
  and the ultra/codebase-parallel conflict.

Use `references/checklist-workflow.md` for risky pre-landing work and
`references/task-management-reviews.md` only when coordination warrants tracking. A typo
review needs no orchestrated pipeline. Reuse checks when revision, inputs and environment
are unchanged; rerun affected checks after edits or changed assumptions.

Preserve the full requested scope; `--yagni` alone opts into scope cutting. Reject abstract
concerns contradicted by current source/tests and explain the evidence. Never reverse an
accepted product decision without a concrete user decision. Report verified findings and
limitations; do not claim correctness beyond the inspected scope.

## Optional finding-triage experiment

After candidate discovery, explicitly opted-in experiments may follow
[semantic triage](references/semantic-triage.md). Ordinary review remains unchanged.
