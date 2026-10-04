---
name: dept-status
description: Read-only department status digest. No spawns. Shows active coords, pipelines, open issues, and incoming tasks.
category: dept-ops
version: 1.0.0
---

# dept-status

Read-only status check for a department. Reads `dept-state.md` and optionally `active-coords.md`. No agents spawned, no files written.

## Usage

```
/dept-status [dept-slug]
/dept-status content-creation
/dept-status all
```

## What It Reads

1. `~/.agency/agents/{dept}/state/dept-state.md` — primary snapshot
2. `~/.agency/agents/{dept}/state/active-coords.md` — if `active-coords` field is non-empty
3. `~/.agency/agents/{dept}/state/incoming/` — file count only (no content)

## Output Format

```
DEPT STATUS — {dept}
Head: {head-agent-name}
Last updated: {YYYY-MM-DD HH:MM}

Priority: {current-priority}
Active coords: {n — DC names or "none"}
Active pipelines: {pipeline names or "none"}
Open issues: {issue slugs or "none"}
Blocked on: {description or "none"}
Incoming tasks: {n pending or "none"}

Notes: {notes field from dept-state}
```

If `active-coords.md` exists and was read:
```
Coord detail:
  DC-{name} | {D3 track} | {State} | since {HH:MM}
  ...
```

## Multi-Dept (all)

When called with `all`, reads all departments listed in `ORG.md` and outputs a summary table:

```
DEPT STATUS — ALL
| Dept | Priority | Coords | Issues | Incoming |
|---|---|---|---|---|
| content-creation | ... | 2 | 0 | 1 |
| engineering | ... | 0 | 1 | 0 |
...
```

## Notes

- This skill never spawns agents — it's a read-only diagnostic tool
- Use `/dept-resume` to start a dept head session
- Use `/dept-save-state` to persist state at session end

## References

- dept-state.md format: `core/runbooks/dept-boot-sequence.md`
- Parallel: `/pd-status` for project status, `/swarm` for full portfolio check
