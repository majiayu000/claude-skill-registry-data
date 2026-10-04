---
name: code-review
description: "Review a PR or feature branch commit by commit so sync-merged changes are not misattributed. Skip feedback on uncommitted edits (verify) and quality questions with no PR or branch context."
argument-hint: "[base-branch]"
allowed-tools: Bash, Read, Glob, Grep, Agent
effort: max
disable-model-invocation: false
---

Review the current branch's PR changes per-commit.

Base branch: $ARGUMENTS (if empty, infer from branch naming or ask)

## Current Context
- Branch: !`git branch --show-current 2>/dev/null || echo "N/A"`
- Commits on branch: !`git log --oneline main..HEAD 2>/dev/null || git log --oneline -10 2>/dev/null || echo "N/A"`

## When to dispatch to `reviewer` agent

For PRs with many commits or a large diff, spawn the `reviewer` subagent via the Agent tool to keep per-commit analysis out of the main context. Run the steps below inline only for small PRs.

Use **inline** when:
- 1–2 unique commits
- Diff under ~200 lines
- Review scope is narrow (single feature or fix)

Dispatch to **`reviewer`** when:
- 3+ unique commits
- Diff exceeds ~400 lines
- Multiple modules touched

Dispatch to a separate context to keep the main thread clean:
- **Claude Code**: `Agent(subagent_type: "reviewer", description: "<short>", prompt: "Base branch: <base>. Focus: <optional>. Branch: <current>. Unique commit/surface inventory: <...>. Requirement/convention source inventory: <...>.")`
- **Codex CLI**: `codex exec` with the same focused prompt and provenance packet. Codex's `multi_agent_v1.spawn_agent` is explicit-request-only (not for auto-dispatch), so spawn a `codex exec` subprocess instead.

The parent completes Steps 1–2 before dispatch. Do NOT re-run delegated per-commit analysis, synthesize missing preflight content, or retry an invalid return into success. Before surfacing it, mechanically validate:

1. Unique-commit inventory appears before Context Preflight, which appears before findings.
2. `Requirements`, `Conventions`, `Impact`, `Tests`, and `Unknowns` are all present and non-empty or explicitly `none`.
3. Every Impact/Tests `[seed:...]` SHA/path/symbol-or-`@file` exists in the dispatched unique-commit inventory; a sync-merged seed is invalid.
4. Every returned requirement, convention, Unknown, and finding-context source ID exists in the dispatched inventories; all available requirements and conventions are covered; all unavailable/conflicting requirements appear under Unknowns. `Requirements: none` or `Conventions: none` is valid only when its inventory is empty.
5. Every finding whose `[context:<source-id>]` is unavailable/conflicting is `[status:Unverified]`.
6. Every finding's `[commit:<sha>]` exists in the dispatched unique-commit inventory.

A valid return reports `Review status: COMPLETE`. An invalid return reports `Review status: INCOMPLETE`, includes a fenced validator result naming every failed check, and keeps delegated findings reference-only with context-dependent claims unverified.

## Steps

### 1. Identify unique commits

`<base>..HEAD` already excludes commits reachable from `<base>`, so no extra cross-reference is needed.

Prefer `--first-parent` — it collapses each sync-merge from base into a single commit on the feature branch, making sync-merged code easy to identify and skip:

```bash
git log --first-parent --oneline <base>..HEAD
```

Fallback: if the branch has unusual merge topology and raw merge commits still appear in the output, use `--no-merges` to drop them entirely:

```bash
git log --no-merges --oneline <base>..HEAD
```

These are the ONLY commits to review. When `git show <merge-commit>` produces a massive diff, that diff is the sync-merged code from base — SKIP it (per Step 5 Cross-verify).

### 2. Context Preflight

After identifying unique commits and before inline analysis or delegation, build this bounded read-only provenance packet from only their changed surfaces:

```text
Unique commit inventory
- <sha>: <changed paths and changed symbols>

Requirement source inventory
- <source-id>: status=<available|unavailable|conflicts-with:<source-id>> locator=<path|URL|user-scope> content=<compact requirement excerpt or access error>

Convention source inventory
- <source-id>: locator=<repository path> content=<compact relevant convention excerpt>
```

Read available user scope, PR/Jira requirements, active-plan criteria, repository-local AGENTS/rules, and relevant project patterns. Add no network authority; record unavailable remote context instead. If `.agents/review-lessons.md` exists, read it as past review evidence, NOT as convention: its `Adopted` entries rank below every written project rule and never override one, `Candidates` are context only, and `Rejected points` must not be re-raised as findings. Its absence is recorded as absent — never a reason to collect, which is `/review-lessons`, the only network-touching step in that loop. Use code-graph support when available, falling back to repository search and language-native tools. Keep discovery relevant to the unique changed surfaces rather than auditing the whole repository.

Present the result before findings:

```text
Context Preflight
- Requirements: [source:<source-id>] <available requirement>, or none
- Conventions: [source:<source-id>] <relevant convention>, or none
- Impact: [seed:<unique-sha>:<changed-path>:<changed-symbol|@file>] <impacted target>, or none
- Tests: [seed:<unique-sha>:<changed-path>:<changed-symbol|@file>] <test path or observable>, or none
- Unknowns: [source:<source-id> status:unavailable|conflict] <detail>, or none
- Past lessons: [lesson:<id> state:adopted|candidate type:correctness|convention|preference] <point>, or none
```

Use canonical `@file` for config, documentation, assets, deletions, or any file-level change without a language symbol. Impacted targets and related tests may be outside the diff, but every seed must be in the unique-commit inventory. Never seed discovery from a branch-wide diff or sync-merged surface. Surface conflicting requirements without resolving them silently.

Every finding must carry `[commit:<unique-sha>]`, `[context:<source-id>|none]`, and `[status:Verified|Unverified]`. A finding dependent on unavailable or conflicting context is `Unverified`, not asserted.

### 3. Review per-commit

For each unique commit:

```bash
git show <commit> --stat   # scope check
git show <commit>          # full diff
```

Do NOT use `git diff <base>..HEAD` for line-level review — it includes sync-merged changes.

### 4. Branch diff for context only

`git diff <base>..HEAD --stat` is acceptable for overall scope, but flag issues only if they trace back to a unique commit.

### 5. Cross-verify before flagging

Before reporting any issue:
1. Identify which commit introduced it
2. If the commit is NOT unique (i.e., from a sync merge), do NOT flag it

### 6. Next step (optional)

After fixes are committed, suggest running `/pr-body` to generate the PR description.

## Rules

- Only review changes from unique commits (Step 1)
- Run Context Preflight before findings and preserve its provenance tags
- Match the project's language and conventions
- Keep feedback actionable and concise
