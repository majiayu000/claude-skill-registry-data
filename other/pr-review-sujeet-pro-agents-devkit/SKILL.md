---
name: pr-review
description: >-
  HEAVYWEIGHT, GitHub-only deep PR review. Takes a GitHub PR URL, prepares a read-only git
  worktree at the PR head (SSH clone only), and reviews the diff with full cross-file context via
  Read/Grep/Glob. Fans out one agent per dimension (correctness, security, tests, performance, api,
  docs, observability, concurrency, feature-flow) through the Workflow tool, then adversarially
  verifies every finding before it survives. Traces feature flags / experiments via the statsig
  MCP and pulls linked Jira/Confluence via the atlassian MCP. Posts inline review comments,
  a review summary, and appreciations through the gh CLI after confirmation. NEVER merges, never
  force-pushes, never edits the PR's code. For a quick read-only pass with no worktree, use /adk:review.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent, Workflow
argument-hint: "<pr-url> [-i|--interactive] [--scope security|correctness|tests|all] [--no-post] [--deep]"
---

# pr-review — deep PR review (heavyweight, GitHub-only)

A real reviewer's pass on a GitHub pull request: a checked-out worktree, cross-file context, a multi-dimension fan-out with adversarial verification, feature-flag tracing, and inline comments posted back to the PR. This is the heavyweight path. For a quick read-only skim with no worktree, use `/adk:review`.

**Scope is a GitHub PR URL only.** `https://github.com/<owner>/<repo>/pull/<n>`. Bitbucket, GitLab, and self-hosted forges are explicitly **out of scope** — see `rules.md`. All GitHub access is the `gh` CLI; all git is `git` directly; cloning is **SSH only**.

The full operating contract lives in this skill folder — read these as you need them:

| Aspect | File |
|---|---|
| How you review (voice, severity rubric, evidence rules) | `persona.md` |
| The phased process + the Workflow orchestration | `workflow.md` |
| Hard rules + refusals + safety | `rules.md` |
| Per-dimension review guide + feature-flow tracing | `dimensions.md` |
| Classifying pre-existing PR review threads | `comment-resolution.md` |

## Quick start

1. **Phase 0 — parse + auth.** Parse the URL → `(owner, repo, number)`. Verify `gh auth status`. (`workflow.md` Phase 0.)
2. **Phase 1 — checkout.** Ensure an SSH clone exists, `git fetch`, add a detached `git worktree` at the PR head SHA. The worktree is **read-only** — you never edit the PR's code.
3. **Phase 2 — gather.** PR metadata + diff + existing review threads via `gh pr view --json` / `gh pr diff` / `gh api`; linked Jira/Confluence via the atlassian MCP.
4. **Phase 3 — the Workflow.** Fan out one agent per dimension over diff + worktree, trace feature flags via the statsig MCP, then adversarially verify and synthesize. (`dimensions.md`, `workflow.md` Phase 3.)
5. **Phase 4 — threads.** Classify each existing review thread resolve / reopen / leave-as-is by re-checking the worktree at its anchor (`comment-resolution.md`).
6. **Phase 5–6 — triage + post.** Triage findings, then render inline comments + a summary + appreciations via the `gh` CLI. Confirm before transmitting.

## Workflow is the default

Every real PR gets the parallel-dimension **Workflow** in `workflow.md`: review fans out one dimension per agent → each finding is adversarially refuted by an independent skeptic → only survivors are reported. This catches what a linear pass misses and kills plausible-but-wrong findings. There is no "skip the workflow" fast path here — that's what `/adk:review` is for.

## Posting policy + merge policy

- **Posting inline review comments is the purpose of this skill**, so it happens by default in non-interactive mode — but you always **summarize what will post** ("about to post N inline comments + a summary on PR #X — proceed?") before transmitting, per `rules.md`. `--no-post` produces the report and posts nothing.
- The verdict is **approve** when there are no surviving blocker/critical findings and no thread needs reopening; otherwise **request changes** or **comment**.
- **NEVER merge a PR.** Even if asked, print the merge link and exit (`rules.md`). Recommend merge; the human clicks. Never force-push.

## Modes

- **default** — full review, post inline comments + summary + appreciations after a one-line confirmation.
- **`-i` / `--interactive`** — walk each finding (accept / reject / edit) before anything is posted.
- **`--scope security|correctness|tests|all`** — restrict the fan-out to one dimension family (default `all`).
- **`--no-post`** — review and report only; transmit nothing to the PR.
- **`--deep`** — stronger reasoning profile; auto-selected for security-sensitive, cross-module, or feature-flag-bearing diffs.
