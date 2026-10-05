---
name: help
description: Think before typing. Root cause first, two candidate fixes, pick one, ask if still unclear, then change only the files the request needs. Edit the confidence bar and scope rules to fit the project. Use when a bug report comes in, when a previous fix did not work, or when the request is vague.
---

# Help

Slow down for thirty seconds before the first edit. It saves an hour later.

## Reflect before acting

1. Why does the current code not do what the user wants? Read it. Do not guess.
2. What is missing, wrong, or incomplete relative to the request?
3. List two or three candidate causes.
4. Pick the most likely one and say why.
5. If the answer to "what is unclear" is not empty, ask one question and stop.

Never assume. A wrong assumption costs more than a question.

## Confidence bar

Do not write code below [98]% confidence in what needs to change. Below that: read more, ask, or propose a plan instead of a diff.

## Convex rules

- Mutations map form fields to document fields one to one. Field names match.
- Patch without reading when possible. Indexed queries for ownership. Idempotent with early returns. `Promise.all` for independent writes.
- Load the matching `convex-*` skill for anything deeper.

## Scope

Change:

- Files the request needs.
- The schema, if the request needs it.
- `changelog.md`, `files.md`, `task.md` after the change lands. Dates from `git log --date=short`, never invented.

Do not change:

- UI, layout, colors, or copy that the request did not mention.
- Existing sections, features, or components. Nothing gets removed without being asked.
- [Add project specific protected areas: admin dashboard, billing flow, etc.]

## UI

- Site design system for every popup, alert, modal, toast, confirmation. Never the browser default.
- Vercel Web Interface Guidelines: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/refs/heads/main/AGENTS.md

## Docs policy

Do not create README, CONTRIBUTING, SUMMARY, or USAGE files unless asked. A short summary in the reply is enough.

## Git

Load `git-safety` before any git command that could discard work. Short version: `git status` first, `git diff` before discarding, edit files by hand to undo, never `reset --hard` / `checkout -- .` / `clean -fd` / `stash drop` without the user saying yes to that exact command.

## Checklist

Before the first edit:

- [ ] I can name the root cause
- [ ] I considered at least two fixes and picked one for a reason
- [ ] I am at or above the confidence bar
- [ ] I know which files change and which do not
- [ ] Anything unclear has been asked

Before saying done:

- [ ] The fix was verified, not just written
- [ ] Nothing outside the request changed
- [ ] Docs synced if the change was non trivial
