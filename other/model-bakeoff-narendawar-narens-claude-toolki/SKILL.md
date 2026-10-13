---
name: model-bakeoff
description: "Use when the user wants to pick the cheapest model that still works for a custom subagent, asks whether Haiku or Sonnet would do, or wants to re-check an agent's model after new models ship (for example 'which model should this agent use?', 'could this run on Haiku?', 'bake-off my reviewer agent')."
---

# Model Bake-off

## Overview

A custom subagent runs on whatever its `model` field says, usually chosen by feel. This skill measures instead: it runs the agent's test cases on Haiku, Sonnet and Opus through `claude -p`, applies a stated pass rule, recommends the cheapest model that passes, and only after the user says yes writes it into the agent's `model` field. It runs only when the user asks. It never invents a number: the script does all the arithmetic, and it states what the runs do and do not show.

## The script

`scripts/bakeoff.py` in this skill's directory (use the base directory shown when the skill loads). Python 3 and the standard library only; use `python3`, or `python` / `py -3` if that is what works.

- `agents [--json]` lists custom agents with their model, tools and whether they are read-only.
- `check-cases --cases FILE` validates a cases file.
- `estimate --agent NAME --cases FILE [--models LIST] [--runs N]` shows the number of runs, the ceiling cost, and whether an opt-in is needed. It calls nothing.
- `run --agent NAME --cases FILE [--allow-writes] [--yes] [--keep-outputs] [--out FILE]` runs the bake-off and saves a results file (default `.claude/bakeoff/<agent>.results.json`).
- `decide --results FILE [--json]` applies the pass rule and prints the table and recommendation.
- `resolve [--results FILE] [--models LIST] [--cases FILE]` finds which model IDs the aliases point to today and what changed since a results file.
- `plan | apply | undo --agent NAME --model MODEL ...` is the guarded edit of the agent's `model` field (the same tool as `agent_edit.py` in this folder; `undo` takes `--agent` and `--backup-dir` only).

## The cases file

`.claude/bakeoff/<agent>.cases.json`: a list of cases, each with a `prompt`, an optional `fixture` folder, at least one deterministic entry in `checks` (`contains`, `not_contains`, `regex`, `json`, `command`), and an optional `rubric` judged by a model (it can only make a case stricter). Run `check-cases` after writing it.

## Process

1. **Pick the agent.** Run `agents`. Only custom agents (a file in `.claude/agents/` or `~/.claude/agents/`) can be tested and edited. For a built-in agent type, say it has no file and stop. Skills are not supported yet.
2. **Get the cases.** If there is no cases file, draft one from the agent's description: 3 to 6 realistic prompts, each with checks a script can evaluate (text that must or must not appear, a regex, JSON keys, or a command that must exit 0). Prefer small fixtures. Show the file to the user and wait for them to say it looks right. Never run anything before the user has seen the cases. Run `check-cases`.
3. **Estimate and ask.** Run `estimate` and show the number of runs, the ceiling cost, and the opt-in lines. Say that the runs use the user's own `claude` usage. If the agent can write or run commands, or a case runs a command, tell the user exactly which tools and commands will really run (in a scratch copy of the fixture, which limits mistakes but is not a sandbox), and get an explicit yes before using `--allow-writes`. A read-only agent needs no opt-in. Ask for a yes to run at all.
4. **Run.** Run `run`. If it aborts, show the reason (for example, `claude` not logged in); do not recommend anything from a partial run.
5. **Decide and explain.** Run `decide`. Show the table, the rule, and the recommendation. Say plainly: this is evidence on these cases, not proof; models vary between runs; the cost is measured from `claude -p` output, not the subscription quota. If no model passed, say so and suggest fixing the failing cases or keeping the current model. If the current model is already the cheapest passing one, say so.
6. **Edit only with a yes.** Run `plan --agent NAME --model <resolved model id>` (the pinned full ID by default; use the alias only if the user prefers it, and say the result then expires when the alias moves), show the diff, and wait for an explicit yes. Then run `apply --backup-dir .claude/bakeoff/backups` (same arguments as `plan`) and give the `To undo:` line exactly as printed. If the file is refused (no frontmatter, duplicate key, multi-line value), say why and leave it.
7. **Come back later.** When the user returns (a new model shipped, or they changed the cases), run `resolve --results FILE --cases FILE`. If candidates changed or the cases changed, offer to re-run only what changed (`run --models` with the changed or new ones). When the cases file and the rule are unchanged, the new results are merged into the saved file and the other models' saved results are kept; otherwise `run` starts a fresh file and says so (then re-run every model). A run that aborts never overwrites good results: its partial results go to a separate `.aborted.json` file. Run `decide` again afterwards: it uses every model in the file.

## Rules

- Do arithmetic only through the script. Never estimate costs or pass rates yourself.
- Never run `run` before `estimate` was shown and the user said yes. Never use `--allow-writes` without naming the tools and commands first.
- Never edit an agent file the user did not approve in this conversation. Never use `apply` without showing `plan` first.
- Never print or paraphrase the agents' outputs unless the user chose `--keep-outputs`.
- Never claim a saving the measurements do not show. The first run of each model pays for a cold prompt cache and costs several times more than the rest, so with few runs the cost ranking can be noisy: when the passing models' mean costs are close, say so instead of presenting a clear winner, and offer more runs (`--runs`).
- The rubric judge, `--allow-writes` agents, `command` checks and `resolve` have not been exercised against a real `claude` yet; say so if the user relies on them for the first time, and suggest trying them on something small.
- The tool does not stop Claude Code from using any model and does not measure the subscription quota.
