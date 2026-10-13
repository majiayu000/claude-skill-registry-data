---
name: cclogs
description: "Load recent prototypes, logs, plans, and artifacts from the repo-scoped Dropbox-synced cclogs dir so work started in an earlier session can be continued. Use whenever the user invokes /cclogs, including inline forms like '/cclogs refer the recent prototype and continue — we need an STL enclosure' or 'the top page prototype is in /cclogs, do the next step'. Also use, without being asked, whenever the user refers to a prototype, plan, log, agent report, or generated artifact from a previous session as if it already exists — cclogs is where /big-plan, /x-wt-teams, /x-as-pr, and /protodev put those, and the user should never have to explain what cclogs is."
disable-model-invocation: false
argument-hint: "[name | N | --dirs | repos | (empty = recent entries) ] [+ what to do next]"
allowed-tools: Read, Bash(node *), Bash(ls *), Bash(find *), Bash(stat *), Bash(head *), Bash(grep *), Bash(wc *), Bash(file *)
---

# cclogs — continue work from a previous session

## What cclogs is

The user's agent sessions write logs, plans, prototypes, and artifacts to a **Dropbox-synced directory outside the repo**, so they survive switching between Mac and WSL and never pollute git history.

- **Base:** `$DROPBOX_CCLOGS_DIR` (symlinked at `$HOME/cclogs`). Set in `.zshrc` on both machines.
- **Repo-scoped:** each repo gets `<base>/<repo-name>/`. Worktrees fold onto the main repo, and a trailing number folds off the folder name, so `zzmod` and `zzmod2` share `cclogs/zzmod/`.
- **Not in the repo:** nothing here is committed or gitignored — it simply lives elsewhere. Editing it never dirties the working tree.

Because it is outside the repo, material here is invisible to a fresh session until someone goes looking. That is what this skill is for: the user says "the prototype is in cclogs" and expects the work to continue, not an explanation.

## Resolve the directory

Never hand-build the path — the worktree and numbered-sibling folding above is easy to get wrong:

```bash
LOGDIR=$(node "$HOME/.claude/scripts/get-logdir.js")
```

Outside a git repo this resolves to `<base>/_misc/`. On Claude Code web (`$CLAUDE_CODE_REMOTE=true`) it is an ephemeral `/tmp` stub with no Dropbox behind it — say the material is unreachable there rather than substituting something else.

## Survey what is there

```bash
node "$HOME/.claude/skills/cclogs/scripts/survey.mjs" [options]
```

| Option | Effect |
| --- | --- |
| *(none)* | 12 newest entries in this repo's dir |
| `--dirs` | directories only — prototypes and workflow dirs, which flat log files bury in a log-heavy repo |
| `--find TERM` | name contains TERM (case-insensitive) |
| `--limit N` | show N entries (`0` = all) |
| `--repo NAME` | another repo's dir |
| `--repos` | every repo dir under the base, newest activity first |
| `--dir PATH` | an explicit path |

Each row is `name`, timestamp, age, kind, size/file-count. Directories are ranked by the newest mtime **inside** them, because editing a file deep in a prototype leaves the parent dir's own timestamp untouched — `ls -t` would bury the very thing just worked on.

Reach for `--dirs` when the user says "the prototype": prototypes are directories, and in an active repo hundreds of agent report files sit on top of them by recency.

## Pick and load

Match the user's words to a row. `--find` with a distinctive fragment beats scrolling a long list. When several plausibly match, prefer the newest and say which one was chosen — a one-line "loaded X (2h ago)" lets the user redirect cheaply if it was the wrong one.

Open each kind on its own terms rather than dumping bytes:

- **prototype (web)** — read `index.html` and its CSS/JS. Multi-variant galleries are common, so check whether the dir holds several numbered patterns before assuming one design.
- **prototype (node/vite, script, cad/3d)** — read the entry point and `package.json`; run nothing without being asked.
- **workflow coordination** — `plan.md` is the spec, `progress.md` the ledger, `sub-NN-*.md` the per-topic tasks. Read `plan.md` first; it frames the rest.
- **workflow-runs (subdirs)** — `local-workflow/` holds one timestamped dir per run. List it and pick the run, don't read them all.
- **images** — view them; screenshot dirs are usually visual evidence for a report sitting beside them.
- **report/log, raw log** — `.md` reports are written for a reader and worth reading whole; `.log` files are raw agent output, so grep for the failure or decision rather than reading end to end.

A file reported as `0 B (unsynced?)` is almost certainly an online-only Dropbox placeholder rather than an empty artifact — usually from the other machine. Wait a few seconds and re-check before treating it as empty.

**If the material is not there,** check `__inbox/` in the repo root before concluding it is missing: a prototype that had to import the repo's production code or use its Vite tooling lives there instead (the documented exception in `/protodev`).

## Then do the work

The survey is not the deliverable. The user invoked `/cclogs` to resume something — "continue the work, we need an STL enclosure", "do the next step, I want to change…" — so loading the material is step one of that task, not the answer to it.

Carry the loaded material forward as real context: the earlier session's decisions, naming, and structure are the starting point, and rebuilding from scratch throws away the work the user is pointing at. If what you found genuinely does not match what they described, say so and ask — do not quietly proceed on the wrong artifact.

## Writing new material here

Same directory, via the `{logdir}` placeholder so the path resolves correctly:

```bash
node "$HOME/.claude/scripts/save-file.js" "{logdir}/{timestamp}-<slug>.md" "$CONTENT"
```

New prototypes go in `$LOGDIR/<descriptive-name>/` per `/protodev`. Never write cclogs paths into a GitHub issue — they are machine-local by nature and unreachable from Claude Code web, so an issue that depends on one is a dead end for whoever picks it up.

## Reference

Read [references/layout.md](references/layout.md) to interpret an unfamiliar entry — which skill produced it, what the naming conventions mean, and what is safe to ignore.

## Related skills

- `/db`, `/ss` — the Dropbox resolver and screenshot loader, for material outside cclogs
- `/protodev` — where prototypes come from and why they live here
