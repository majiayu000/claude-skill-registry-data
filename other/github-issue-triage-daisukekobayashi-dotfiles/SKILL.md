---
name: github-issue-triage
description: Use only when the user explicitly invokes $github-issue-triage or names github-issue-triage. Triage open GitHub issues in the current repository, recommend the next issue to handle, and identify safe parallel work candidates without starting implementation.
---

# GitHub Issue Triage

## Scope

Use this skill to answer questions like:

- Which open GitHub issue should we handle next?
- Which issues can be worked on in parallel?
- Which issues are blocked, parent trackers, or future-scope work?

This skill is for current-repository triage only. It recommends work; it does
not start implementation.

## Workflow

1. Resolve the current repository from local git context.
   - Confirm the branch and dirty state with `git status --short --branch`.
   - List other worktrees with `git worktree list --porcelain`, and map each to an issue number when its branch or path names one; report the rest as unmapped.
   - Resolve the GitHub repository with `gh repo view --json nameWithOwner,url,defaultBranchRef`.
2. Fetch the current GitHub state.
   - List open issues with `gh issue list --state open --limit 100 --json number,title,labels,assignees,updatedAt,createdAt,url`.
   - List open pull requests with `gh pr list --state open --limit 50 --json number,title,headRefName,baseRefName,labels,updatedAt,url`.
   - For each plausible work issue, fetch details with `gh issue view <number> --json number,title,body,labels,comments,url,state`.
   - Collect each issue's dependencies from `Blocked by #<n>` lines in its body and from GitHub's native relationships: `gh api repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by` and, for trackers, `gh api repos/<owner>/<repo>/issues/<number>/sub_issues`.
   - If a relationship API is unavailable or fails, use the body lines alone and mention that native relationships could not be read.
   - Collect each issue's `Touched Areas` section when present.
   - For open PRs that may overlap with candidate issues, fetch changed files with `gh pr view <number> --json files`.
3. Read local repository guidance before ranking.
   - Check project instructions such as `AGENTS.md`.
   - Check product or roadmap docs if present, commonly `README.md`, `docs/*.md`, `WORKFLOW.md`, or milestone docs.
   - Use this context to filter out work that violates product scope or repository rules.
4. Classify each open issue.
   - Parent tracker or milestone issue.
   - Directly actionable implementation issue.
   - Blocked by another issue or PR. Treat an issue as blocked while any of its blocking issues is still open, whether the dependency came from a `Blocked by #<n>` line or a native relationship.
   - If body lines and native relationships disagree, use their union and note the disagreement.
   - Future-scope or out-of-scope work.
   - Duplicate or already represented by an open PR.
   - Already in progress in another local worktree.
5. Rank actionable issues.
   - Prefer issues that unblock later work, especially precursor issues that settle a contract for several blocked issues.
   - Prefer work aligned with current product direction and repository instructions.
   - Prefer clear acceptance criteria and moderate blast radius.
   - Defer broad, ambiguous, high-risk, or future-scope work unless it is explicitly the priority.
   - Treat parent tracking issues as coordination items, not the next coding task, unless all children are complete.
6. Identify parallel work candidates.
   - Build the current wave: actionable issues that have no open blocking issues.
   - Within the current wave, group issues as parallel only when their touched areas do not overlap, including shared resources such as schemas, config, migrations, lockfiles, or public interfaces.
   - Also check each candidate's touched areas against the changed files of open PRs, and flag overlaps as conflicts with in-flight work.
   - For other worktrees that may overlap candidates, list changed files with `git -C <path> diff --name-only <default-branch>...HEAD` and `git -C <path> status --short`, and flag overlaps the same way. Skip worktrees with no changes.
   - When an issue has no `Touched Areas` section, infer its likely areas from the body and repository, and label them as inferred.
   - Do not recommend parallel work when one issue defines policy, schema, or workflow behavior that another issue depends on.
   - Mention likely conflict areas such as shared config modules, schemas, migrations, job orchestration, or the same UI files.
7. Recommend the next step without starting work.
   - Give exactly one best next issue.
   - If useful, suggest the follow-up command, for example `$github-issue-start #23`.

## Output Format

Use this structure:

```markdown
**Current State**
- Open issues: <count>
- Open PRs: <count>
- Active worktrees: <count, mapped issues>
- Local branch/state: <short note>

**Recommended Order**
| Rank | Issue | Recommendation | Reason |
|---|---|---|---|
| 1 | #<n> <title> | Do next | <why> |

**Parallel Work**
- Current wave: #<a>, #<b> (<parallel groups, or why they must not run together>)
- Overlaps: <touched-area overlaps between issues or with open PRs or worktrees, or "none">
- Next wave after #<n> closes: #<c>, #<d>
- Or: "No safe parallel split right now"

**Next Step**
- Start with `$github-issue-start #<n>` if the user wants to implement the top recommendation.
```

Keep the report concise, but include enough reasoning that the recommendation
is auditable.

## Guardrails

- Do not create worktrees, branches, commits, pull requests, or issue comments.
- Do not edit repository files.
- Do not close, label, assign, or otherwise mutate GitHub issues.
- Do not assume cross-repository work.
- Do not force unrelated issues into a parallel plan just because multiple issues are open.
- If GitHub authentication or network access blocks issue reads, report the blocker and stop.
- If product intent is unclear after reading local docs and issue bodies, ask a focused question before ranking.
