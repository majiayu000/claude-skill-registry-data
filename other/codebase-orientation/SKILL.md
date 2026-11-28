---
name: codebase-orientation
description: Fast recon before changing unfamiliar code — instructions, manifest, tree, one flow traced end-to-end, git history, newest precedent. Use when starting in a repo or module you haven't touched this session, when asked "where does X live" or "how is Y wired", or before designing against an existing architecture. Not for a one-line edit to a file already open in the conversation.
---

# Codebase Orientation

Weak orientation reads the one file named in the request and starts editing; the result fights the repo's architecture and gets rewritten in review. Strong orientation spends 5–10 minutes on breadth-first reads, then edits where the existing analog lives, in the repo's idiom.

## The recon sequence

1. **Instructions first.** CLAUDE.md / AGENTS.md / CONTRIBUTING / README, in that order. They override your defaults and usually name the gotchas you would otherwise rediscover.

2. **The manifest.** `package.json` scripts, Makefile, justfile, pyproject, Cargo.toml: how to build, test, lint, run, and what the intended stack is. Use the project's declared commands, never your generic equivalents. Run the declared test (or build) command once now, before any edit: a red baseline is a finding to report, not a bug you introduced.

3. **Shape of the tree.** One `ls`-depth pass over the source root. Learn the layering (types, business logic, UI, IO) and spot generated or vendored directories you must not hand-edit. New code goes where the existing analog lives.

4. **The relevant flow, end to end.** Trace one representative request or action from entry point to effect (route → handler → service → store; CLI arg → command → output). Read the actual files on that path: this is the single highest-value read. Note error-handling style, naming, import conventions, and where the nearest test for that path lives.

5. **Recent history.** `git log --oneline -20`, plus `git log --oneline -5 -- <file>` for each file you will edit. Look for in-flight migrations: a commit titled "migrate X to Y" means new code uses Y, even if most of the repo still uses X.

6. **Find the precedent.** For "add a Z" tasks, find the most recently added Z and read all of its wiring (`git log --diff-filter=A --oneline -- <dir>` finds it). Imitate it exactly; deviate only deliberately and say why.

## Write the map before the first edit

Before editing, put 3–6 lines in your notes or first status message: test/build command; the files on the traced path; the precedent you are imitating; any in-flight migration or instruction that constrains the change; the baseline test result. If you cannot fill a line, you have not oriented on it yet.

## Judging which pattern to copy

When two patterns compete for the same job, prefer: (1) the one in newer code, (2) the one the instructions endorse, (3) the one nearest your change. If it is genuinely ambiguous and load-bearing, ask one question citing both patterns.

## Cheap map, not deep study

Breadth-first and time-boxed. Read signatures and shapes, not every body; depth comes later on the specific path you change. If the repo is huge, delegate the sweep to search subagents and keep only the conclusions.

## Signs you skipped this step (go back)

- You are about to add a dependency the repo already has an equivalent for.
- Your new file's imports look different from every neighbor's.
- You invented a directory.
- You wrote a helper that grep would have found already exists.
- You edited a file that a build step regenerates.
