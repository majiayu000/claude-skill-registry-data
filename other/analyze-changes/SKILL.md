---
name: analyze-changes
description: Analyze uncommitted changes for categorization and risk assessment
user-invocable: false
model: sonnet
allowed-tools: Bash, Read
---

# analyze-changes

Model-invocable skill for analyzing uncommitted changes.

## Purpose

Analyze uncommitted changes and produce structured analysis for the calling agent.

You DO the analysis work. You do NOT make decisions about what to do with it.

## Input

Receive from agent:
- Request to analyze current uncommitted changes

## Process

1. **Read State**
   ```bash
   git status --porcelain
   git diff --name-only
   git diff --stat
   git diff
   git branch --show-current
   ```

2. **Categorize Each File**

   Load categories from: `~/.garura/core/memory/standards/rules/commits.md`

3. **Detect Risks**

   Load patterns from: `reference/risks.md`

4. **Group by Issue**

   The primary grouping dimension is ISSUE, not component or file location.

   **Grouping rules (in priority order):**
   1. **Branch signal first** — extract issue number from branch name (e.g., `feature/95-foo` → #95). All changes on a single-issue branch default to ONE group for that issue.
   2. **Split only when multiple issues are present** — if the working tree contains changes for different issues (e.g., a hotfix mixed with feature work), split into one group per issue.
   3. **Within an issue group, pick the dominant commit type** — if an issue group has mostly `feat` files with a few `docs` files, the type is `feat`. Only split by type within an issue if the types are genuinely unrelated (e.g., a `fix` for issue #78 and a `feat` for issue #95).
   4. **Never split a single issue into multiple groups by component** — agents, skills, plays, and memory changes for the same issue are ONE commit, not separate commits per directory.

   **When to split within a single issue (rare):**
   - Changes include a genuinely unrelated `chore` (e.g., dependency bump) alongside feature work
   - STM/evidence artifacts that are operational, not part of the feature itself

## Output

Write the grouped analysis to the contract's `outputs.analysis` path as **YAML in the
executor's schema** — `commit-change/scripts/execute_commits.py` consumes this file
mechanically, so the schema is a hard contract, not a style. The exact shape (with field
notes) is in `templates/analysis-output.md`:

```yaml
needs_judgment: false          # always false on output — the judgment is now done
change_groups:
  - id: <kebab-slug>           # `id`, NOT `name`
    issue: <n>                 # bare number, no '#'
    commit_type: <type>        # `commit_type`, NOT `type` — feat|fix|refactor|docs|chore|test
    scope: <area>
    subject: "<imperative subject>"   # no issue suffix — the executor appends (#issue)
    files:                     # PLAIN repo-relative paths only.
      - <path>                 # a rename lists BOTH sides as separate entries
      - <old-path>             #   (never "old -> new" in one string)
      - <new-path>
exclusions:                    # carry the scan's exclusions through unchanged
  - path: "<path>"
    reason: "<why>"
    blocking: false
risks:
  sensitive_files: []          # paths that must block the run, [] when clean
```

Every changed file from the scan lands in exactly one group's `files` or in `exclusions`.
Any extra keys (notes, eval evidence, confidence) are tolerated but ignored by the
executor — never rename or omit the contract keys above.

**IMPORTANT**: This skill produces analysis data. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop — the agent continues its workflow after receiving this analysis.

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Category | analysis |
