---
name: english-facing
description: In this repo the README and every commit message are written in English, never Chinese. Read and follow this before writing or editing README.md or any commit message. Scope is only those two surfaces — code comments and other docs keep their existing language; do not translate them unless asked.
---

# English-facing: README and commit messages

This repo is public and read by outsiders (an interviewer, among others). Two surfaces must always be
English:

- **README.md** — the front page.
- **Commit messages** — the whole message, subject and body, and any PR description.

That's the whole rule. Set 2026-09-17, after the entire history was translated to English once.

## What is NOT covered

- **Code comments** stay as they are (this repo has dense Chinese comments across `src/`). Don't
  translate them, and don't start writing new comments in English just because of this rule — match
  the file you're editing.
- **Other docs** (`docs/*`, skill files, etc.) keep their current language. `docs/NOTES.md` and
  `CLAUDE.md` happen to be English now; a doc that is Chinese stays Chinese unless the user asks.

If in doubt about a surface not listed above, leave its language alone.

## Chinese as data is fine

The rule is that the **prose** is English, not that Chinese characters are banned. A commit message
may — and sometimes must — quote Chinese that is *data*:

- a real filename or title the change touches (`Full passport_LL.pdf`, `_哔哩哔哩_bilibili`),
- a query or string the system processes, when it's the point (`今天做了什么` returning nothing, the
  bigram cut of `报错` into `报错 / 错截 / 截图`),
- a place name or example demonstrating multilingual behaviour (`泰晤士河 ↔ Thames`).

Stripping those would destroy the meaning. Keep them; write the sentence around them in English.

## Commit message style

Follow the existing `git log`: say **why**, not just what, and give the **measured numbers** that made
it the decision. Keep the attribution line the harness/CLAUDE.md specifies.

## If asked to translate history again

The one-time job (translate all Chinese commit messages, re-point the release tags, force-push) was
done once. If it's ever needed again: back up first (`git bundle create <file> --all`), build a
`SHA → new message` map, rewrite with `git filter-branch --msg-filter … --tag-name-filter cat -- main
v1.0.0 v1.0.1` (git-filter-repo isn't installed), and remember that force-pushing rewritten history to
a public repo means any other clone must reset, not pull.
