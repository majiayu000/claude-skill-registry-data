---
name: save-state
description: >
  Freezes the current session — writes all session-end files, resets the turn
  counter, outputs a single confirmation. Fully autonomous, no user interaction.
  Invoke as /save-state [slug], /save-state (auto-detects from cwd), or
  /save-state all. When to trigger: at the end of every working session before
  closing; before switching to a different project; when mid-flight work needs
  to be preserved for the next session; after any significant milestone or
  decision; and whenever the user says "save state." Key capabilities: INLINE
  mode (default) — the caller synthesizes a small payload from what it already
  knows and one script does every mechanical write, zero subagent spawn;
  SUBAGENT mode (/save-state all, or abrupt-shutdown recovery) — spawns a
  save-state-runner per project to full-scan state the caller never saw.
---

# save-state

Two modes. INLINE is the default and costs ~2k tokens. SUBAGENT exists only
for the cases where the caller has no session knowledge to synthesize from.

## SSOT

Project registry: `~/.claude/memory/medium-term.md` — Active Projects table.
Resolve `[slug]` → project path there. No slug argument → match cwd against
the table. Slug not found → output `PROJECT NOT FOUND: {slug}` and stop.

## Mode selection

| Situation | Mode |
|---|---|
| Live session saving its own project (PD at session end, parent after work) | **INLINE** |
| `/save-state all` | **SUBAGENT** per project (abrupt-shutdown recovery — caller has no knowledge of those sessions) |
| Caller did NOT do the session work (fresh session saving a dead one) | **SUBAGENT** |

## INLINE mode (default)

You already know what happened this session. Do NOT spawn anything and do NOT
re-read project memory — synthesize the payload from your own context (PDs:
your Session Delta from Step 9.5 is exactly this content).

1. Build the payload JSON:

```json
{
  "slug": "{slug}",
  "phase": "current phase or status",
  "next": "specific next action — one sentence, concrete target (file, task ID, action, URL, or agent). Vague entries like 'continue work' are INVALID.",
  "blockers": ["..."],
  "decisions": ["new decisions locked this session"],
  "top_decisions": ["top 1-2 locked decisions that affect the Next action"],
  "mid_flight": ["path — one-line description"],
  "delegated": ["pending inter-spawn task — status"],
  "was_doing": "one line",
  "just_finished": "one line",
  "session_notes": ["notable events this session"],
  "interspawn_active": ["active inter-spawn tasks for index.md Active Summary"]
}
```

2. Run:

```bash
echo '{payload}' | python3 ~/.claude/scripts/save-state.py --project {project-path} --payload -
```

The script does ALL mechanical work: session log, heartbeat, next-session.md
(incl. pending-inbound sweep), decisions append + auto-prune, next-action stub
materialization (Step 3c), inter-spawn index, STATE.md, save-state-state.json
reset, overseer brief, metric emits, graphify update + unified-graph session
node, Pinecone upsert. All fire-and-forget parts are backgrounded by the
script itself — no caller-side follow-up steps.

3. Relay the script's `save-state done!` line. Stop. No further narration.

## SUBAGENT mode (`all` / recovery only)

For each target project (for `all`: every project in the Active Projects
table; sequential, NOT parallel — these are cheap reads but spawns are not):

Spawn ONE `save-state-runner` (sonnet, background OK) with this prompt:

```
SKILL SPAWN: save-state. You own the save-state ritual for one project.
Project: {project-path}   Slug: {slug}
Read ~/.claude/skills/save-state/full-scan.md and follow it exactly.
```

The runner full-scans the project (delta check → baseline reads → mid-flight
scan), synthesizes the same payload, and calls the same script. It reports
`save-state done!` per project. Relay a one-line summary per project.

## Invariants (do not break — consumers depend on these)

- `next-session.md` is the ONLY file pd-resume/recall read at startup — the
  script keeps it ≤15 lines, self-contained, `Pending inbound` always present.
- decisions.md is newest-at-top; prune keeps top 60 lines when >200.
- Overseer brief goes to
  `~/projects/overseer/memory/inter-spawn-tasks/incoming/` (skipped
  when saving overseer itself).
- Metric events `save_state` / `save_state_complete` are emitted by the script.
