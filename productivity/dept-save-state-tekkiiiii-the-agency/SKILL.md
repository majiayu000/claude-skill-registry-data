---
name: dept-save-state
description: Write dept-state.md and member-roster.md at end of department session. Department-operations parallel of /save-state.
category: dept-ops
version: 1.0.0
---

# dept-save-state

Persists department state at end of session. Writes `dept-state.md` and `member-roster.md`. Called by Dept Heads before stopping.

## Usage

```
/dept-save-state [dept-slug]
/dept-save-state content-creation
/dept-save-state all
```

## What It Writes

### dept-state.md
Path: `~/.agency/agents/{dept}/state/dept-state.md`

Key:value format, max 20 lines:
```
dept: {dept-name}
head: {head-agent-name}
last-updated: {YYYY-MM-DD HH:MM}
active-coords: [DC names] | none
active-pipelines: [pipeline names] | none
open-issues: [issue slugs] | none
blocked-on: [description or "none"]
current-priority: {top D1 initiative or "none"}
incoming-count: {n} | 0
notes: {freeform, max 2 lines}
```

### member-roster.md
Path: `~/.agency/agents/{dept}/state/member-roster.md`

Per-member status:
```
| Member | Role | Status | Current Project | Utilization |
|---|---|---|---|---|
| {name} | {role} | available | none | 0% |
```

### Session Log
Appends to: `~/.agency/agents/{dept}/memory/sessions/YYYY-MM-DD.md`

### Decisions
Appends any new decisions to: `~/.agency/agents/{dept}/memory/decisions.md`

## Steps

1. Read current `dept-state.md` (if exists) as baseline
2. Collect from Dept Head session:
   - Active DC names and D3 track states
   - Active pipelines
   - Open issues and blockers
   - Current priority
   - Any new decisions made this session
3. Write updated `dept-state.md`
4. Write updated `member-roster.md`
5. Append session log entry
6. Append any new decisions to `decisions.md`
7. Output confirmation

## Output

```
dept-save-state done — {dept}
  Coords: {n active or "none"}
  Open issues: {n or "none"}
  Next priority: {current-priority}
  State written: ~/.agency/agents/{dept}/state/dept-state.md
```

## Notes

- Never rewrite history — append to session logs and decisions only
- If `active-coords` field lists any DCs, the Dept Head must confirm their last-known state before saving
- Incoming tasks that are still pending: keep `incoming-count` accurate so the next session boots with the right picture

## References

- dept-state.md format: `core/runbooks/dept-boot-sequence.md`
- Parallel: `/save-state` for project state, `/dept-resume` to reload
