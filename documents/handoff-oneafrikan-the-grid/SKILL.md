---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
---

## Session handoff file

Write a handoff document summarising the current conversation so a fresh agent can continue the work.

**Template:** load `handoff-template.md` from this skill's base directory and fill it in. Do not invent a different structure.

**Filename:** `YYYY-MM-DD-<machine>-<slug>-handoff.md` where:
- `YYYY-MM-DD` is today's date
- `<machine>` is the output of `hostname -s` (e.g. `my-laptop`, `build-box`)
- `<slug>` is a 2-4 word kebab-case summary of the session topic (e.g. `machine-overlays`, `agent-factory-roster`)
- `-handoff` is appended to make the file self documenting

**Save location:** the project's `LOGS` folder, always (see Document locations below). No other location.

**Rules:**
- Do not duplicate content already captured in commits, diffs, PRDs, plans, or ADRs — reference them by path or URL instead
- If the user passed arguments, treat them as a description of what the next session will focus on and tailor accordingly
- Suggest relevant skills for the next session in the Suggested Skills section

---

## Session context file

Also write a context file using today's actual date.
**Template:** load `context-template.md` from this skill's base directory and fill it in.
**Filename:** `YYYY-MM-DD-<machine>-<slug>-context.md` — same date, machine, and slug as the handoff file, with `-context` appended.
**Must include:** what was investigated and why, every decision and reasoning, field conventions, known bugs, key findings, open questions, immediate next actions.

---

## Document locations reference

Both files go to the `LOGS` folder of the project the session ran in. Nothing else
decides this: no per-project table, no other directory, and not whether the repo is
public or who owns it. Do not ask where.

- **Project:** if the working directory is inside a git repo, the repo root
  (`git rev-parse --show-toplevel`); otherwise the working directory itself.
- **Folder:** `<project>/LOGS`. If a directory named `logs` in any casing (`logs`,
  `Logs`, `LOGS`) already exists there, write there as-is; never create a second one in
  another casing, and do not compare with git's tracked casing or `core.ignorecase`.
- **Missing:** create `LOGS` and write there.
- **Automated runs** (the SessionEnd worker) name the folder in the prompt as
  `Target directory`: use exactly that path; it is already resolved and created.

---

## After writing

Resolve the folder to its real path first (`realpath <dir>`): it may be a symlink into
a **different** git repo (e.g. the-grid's `LOGS/` links to a separate private repo).
The repo that matters is the one containing the resolved path, not necessarily the
project repo.

- **In a git repo:** commit the two files by explicit path only
  (`git add -- <f1> <f2>`, then `git commit -m "docs: handoff <slug>" -- <f1> <f2>`),
  never the session's other changes. Then `git push` the current branch. A plain push
  also publishes any other unpushed commit on that branch. No remote or upstream, or a
  failed push: say so, leave the commit local, and carry on; never fail over it.
- **No git repo:** leave the files in the folder and say so. Do not create a repo.
