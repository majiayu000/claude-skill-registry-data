---
name: devlog-generation
description: Generate comprehensive development logs from git history, documentation, and code artifacts. Use when creating project history, onboarding to unfamiliar.
---

# DevLog Generation

Synthesize a complete, structured development log from a repository's git history, documentation, and code artifacts to serve as a durable knowledge base for developers and AI assistants.

## When to Use This Skill

Use this skill when you need to:

-   Generate a full development history for a project that lacks one
-   Onboard to an unfamiliar codebase by reconstructing its evolution
-   Recover development context after a lost or corrupted devlog
-   Create a troubleshooting knowledge base from historical commits
-   Audit project decisions and their rationale retroactively
-   Prepare a project handoff with full context

**Trigger phrases**: "generate devlog", "create development log", "reconstruct project history", "build devlog from git", "development history", "project timeline"

## What This Skill Does

### Core Capabilities

1.  **Source Material Collection**: Gather git commits, tags, branches, documentation, code comments, and (optionally) PR/MR data
2.  **Timeline Synthesis**: Cluster commits into logical units of work aligned with features, releases, and milestones
3.  **Entry Generation**: Produce rich entries covering what changed, why, decisions made, troubleshooting trails, and downstream impact
4.  **Cross-Referencing**: Correlate CHANGELOG entries, PR descriptions, and inline comments with commit clusters for maximum context density

### Entry Structure

Each devlog entry contains five sections:

| Section | Purpose | Required |
|---------|---------|----------|
| What Changed | Concise summary of modifications | Always |
| Why It Changed | Motivation, triggers, requirements | Always |
| Decisions Made | Trade-offs, alternatives, rationale | When design choices were made |
| Troubleshooting Trail | Failed attempts, errors, solutions | When debugging occurred |
| Impact & Context | Affected modules, downstream effects | When cross-cutting changes |

## Instructions

### Step 1: Analyze the Git Timeline

Establish the project's full chronological history:

```bash
# Full commit timeline (oldest first for analysis)
git log --format="%H|%ai|%an|%s" --reverse

# Tag/release milestones
git tag -l --sort=version:refname

# Branch topology
git log --all --oneline --graph --decorate --first-parent

# Identify large/significant commits
git log --shortstat --format="%H %s" | head -100
```

Key analysis tasks:
-   Identify the natural "chapters" of the project (initial setup, major features, releases)
-   Note merge commits as boundaries between logical units
-   Flag commits with keywords: "fix", "revert", "workaround", "hack", "breaking"

### Step 2: Gather Supporting Documentation

Read all available documentation sources in the repository:

-   **Primary sources**:
    -   `README.md`
    -   `CHANGELOG.md`
    -   `docs/DEVLOG.md` (existing, if any)
    -   `tasks/todo.md`, `tasks/lessons.md`
-   **Secondary sources**:
    -   `docs/` or `guides/` directories
    -   ADR files (Architecture Decision Records)
    -   `.github/PULL_REQUEST_TEMPLATE.md` (for PR context patterns)

For each source, extract:
-   **CHANGELOG.md**: Version-tagged change summaries (map to git tags)
-   **README.md**: Project purpose evolution (compare across git history with `git log -p README.md`)
-   **tasks/lessons.md**: Captured failure patterns and solutions
-   **Inline comments**: Search for `TODO`, `FIXME`, `HACK`, `WORKAROUND`, `XXX` comments across the codebase

### Step 3: Gather PR/MR Context (Optional)

If the repository is hosted on GitHub and the `gh` CLI is available:

```bash
# Merged PRs with descriptions
gh pr list --state merged --limit 100 --json number,title,body,mergedAt,headRefName

# PR review comments (for significant PRs)
gh pr view <number> --json reviews,comments
```

Map each PR to its commit range using the branch name or merge commit. If the `gh` CLI is not available, note this as a gap and proceed with git-only sources.

### Step 4: Cluster Commits into Logical Units

Rules for clustering:

1.  **Release boundaries**: Every tagged release starts a new cluster
2.  **Feature branches**: Commits from the same feature branch form one cluster
3.  **Time proximity**: Consecutive commits on the same day by the same author touching the same files form one cluster
4.  **Semantic grouping**: Commits with the same conventional commit scope (e.g., `feat(auth)`) form one cluster
5.  **Standalone significance**: Any commit with 10+ files changed, a revert, or a hotfix gets its own cluster

For each cluster, determine:
-   **Date**: Use the date of the last commit in the cluster
-   **Title**: Derive from the most descriptive commit message or the PR title
-   **Category**: `[feature]`, `[bugfix]`, `[refactor]`, `[decision]`, `[infra]`

### Step 5: Generate Entries

For each cluster (newest first), produce an entry using this template:

```markdown
## [YYYY-MM-DD HH:MM] — [Short Descriptive Title] [category-tag]

### What Changed
Concise summary of changes: features, fixes, refactors, dependency updates.

*   Modified `path/to/file`: Brief description
*   Added `path/to/new-file`: Purpose
*   Deleted `path/to/old-file`: Reason

### Why It Changed
Motivation, triggering issue, or requirement. Reference issue numbers or user reports.

### Decisions Made
*   **Chose X over Y**: Reasoning
*   **Rejected Z**: Reasoning

### Troubleshooting Trail *(if applicable)*

<details>
<summary>Expand troubleshooting details</summary>

*   **Attempt 1**: What was tried
    *   *Result*: Failed
    *   *Error*: `error message`
    *   *Analysis*: Why it failed
*   **Attempt 2 (Solution)**: What worked
    *   *Key Insight*: What made the difference

</details>

### Impact & Context
*   **Affected**: `module-a`, `module-b`
*   **Downstream**: Effects on other parts of the system
```

**Category tags**: `[feature]`, `[bugfix]`, `[refactor]`, `[decision]`, `[infra]`

**Guidance for each section**:
-   **What Changed**: Map directly to git diffs. List specific files where possible.
-   **Why It Changed**: Capture intent that is often lost in commit messages. Reference issues, user reports, or architectural goals.
-   **Decisions Made**: Serve as lightweight ADR (Architecture Decision Record) entries. Include rejected alternatives with reasoning to prevent future developers from re-evaluating settled decisions.
-   **Troubleshooting Trail**: Use collapsible `<details>` to avoid cluttering the file while preserving critical debugging context. This is the highest-value section for AI assistants trying to avoid repeated dead ends.
-   **Impact & Context**: Help readers scope the blast radius of changes without reading diffs.

### Step 6: Assemble the DevLog File

1.  Start with the file header:

    ```markdown
    # Development Log

    > A comprehensive record of this project's development history.
    > For AI assistants: use this file to understand what has been tried, what worked, what failed, and why.
    > Generated by the `generate-devlog` command. Maintained incrementally via `update-devlog`.
    ```

2.  Append all entries in **reverse chronological order** (newest first).

3.  Use consistent `## [YYYY-MM-DD HH:MM]` heading format. For entries where exact time is unknown, use `00:00` as placeholder.

4.  If `docs/DEVLOG.md` already exists, **warn the user** before overwriting. Offer to create a backup as `docs/DEVLOG.backup.md`.

### Step 7: Validate and Report

After generation, verify:

-   Every tagged release has a corresponding entry
-   Entries are in strict reverse chronological order
-   No duplicate entries for the same logical unit
-   Category tags are consistently applied
-   File paths referenced in entries actually exist (or existed at that point in history)

Report summary in chat:

```
Generated DEVLOG.md: X entries, spanning [earliest date] to [latest date].
Sources: git history (Y commits), CHANGELOG.md, [other sources].
Coverage: Z releases, W feature branches.
```

## Handling Edge Cases

### Very Large Repositories (1000+ commits)
-   Focus on tagged releases and merge commits as primary entry sources
-   Batch analysis in chunks of 100 commits
-   Prioritize entries for tags, merges, and high-impact commits
-   Group maintenance commits (dependency updates, formatting) into monthly summaries

### Repositories Without Tags
-   Use date-based grouping (weekly or bi-weekly clusters)
-   Identify "milestone" commits by diff size or message keywords

### Missing Context (No CHANGELOG, No PRs)
-   Rely on commit messages and diffs as primary source
-   Flag entries with low confidence: `*(Inferred from commit messages only)*`
-   Recommend the user review and enrich flagged entries

### Squash-Merged Repositories
-   Each squash-merge commit becomes one entry
-   Use the squash commit message (typically contains the PR description) as the primary source

## Quality Checklist

-   [ ] All tagged releases have corresponding entries
-   [ ] Entries are in strict reverse chronological order
-   [ ] Each entry has at minimum "What Changed" and "Why It Changed" sections
-   [ ] Decisions sections include rejected alternatives with reasoning
-   [ ] Troubleshooting trails use collapsible `<details>` sections
-   [ ] Category tags are consistently applied to all entries
-   [ ] File paths use backtick formatting
-   [ ] Date format is consistent (`[YYYY-MM-DD HH:MM]`)
-   [ ] File header includes purpose statement and maintenance guidance
-   [ ] User was warned before overwriting any existing DEVLOG.md

## Related Skills

-   `code-commit-workflow` — Commit message conventions that feed into devlog generation
-   `technical-documentation` — Broader documentation practices
-   `context-manager` — Maintaining context across large codebases

---

**Version**: 1.0.0
**Last Updated**: February 2026


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1.  **Execute**: Perform the core steps defined above.
2.  **Review**: Critically analyze the output (coverage, quality, completeness).
3.  **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4.  **Loop**: Continue until the definition of done is satisfied.
