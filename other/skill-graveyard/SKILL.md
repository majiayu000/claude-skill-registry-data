---
name: skill-graveyard
description: Audit which Claude Code skills you actually invoke. Use when the user wants to find dead/unused skills, hallucinated skill invocations, per-project skill stats, or token cost of installed skill metadata. Triggers on "what skills don't I use?", "clean up my skills", "why didn't this skill work?", "audit skills". Runs locally; reads ~/.claude session JSONL logs. No network calls.
license: MIT
metadata:
  author: sfrangulov
  version: "1.0.0"
---

# skill-graveyard

CLI that audits Claude Code skill usage. Two signals from one parser:

1. **Dead installs** — installed but never invoked → safe to remove.
2. **Hallucinated invocations** — invoked but not installed → typos, external-framework registrations, or model tool/skill confusion.

## How to invoke

Run via `npx skill-graveyard@latest <subcommand> [flags]` — no install needed.

## Subcommands

- `audit` (default) — classify into active / dead / missing / hallucinated. Flags: `--days N`, `--only <bucket>`, `--json`, `--claude-dir <path>`.
- `prune` — print removal commands for dead skills. `--apply` to execute (user/agents only; plugin removals always print only).
- `suggest` — triage hallucinated/missing into actionable buckets.
- `projects` — per-project usage breakdown (cwd from sessions).
- `cost` — token cost estimate of installed metadata vs invocations.
- `outdated` — check installed plugins / git skills for upstream updates (network).

## Decision flow

- "are there skills I don't use?" → `npx skill-graveyard@latest`
- "clean up unused skills" → `prune`, then `prune --apply`
- "skill X didn't work" → `suggest` (look for hallucinated/missing entry)
- per-project view → `projects`
- token cost → `cost`
- check updates → `outdated`

After running, print binary output as-is. Do not summarize unless the user asks.
