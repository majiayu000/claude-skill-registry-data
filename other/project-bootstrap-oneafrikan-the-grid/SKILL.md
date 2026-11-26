---
name: project-bootstrap
description: Scaffold a project and fill its docs from the operator's answers, then optionally add the grid extras (signals, knowledge, agents, hooks). Use for "bootstrap this project" or "set up a new project properly".
---

# project-bootstrap

Scaffold, then fill. `project-scaffold` lays down empty docs; this skill asks the
operator about the project and writes real content into them. The grid layer
(`--grid`) is opt-in; "default yes inside the grid" only means you offer it.

**Hard rule: never invent a fact.** Anything the operator did not give stays a
`<fill: ...>` marker or becomes `<unknown: ask the operator>`. Quote their words.

## Steps

1. Ask ONE numbered batch of questions, answerable in one reply (wording:
   sections/questions.md). If there is a README, notes or a partly answered brief,
   read it first, drop what it already answers and ask only the gaps, still as one
   batch. Never answer a question from your own guess.
   Stop. Do not run the scaffold until the operator replies.
2. Find `project-factory/scripts/cut-project.sh` (beside `skills/`; resolve symlinks
   with `cd -P`). Run it, then report `wrote:` / `SKIPPED` / `unchanged:` and any
   `warning:` or `note:` line verbatim:

   ```bash
   bash <project-factory>/scripts/cut-project.sh --generic [--with a,b | --all-optional] [--grid] <target-dir>
   ```

   `--with` names: design, agents, logs, humans, context, calculations, assumptions, learnings, memory.
   Pick them from the answers (formulas or numbers: calculations, assumptions;
   lessons the operator named: learnings; things to remember each session: memory).
3. Fill every scaffolded file from the answers. Per-file rules: sections/fill-rules.md.
   Never touch a `SKIPPED` file; list it for the operator.
4. Grid extras, only if chosen: sections/grid-extras.md. State every state-changing
   command (deploy.py, deploy_hooks.py, anything writing `.claude/`) first and run it
   only after an explicit yes; an unanswered question never runs them. Run nothing
   that sends data off the machine.
5. `git add` the new docs first (map.py lists tracked files only, so an untracked
   tree gives a false pass), then regenerate the map and verify, from the target directory:

   ```bash
   python3 scripts/map.py
   python3 scripts/map.py --check
   ```

6. Report, in bullets: files filled; files still holding markers or unknowns (list
   each); the next three actions for the operator. Commit only if the operator asks.

## Sections

- sections/questions.md: read when writing the question batch in step 1.
- sections/fill-rules.md: read when filling the files in step 3.
- sections/grid-extras.md: read when the operator chose the grid extras, step 4.
