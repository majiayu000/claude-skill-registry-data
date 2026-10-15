---
name: resolve-issues
description: Map change groups to existing open issues with confidence scoring. Use when you have grouped file changes and need to determine which issue each group belongs to before committing.
user-invocable: false
---

# resolve-issues

Model-invocable skill for mapping change groups to existing repository issues.

## Purpose

Take grouped file changes and a list of open issues, then determine which issue each group maps to. Produce a confidence score for each mapping so the calling agent knows when to seek human approval.

You DO the mapping work. You do NOT decide what to do with unmapped groups — the calling agent handles that.

## Input

Receive from agent:
- `change_groups`: Structured output from `analyze-changes` — groups with type, scope, description, and files
- `open_issues`: List of open issues with number, title, labels, and body
- `branch_name`: Current branch name (may contain issue references)

## Process

### 1. Extract Signals

For each change group, collect mapping signals:

**Branch signal** — Does the branch name contain an issue number? (e.g., `feature/42-auth-flow` → issue #42). This is the strongest signal when present.

**Semantic signal** — Compare the group's scope, type, and file paths against each open issue's title, labels, and body. Look for:
- Issue title keywords matching the group's scope or description
- Issue labels matching the group's commit type (e.g., `bug` label → `fix` type)
- File paths mentioned in the issue body
- Component/area overlap between the group and the issue

**Proximity signal** — If multiple groups map to the same issue, that strengthens confidence (they're all part of the same work).

### 2. Score Confidence

For each group-to-issue mapping, assign a confidence level:

| Level | Criteria |
|-------|----------|
| `high` | Branch contains issue number AND semantic signals align, OR 3+ semantic signals agree |
| `medium` | Branch contains issue number but semantic signals are ambiguous, OR 2 semantic signals agree without branch signal |
| `low` | Only 1 weak semantic signal, OR multiple issues compete for the same group |
| `none` | No issue can be reasonably mapped — group is unmappable |

### 3. Detect Conflicts

Flag when:
- Two groups map to the same issue with conflicting types
- A single group has equal-strength signals pointing to different issues
- The branch references an issue that doesn't match any group semantically

## Output

Produce output using template: `templates/mapping-output.md`

Return a structured mapping for every change group — no group should be silently dropped.

**IMPORTANT**: This skill produces mapping data. The calling agent receives this output and decides what to do next (proceed, seek approval, or halt per NWWI). Do NOT instruct the agent to return or stop.

## Constraints

- NEVER create or modify issues — read-only access to issue data
- NEVER drop a group from the output — every input group must appear in the mapping
- NEVER assign `high` confidence without at least two corroborating signals
- ALWAYS flag conflicts explicitly rather than silently picking a winner
- ALWAYS include reasoning for each mapping so the agent can build a brief

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Category | analysis |
