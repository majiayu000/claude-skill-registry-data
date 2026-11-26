---
name: committing
description: >-
  Makes clean git commits in the project's own style. Use when the user asks to commit, write a commit message, split changes into commits, or open a PR. Not for reviews or explaining history.
license: Apache-2.0
metadata:
  level: "atomic"
  uses: ""
  agents: ""
  tokens: "556"
---

Commit only your own finished changes, in small focused commits, in the message style the project already uses.

Path: one obvious change → steps 1, 3, 5 and one commit, no ceremony; mixed changes → propose a split first. Say which path in one line.

## Steps
1. Run `git status` and `git diff` (staged and unstaged). Separate what you changed for this task from other changes in the tree.
2. Mixed or unrelated changes: propose the split (one logical change per commit, with file lists and messages) and wait for the user's ok.
3. Find the message style: the project's CLAUDE.md first (Workflow, Conventions, git section), else `git log --oneline -10`. Match language, tense, prefix and length. Add a trailer (Co-Authored-By etc.) only if the project's rules or the session's attribution instructions call for one.
4. Check the files to stage for secrets (`.env`, keys, tokens, credentials) and junk (build output, logs, scratch files, debug lines). Leave them out and tell the user.
5. Stage by path (`git add <path>…`). Run `git diff --cached -U0 | grep -n '^+.*\[DEBUG-'`; a hit is a temporary debug line you are about to commit (foma-skills:debugging tags them): remove it, restage, then commit. Removed lines do not count.
6. Commit now only if the user asked to commit or the project's CLAUDE.md says to commit after each finished task. Otherwise show the proposed message and staged files and ask first.
7. Run `git status` to confirm what was committed and what remains.

## Rules
- Never `git add -A`, `git add .` or `git commit -a`; they pick up files you did not change.
- Never push without an explicit ask in this conversation; a past ask does not carry over.
- Never amend, rebase, force-push, `reset --hard`, `clean -f`, `branch -D`, `checkout .` / `restore .`, or skip hooks (`--no-verify`) without an explicit ask for that exact action.
- A failing hook is fixed, not bypassed; make a new commit rather than amending.
- One logical change per commit; never mix refactor, feature and formatting.

If the user asks to open a PR, read `references/pull-request.md`.

## Report
- Commit hash(es) and message(s), or the proposed message awaiting ok.
- Left uncommitted, if anything, and why.
- Not checked: <…>
