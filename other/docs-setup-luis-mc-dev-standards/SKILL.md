---
name: docs-setup
description: Lay out a repository's docs to the documentation standard (DOCSPEC), or move an existing repo to it. Use when the user wants to set up, standardise, restructure or migrate docs, move docs/specs or docs/guides into the new layout, create docs/overview, AGENTS.md or docs/docs.json, or move the artifacts record to docs/project. Dry run by default; moves with git mv, rewrites links, never deletes.
model: sonnet
effort: medium
---

# Docs — setup

Runs `scripts/docs_setup.py` from the `luismc-docs` plugin (DOCSPEC §9). The layout rules are in `references/docspec.md`. Read §2 and §9 first.

```bash
S="${CLAUDE_PLUGIN_ROOT}/scripts/docs_setup.py"
python3 "$S" init --apply --app web --topic library       # new repo: layout, docs.json, overview stubs, AGENTS.md
python3 "$S" migrate                                      # existing repo: print the plan, change nothing
python3 "$S" migrate --map docs/specs/x.md=docs/architecture/x.md   # override a guessed target
python3 "$S" migrate --apply                              # git mv, rewrite links, front matter stubs, layout
python3 "$S" move-record --apply                          # artifacts record to record_dir (docs/project)
```

## Steps for an existing repo

1. Confirm no branch is in flight (run between trains, R9.8).
2. Run `migrate` and read the plan. Lines marked `guess` come from the file name. The owner decides which guesses are wrong, and you pass `--map`.
3. Run `migrate --apply` on its own branch. Exit 2 means a target already existed. The file was kept; decide by hand.
4. Fill `apps` and `topics` in `docs/docs.json`, then run `docs_index.py build` and `docs_check.py`.
5. Report the gaps list (`docs/features/index.md`, Gaps). Content gaps become tasks. This skill does not rewrite docs (R9.5).

`docs/work/` is never moved. If it holds files, say so in the report. Do not commit generated files by hand: `docs_index.py build` writes them.
