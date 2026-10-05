---
name: synthesizing-cc-bigpicture
description: Synthesizes a living big-picture meta-plan from Claude Code sessions, plans, tasks, and team communications. Use when orienting across projects, assessing reasoning modes, or creating a plan-to-plan overview.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob
  argument-hint: "[project-name] [time-range] [output-path]"
  context: fork
---

# Big-Picture Synthesis

**Target**: $ARGUMENTS

Synthesizes a **plan to plan** — an overarching view across all Claude Code
artifacts. A reasoning tool that connects sessions, plans, tasks, and memories
into a coherent narrative of what you're working on, why, and where you're headed.

## Arguments

| Position | Name | Required | Default | Description |
|----------|------|----------|---------|-------------|
| 1 | `project-name` | no | all projects | Filter to a single project (substring, case-insensitive). Use `all` for all. |
| 2 | `time-range` | no | all time | E.g. `7d`, `30d`, `this-week`. |
| 3 | `output-path` | no | auto | Where to write output. |

**Default output path:**

- `project-name` set: `<decoded-project-path>/docs/bigpicture.md`
- `all` or omitted: `~/.claude/bigpicture.md`
- Explicit `output-path`: overrides both.

**Project matching**: Matched against decoded `~/.claude/projects/<encoded-path>/`
directories (`-` → `/` in encoding). Substring match on any path segment.

**Examples:**

```text
/synthesizing-cc-bigpicture                          # All → ~/.claude/bigpicture.md
/synthesizing-cc-bigpicture Agents-eval              # Single → project docs/
/synthesizing-cc-bigpicture Agents-eval 7d           # Single, last 7 days
/synthesizing-cc-bigpicture all 30d ./bigpicture.md  # All, 30 days, custom path
```

## When to Use

- Starting a work session — orient across projects
- Planning what to work on next — strategic prioritization
- Sprint/week boundary — maintain the meta-plan
- Feeling stuck — surface current reasoning mode and whether a shift is needed

## Do Not Use

- Searching a specific past conversation (use `/resume` or `/history`)
- Per-session context (session-memory does this automatically)
- Real-time usage monitoring (use `/insights`)

## Project Filtering

When `project-name` is set (not `all`), ALL data collection and output must
respect the filter. Apply these rules once, consistently:

1. **Session allowlist**: From `history.jsonl`, collect `sessionId` values whose
   `project` field matches (case-insensitive).
2. **Project dirs**: Filter `~/.claude/projects/*/` to matching decoded paths.
3. **Plans**: Content-based — include only plans mentioning the project name.
4. **Tasks**: Match task dir names against session allowlist (UUIDs) or filtered
   team names.
5. **Teams**: Include only teams whose `config.json` references the project name.
6. **Session .jsonl**: Only read files whose UUID is in the session allowlist.
7. **Output**: Every section scoped to filtered data only. Exception:
   "Cross-Project Connections" may reference other projects as outbound links.

## Workflow

1. **Parse arguments** — Apply defaults per Arguments table. Resolve output path.

2. **Check existing** — If bigpicture.md exists at output path, load for
   incremental update (preserve structure, refresh content).

3. **Discover & filter projects** — Glob `~/.claude/projects/*/`. Decode paths.
   Apply project filter if set. Build session allowlist from `history.jsonl`.

4. **Progressive retrieval** — Escalate through tiers, stop when every output
   section has concrete evidence. See `references/progressive-retrieval.md`
   for tier definitions, cost estimates, and the escalation rule. Start at
   Tier 1 (metadata-only).

5. **Collect signals** — Following the progressive retrieval tiers, collect
   signals starting from Tier 1. See `references/cc-data-sources.md` for the
   full data source layout. Walk these in order (sequential, metadata-first,
   no subagents):
   - `stats-cache.json`, `history.jsonl`, project memory, plans, tasks, teams
   - Session metadata (first+last 5 lines of each `.jsonl`)
   - Session summaries (skip if directory absent)
   - Subagent transcripts (first+last 5 lines, cap 10 most recent by mtime)
   - Project docs (`CHANGELOG.md`, `AGENT_REQUESTS.md`)

6. **Classify reasoning modes** per work stream — diverge/converge and
   strategic/tactical. See `references/reasoning-modes.md` for axis definitions,
   signals, and alert conditions.

7. **Synthesize** — Group by project → time clusters. Link plans↔sessions↔tasks.
   Surface blockers, trajectory, recurring themes, cross-project connections.

8. **Output** using the template in `references/output-template.md`. Write to
   output path.

## Common Pitfalls

- **Data dump**: If output exceeds ~200 lines, raise abstraction. Interpret, don't list.
- **Reading full transcripts**: Use `history.jsonl` + first/last lines only.
- **False mode classification**: Reasoning modes are heuristic signals, not verdicts.
- **Spawning subagents**: Don't. Sequential within fork context is sufficient.

## Quality Check

- Correct > Complete > Minimal (ACE-FCA)
- ~100-200 lines output
- Every claim traces to a specific CC artifact
- Incremental update preserves structure, refreshes content

## References

- `references/progressive-retrieval.md` — tier escalation rule and cost estimates
- `references/cc-data-sources.md` — full `~/.claude/` directory layout
- `references/cc-entry-types.md` — JSONL session entry type taxonomy
- `references/reasoning-modes.md` — diverge/converge and strategic/tactical axes
- `references/output-template.md` — standard output format
