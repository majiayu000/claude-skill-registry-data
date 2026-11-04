---
name: pickup
description: Continue a handoff under .tmp/grunt/handoffs/.
---
# pickup

Voice: `.rulesync/reference/output.md`.

Load a handoff and continue in this session. Not a mode. Not `/handoff`. Inverse of `/handoff`.

## Invocation

- `/pickup`
- `/pickup latest` (also `newest`/`last`)
- `/pickup {serial}`
- `/pickup {abs|rel|drag-drop path}`
- `/pickup {title substring}`

## Resolve

Read `.tmp/grunt/handoffs/`. Use `node .rulesync/scripts/grunt-job.mjs --job search|exec` when the listing is fat.

Order:

1. path-like → file if exists + FILENAME_RE `^[0-9]+-[a-z0-9]+(-[a-z0-9]+)*-\d{8}T\d{6}Z\.md$`
2. integer → FM serial or filename prefix
3. latest|newest|last → newest by FM `created`
4. else case-insensitive substring on name/source/H1
5. empty arg: 0→none; 1→auto; N→list+ask (**not** auto-newest)

List lines: serial status name created path. Prefer open|resumed first; still include done.

Matches: 0→recap missing; 1→proceed; N→list+ask never guess.

Empty/missing dir: recap no handoffs; stop.

Drag outside handoffs dir or non-FILENAME_RE: reject; list valid.

Corrupt FM: recap; do not continue on garbage.

status done + explicit serial/path: warn; still load if the user named it.

## After unique path

Read the file. Set `status: resumed`. Work Next leaves in order; flip only that box; all `[x]` → `status: done`; do not re-plan; stale → `/write-plan`. Edit in place. Never persist-handoff.mjs on pickup.

## Recap

```
serial={int} path={abs}
```

Do not invent a new role tag.

## Rules

- `/handoff` stays one-turn write. This skill owns pickup.
- Protocol: `.rulesync/reference/cascade.md`. Do not paste.
