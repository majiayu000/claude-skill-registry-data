---
name: handoff
description: Generates a comprehensive handoff spec for the current session so another agent can pick up exactly where this one left off. Triggered by /handoff.
---

# Handoff

Announce at start: `Generating a handoff doc...`

Capture the full context of this session into a `.md` spec another agent can act on cold, without
asking the user a single clarifying question. Self-containment is the whole bar.

## 1. Gather context

Pull all of it before writing anything - the doc is only as good as this step:

- Repo name from the working directory or `git remote get-url origin`
- Active branch (`git branch --show-current`)
- Uncommitted changes (`git status --short`, `git diff --stat`)
- Recent commits (`git log --oneline -10`)
- Existing plans, specs, and tasks under `~/.agents/plans|specs|tasks/<repo-name>/`
- This conversation: goals, decisions made, files touched, problems hit, solutions found, open
  questions, and what was left unfinished

## 2. Write the doc

Save to `~/.agents/handoffs/<repo-name>-<YYYY-MM-DD>-<short-slug>.md`, where the slug is 2–4
kebab-case words (`auth-refactor`, `beat-upload-fix`). Outside a git repo, use `scratch` as the repo
name.

```markdown
# Handoff: <Task Title>

**Repo:** <repo-name>
**Branch:** <branch-name or "no git">
**Date:** <YYYY-MM-DD>
**Session summary:** <1–2 sentences - what we were doing and why>

## Goal
What the incoming agent should achieve, with acceptance criteria when known.

## Current State
Where things stand right now: what works, what doesn't, what's half-done. Report it honestly rather
than rounding up. List uncommitted changes explicitly so the agent knows the tree is dirty. If the
session was exploratory with no concrete output, say exactly that.

## What Was Done This Session
Completed work, with file paths and line numbers where relevant.

## Decisions Made
Non-obvious choices and the reasoning behind them. This section is what stops the next agent from
re-litigating settled questions, so it always has content.

## Next Steps
Ordered and specific - name the file, the function, and the change, so step 1 needs no clarification.

## Open Questions
Anything unresolved or left for the user to decide. "None." if there are none.

## Key Files
- `path/to/file.ts` - what it does and why it matters here

## Constraints & Gotchas
What the incoming agent must avoid, edge cases it must handle, and the non-obvious constraints
discovered this session - especially any mistake you already avoided that a reasonable agent would
walk straight into.

## Environment Notes
Commands, env vars, credential patterns, known flaky tests. Omit when nothing is unusual.
```

Fill every section; "None." or "N/A" only where one genuinely doesn't apply.

## 3. Surface it

Print the full path, show the **Goal**, **Current State**, and **Next Steps** sections inline so the
user can spot-check, and close with:

> Handoff doc saved. Pass `~/.agents/handoffs/<filename>` to the next agent to continue.

The user can read the rest themselves - keep the other sections out of chat.
