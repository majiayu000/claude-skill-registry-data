---
name: triaging-issues
description: Triage open GitHub issues by ROI × feasibility — cluster by concern, score each, and propose a P0–P3 plan with execution order, quick wins, and evidenced close candidates. Use for "triage the issues" or "what should we work on next?".
compatibility: Designed for Claude Code
metadata:
  argument-hint: "[label-or-keyword]"
  allowed-tools: Bash, Read, Grep, Glob, Agent
  stability: experimental
---

# Triage GitHub Issues

**Filter**: $ARGUMENTS (optional label or keyword; empty = all open issues)

Read-only: never label, comment on, or close issues — present the plan; acting on it is a
separate, explicit step.

## Step 1: Fetch issues

```bash
gh issue list --state open --limit 200 --json number,title,author,labels,createdAt,updatedAt
```

If `gh` is missing or unauthenticated, stop and say so — do not guess the backlog. Apply the
filter if given. Read bodies (and comments) with `gh issue view <N> --json body,comments`.

## Step 2: Cluster by concern

Group issues by the concern they actually address (e.g. CI gates, a plugin's behaviour, docs,
proposals needing a decision) — derive clusters from the content, not a fixed taxonomy. Note
dependencies (X blocks Y) and duplicates.

## Step 3: Score each issue

| Dimension | Scale |
| --- | --- |
| **ROI** | H / M / L — user-visible impact, bugs breaking installs/runs rank highest |
| **Effort** | S < 0.5 d · M 1–2 d · L > 2 d — **from the actual code**, never estimated blind |
| **Risk / deps** | what could break, what must land first, what needs an owner decision |

Tier: **P0** do now (high ROI, low effort) · **P1** next · **P2** later / needs scoping ·
**P3** close or won't-do (with evidence).

For large backlogs, fan out one read-only subagent per cluster (Agent tool; or
`cc-meta:orchestrating-parallel-workers` if installed) and ground effort estimates by reading the
relevant code (`codebase-tools:researching-codebase` if installed).

## Step 4: Verify before asserting

The step triage most often gets wrong:

- **"Already fixed" / "superseded" / "close it" needs file-level evidence** — the current file
  on the default branch or the commit that fixed it. A plausible commit message is not evidence.
- Re-check any count you report (files, skills, affected items) at source; say how you counted.
- Verify vendor/library claims against a first-party source.
- A subagent's verdict is a hypothesis: spot-check the load-bearing ones yourself.

## Step 5: Output

1. **Rubric** used (one line).
2. **Per-cluster table**: `# | title | ROI | effort | risk/deps | tier | one-line rationale`.
3. **Execution order**: batches (which issues ship together), each marked agent-doable or
   owner-gated, with a done-when.
4. **Quick wins**: P0 items that are S effort.
5. **Close candidates**: each with its evidence, or marked unverified.

## Reference

Ported from `qte77/polyfetch-scrape` `.claude/commands/analyze-issues.md` (PRs #65, #69).
