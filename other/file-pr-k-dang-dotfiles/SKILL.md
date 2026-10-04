---
name: file-pr
description: File a concise pull request. Use when the user asks to file, open or create a PR.
---

# File PR

Before filing, check whether a PR for this branch already exists. Resolve the actual base — the existing PR's base if present, otherwise the parent branch for stacks or the repo default. Do not assume `origin/main`. Review the diff locally against that base to make sure its contents match the goal.

PR titles usually become commit messages, so follow the repository's title conventions. Look at recently merged PRs and Git history for examples. Prefer a concise, human-readable title that explains why the change matters:

BAD
> ❌ perf(server): negotiate permessage-deflate on the websocket

GOOD
> ✅ perf(server): cut websocket frame size by 70%+ with gzipping

Follow PR templates when they are available. The template owns the sections — never add top-level headings it does not define. Use show-me visuals inside its sections (e.g. under "Changes") to express the change compactly. If the template is explicitly minimal, skip the outline entirely.

Open the description with a simple explanation of the problem based on the user's original prompt, then briefly explain the solution. Do not lead with an implementation inventory:

BAD
> ❌ Removed implicit workspace carry-over from every "new thread" entry point (cmd +n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads inherit only the project from context; branch, worktree, and env mode always come from the configured defaults. Deleted buildContextualThreadOptions, startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.

GOOD
> ✅ My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

## Context gathering

Gather only what is needed to explain the change: the ticket/task artifacts, the complete diff against the base plus enough surrounding code to understand behavior and ownership, and `gh pr view` metadata / changed files when a PR already exists.

## Change outline

Every PR follows the opener with at least one visual, in place of prose or a file-by-file changelog. Scale the outline to the change:

- Simple single-concern PRs get one small visual showing the core logic or data flow.
- Complex PRs get a fuller outline. Complex means the reviewer could misread scope without it: multiple areas, cross-package changes, API/SQL contract changes, migrations, or surprising decisions/omissions.

Include only views that help explain this PR, ordered to tell the story. Omit categories that did not change. See `references/show-me.md` for formatting conventions.

- Endpoint request/response contracts and SQL table / column changes.
- Key data structure / type changes.
- Pseudocode for changed business logic.
- Shallow file tree showing changed responsibilities.
- React component tree changes, including important hooks, state, and package boundaries.
- Call-tree, control-flow, or data-flow changes.

Prefer `diff` blocks when showing changes to an existing shape. Show the complete target shape when most of it is new or diff notation would obscure ownership or order.

Write as one human talking to another: simple, coherent, concise language, no jargon or slang.

## Report completion

After filing or updating, respond with the PR URL, a 2-3 sentence summary of what it does plus key decisions, and a concise list of changed files with one-line descriptions.

