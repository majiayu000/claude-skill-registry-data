---
description: Given a proposed unit of work (a task, gap, feature, follow-up, etc.), find an existing open GitHub issue that already covers it — or create a new one. Use when the user asks to file, open, or track an issue, and after any analysis skill that surfaces work worth tracking.
---

Take a proposed unit of work and ensure there's exactly one GitHub issue
tracking it: either an existing open one the user confirms is a match, or a new
one this skill creates.

The dedupe gate is the user — this skill surfaces candidates, the user judges
whether any matches. It never silently merges into an existing issue and never
creates a duplicate when a match exists.

## Input

The calling skill (or user) should provide:

- **Title** — short, imperative, the kind of phrasing that would work as a
  GitHub issue title.
- **Body** — the full proposal: context, what needs to happen, acceptance
  criteria, links to relevant files.
- **Labels / domain hint** (optional) — labels to apply on creation, or a domain
  keyword to narrow the search.

If any of these are missing, ask the caller (or the user) before searching —
issue creation without a real body produces a low-quality issue.

## Step 1: Search for an existing match

Search the repo's open issues with a query built from the title's distinctive
nouns/verbs (skip generic words like "add", "fix", "the"). Restrict to open
issues (`is:open is:issue`). Resolve the repo from the git remote —
`gh repo view --json nameWithOwner --jq .nameWithOwner` — rather than assuming
one.

Either `gh search issues --repo <owner>/<repo> …` or
`mcp__github__search_issues` works; `gh` is the more reliable path in remote
sessions (see `/override-gh`).

If the title or body references a specific file path, symbol, or feature name,
include it in the query — those are the highest-signal terms.

## Step 2: Triage matches

- **0 results** → go to Step 3.
- **1+ results** → present the candidate(s) to the user:
  - Show each candidate's number, title, and URL.
  - Ask: "Does any of these already cover the proposal?"
  - Options: each candidate (`#<n> <title>`), plus "None — create a new issue".
  - In a **web/remote session**, ask as numbered prose rather than via
    `AskUserQuestion` — that UI drops answers after the session idles
    (`@.claude/skills/plan/SKILL.md` § Part 2). In a local CLI session
    `AskUserQuestion` is fine.
  - If the user picks an existing candidate: surface its number + URL to the
    caller and stop. Done.
  - If the user picks "None": go to Step 3.

If there are many candidates (>4), pre-filter to the most plausible ones in your
write-up before asking — don't dump a wall of unrelated issues into the
question.

**Steps 1–2 and Step 3 may run in different turns.**
`@.claude/skills/plan/carving.md` runs the search and triage at plan time, where
they touch nothing and the operator rules on any match while reviewing the
carve, and `/go` runs the creation on the go-ahead. Neither turn needs a mode
flag: the split falls on the numbering this skill already has, because Steps 1–2
are read-only and Step 3 is the only one that writes.

## Step 3: Create the issue

Create it with the title and body as provided, plus any labels the caller passed
in (`gh issue create --title … --body-file … --label …`, or
`mcp__github__issue_write` with action `create`). Return the new issue number
and URL to the caller.

**Then fill in any `#<tbd>` this issue resolves.** A branch whose PR was opened
before its issue existed carries the marker `@.claude/skills/pr/SKILL.md` Step 4
writes; this skill is the one place an issue is ever created, so it is the only
party that knows the number the moment it exists. Replace `#<tbd>` in the PR
body and anywhere else on the branch that carries it — one marker per issue
created, in the order the carve proposed them.

## Output

Return one of:

- `existing: #<n>` (URL) — user confirmed a match.
- `created: #<n>` (URL) — new issue created.

The caller decides what to do with the result (log it, surface it in a report,
etc.).

## Notes

- This skill is read-only for source code. It only writes to GitHub.
- Don't open PRs, don't comment on existing issues, don't change labels on
  existing issues — those are outside scope.
- If the user wants the proposal worked on now (not just tracked), the caller
  should chain into `/task` after this skill returns, passing the proposal and
  the number.
