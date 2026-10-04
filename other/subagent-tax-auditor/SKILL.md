---
name: subagent-tax-auditor
description: "Use when the user asks why their Claude Code quota or usage limit runs out so fast, which subagents cost the most, or wants their subagents made cheaper (for example 'audit my subagents', 'which agent is eating my quota', 'make my agents cheaper')."
---

# Subagent Tax Auditor

## Overview

Every subagent starts with a large fixed context (system prompt, tool definitions, CLAUDE.md) that is sent again on each of its requests, so many small subagents can cost far more than the work they produce. This skill measures that from the local transcripts, explains which agent types are expensive, proposes a cheaper model for custom agents, and later checks whether the change helped. It runs only when the user asks. It never edits anything before the user has seen the diff and said yes, and it never invents a number: scripts do all the arithmetic.

## The scripts

`scripts/audit.py` and `scripts/agent_edit.py` in this skill's directory (use the base directory shown when the skill loads). Python 3 and the standard library only; use `python3`, or `python` / `py -3` if that is what works. `rates.json` beside `scripts/` holds the prices.

- `audit.py report [--project PATH | --all] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--json] [--show-descriptions]` splits usage between the main thread and each subagent type, by model. Read-only. The default project is the current directory.
- `audit.py snapshot --out FILE [same selectors]` saves the per-type numbers so a later comparison has a baseline.
- `audit.py compare --snapshot FILE [--json]` shows per-spawn usage before and after the snapshot, per agent type.
- `agent_edit.py list` shows custom agents (project `.claude/agents/` and `~/.claude/agents/`) with their model and effort.
- `agent_edit.py plan --agent NAME --model MODEL [--effort LEVEL]` prints a diff and changes nothing. `apply` (same arguments, plus `--backup-dir`) writes it and saves a backup. `undo --agent NAME` restores the last backup.

## Process

1. **Measure.** Run `audit.py report --json` for the current project, and offer `--all`. If it says no transcripts were found, or there are no subagent rows, say so and stop. Read the "data quality" footer before concluding anything: skipped lines, subagents without a meta file, and models with no rate change what the numbers mean.
2. **Explain.** Lead with the biggest cost and its share of output tokens. Show the per-type table, the fixed context per spawn, and the footer. Say once that the dollar figure is a proxy at published API rates, not the subscription quota. Never quote or paraphrase what the agents were doing; task descriptions are shown only if the user asks (`--show-descriptions`).
3. **Recommend,** using only these rules, and cite the numbers each one used:
   - A type with a large fixed context per spawn and a small output share: a cheaper model for that type.
   - Many spawns of one type: spawn fewer or batch the work, because each spawn pays the fixed context again.
   - A type whose output share is about its cost share: say it looks fine and leave it alone.
   - A built-in type (`general-purpose`, `Explore`, `Plan`, and so on): report only. It has no file. Tell the user to set `model` where the agent is spawned (in the prompt or in the skill that spawns it).
   - Fewer than 5 spawns: no recommendation.
4. **Propose edits, custom agents only.** Run `agent_edit.py list`. For a custom agent you want to change, run `agent_edit.py plan`, show the diff, and wait for an explicit yes in this conversation. If the file is refused (no frontmatter, duplicate key, multi-line value), say why and leave it. Before proposing any `--effort` change, check the current Claude Code docs that agent frontmatter supports `effort` and which levels it accepts; if it does not, propose `model` only and say so.
5. **Apply.** Run `audit.py snapshot --out <file>` first so there is a baseline (keep it in the project's `.claude/` or a scratch folder, not in the repo), then `agent_edit.py apply`. Show the backup path and give the `To undo:` line that `apply` printed, exactly as printed (it carries the full script path and `--backup-dir`; `undo` takes no `--agents-dir`).
6. **Re-measure later.** When the user comes back, run `audit.py compare --snapshot <file>` and report before and after per spawn with the sample sizes. When it says "not enough data", "model unchanged" or "no spawns since the snapshot", say exactly that. Transcripts do not record effort, so an effort-only edit cannot be judged by `compare`: say that instead of claiming it made no difference. Never claim a saving the comparison does not show; different tasks run in different periods, so even a clear difference is a trend, not proof.

## Rules

- Do arithmetic only through the scripts. Never estimate costs yourself.
- Never edit a file the user did not approve in this conversation. Never use `apply` without showing `plan` first.
- Never print or paraphrase prompt, response or file content from transcripts.
- If the report and the user's expectation disagree, show the data-quality footer before drawing conclusions.
- The tool does not stop Claude Code from spawning agents and does not measure the subscription quota itself.
