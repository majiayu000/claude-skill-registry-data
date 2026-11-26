---
name: project-retrofit
description: Move an existing project's big CLAUDE.md, notes or TODO into the standard doc set without losing any text. Use for "retrofit this project", "split up this CLAUDE.md" or "migrate our notes to the standard docs".
---

# project-retrofit

You decide where each block of text goes. `retrofit.py` moves it verbatim and
proves nothing was lost. **Never retype, summarise or reword source text**, and
never hand-edit a destination to fix a coverage failure.

Script: `project-factory/scripts/retrofit.py` (beside `skills/`; resolve symlinks
with `cd -P`). Run it from the target repo root. Exit codes: 0 ok, 1 coverage
failure, 2 plan error or refusal (nothing written).

## Steps

1. `python3 <retrofit.py> survey .` (read-only). Ask the operator ONE short batch:
   which sources to migrate (default: CLAUDE.md and agent notes; README and TODO
   stay unless chosen), which optional docs to scaffold, anything off-limits.
   Stop and wait for the reply.
2. Scaffold what is missing: `bash <project-factory>/scripts/cut-project.sh --generic [--with a,b] .`
   (existing files are skipped, never overwritten).
3. `python3 <retrofit.py> blocks <source>`; read the source with line numbers.
   Write the plan to a working file outside every destination, e.g.
   `.retrofit/plan.md` (tell the operator it is a working file). Its header is the
   `## source: ... sha256:...` line `blocks` printed, pasted unchanged. Mapping
   guide and syntax: sections/. Every block is accounted for once. Ambiguous means
   `unsorted`. Never guess, never drop.
4. `apply <plan>` (dry run; validates everything) and show the operator a SUMMARY
   TABLE: destination, block count, bytes, previews, any WARNING. Wait for
   approval. Never apply before approval.
5. Ask the operator to commit or stash first, so `git restore <destinations>` (plus
   deleting a new UNSORTED.md or newly scaffolded files) is the undo: apply has no
   revert command. Then `apply <plan> --yes` and `check <plan> --report`. If check
   fails: stop, show the MISSING lines, restore via git, fix the plan, re-run.
6. Write a SLIM replacement entry doc (under 60 lines; `finalize` refuses more,
   `--max-lines N` overrides, 0 = none). Shape: 
   `project-factory/templates/_core/CLAUDE.md` (cut-project skips an existing
   CLAUDE.md). Include only pointers, the `keep` text (`retrofit.py keep <plan>`
   prints it) and facts in the archived original; nothing mechanical checks the
   rest, so invent nothing. Show the FULL replacement to the operator; run
   `finalize <plan> --replace-with <file>` dry, then `--yes` after approval. Never
   pass `--allow-dirty` without the operator's explicit yes; ask them to commit
   the source instead. It archives the original to `docs/archive/` and prints
   the undo (`mv`).
7. `git add` the new docs first (map.py lists tracked files only, so an untracked
   tree gives a false pass), then `python3 scripts/map.py` and `python3 scripts/map.py --check`. Report: coverage
   numbers, UNSORTED.md block count, `<fill:` markers left, files changed. Commit
   only if the operator asks.

## Sections

- sections/mapping-guide.md: read when writing the plan in step 3.
- sections/plan-format.md: read when the script rejects a plan or you need the exact syntax.
