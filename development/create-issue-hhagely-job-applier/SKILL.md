---
name: create-issue
description: Create a GitHub issue in this repo with consistent formatting that the fix-issue skill can consume. Gathers summary, context, current/expected behavior, and acceptance criteria, then calls `gh issue create` with a `claude-ready` label. Use when the user asks to file/open/create an issue, log a bug, or write up a task. Also invoked via /create-issue.
---

# create-issue

File a GitHub issue with a structured body so [fix-issue](../fix-issue/SKILL.md) (or any future automation) can pick it up cleanly. Consistent formatting matters more than length — empty sections beat freeform prose.

## When to Use

- User asks to "create an issue", "file a bug", "open a ticket"
- User describes a bug or task and says "let's track this"
- User invokes `/create-issue`

## Arguments

The user may pass a short description inline (e.g. `/create-issue dedupe SimHash misses near-duplicate JDs over 200 chars`). Treat it as the seed for the title and summary. If no argument is given, ask what the issue is about before continuing.

## Instructions

### Step 1: Gather the required fields

You need:

1. **Title** — short, imperative, under 70 chars. "Fix X" / "Add Y" / "Refactor Z".
2. **Summary** — one or two sentences. The problem or the change in plain language.
3. **Context** — where in the codebase this lives. File paths (e.g. `src/job_applier/filters/rules.py`, `web/src/routes/jobs/[id]/+page.server.ts`), package (`api/`, `sources/`, `filters/`, `models/`), or system name. Pull from the conversation if obvious; otherwise ask.
4. **Current Behavior** — what happens today. For a new feature, write `N/A — new feature`.
5. **Expected Behavior** — what should happen instead.
6. **Acceptance Criteria** — 2–5 checkbox items that define "done". Concrete and verifiable (e.g. "`make test` passes", "filter drops `Senior Sales Engineer`", "`/api/jobs/{id}/score` returns `MatchScoreHistory` snapshot count").

If the user's request already covers some of these, fill them in from context. Only ask for fields that are genuinely missing or ambiguous. Do not pepper the user with questions for things they obviously meant.

### Step 2: Confirm before filing

Show the user the full rendered issue body (the markdown that will go into GitHub) and the proposed title. Wait for confirmation — they will often tweak wording at this step.

### Step 3: File the issue

Ensure the `claude-ready` label exists, then file with a HEREDOC body:

```bash
gh label create claude-ready --description "Ready for Claude Code to pick up" --color 0E8A16 2>/dev/null || true

gh issue create --title "<title>" --label claude-ready --body "$(cat <<'EOF'
## Summary
<summary>

## Context
<context>

## Current Behavior
<current>

## Expected Behavior
<expected>

## Acceptance Criteria
- [ ] <criterion 1>
- [ ] <criterion 2>

## Notes
<notes — omit this section entirely if empty>
EOF
)"
```

### Step 4: Report

Return the issue URL printed by `gh issue create`. One line is enough.

## Conventions

- Always apply `claude-ready` by default. Add others (`bug`, `enhancement`) only if the user asks.
- Omit the **Notes** section entirely when there's nothing to add — don't leave a placeholder.
- Don't paste large code blocks or diffs into the body. [fix-issue](../fix-issue/SKILL.md) will read the actual code from **Context**.
- Never auto-assign. The repo is solo-maintained.
- This skill only files the issue. It does not branch or implement. That's [fix-issue](../fix-issue/SKILL.md)'s job.
