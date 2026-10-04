---
name: solar-workspace
description: >
  Solar workspace content health: doctors for sun/ and planets/ layout, plans, and optional git.
  Use when validating MEMORY, profile, planet structure, or plan folder conventions.
---

# Solar Workspace

## Purpose

Validate **workspace content** under `SOLAR_WORKSPACE`:

- `sun/` (profile, MEMORY, plans layout),
- `planets/*` (AGENTS.md, skills layout),
- optional git checks.

Does **not** cover manifest, bundle, or IDE sync — use **`solar-client`** (`solar client doctor`).

## Required MCP

None

## Validation commands

```bash
python3 core/skills/solar-skill-creator/scripts/package_skill.py core/skills/solar-workspace /tmp
bash -n core/skills/solar-workspace/scripts/workspace_doctor.sh
```

## CLI

```bash
solar workspace doctor [--strict] [--check-git] [--check-plans] [--no-summary]
```

## Frontera

| Skill | Rol |
|-------|-----|
| **solar-workspace** | `sun/` + `planets/` doctors |
| **solar-client** | Manifest, bundle, sync, client doctor |
| **solar-app** | Local console for status, activity and logs (`solar status`, `:9000/app`) |

## Future

- `solar workspace create-planet` (scaffold) — planned; use `core/skills/solar-workspace/scripts/create-planet.sh` until wired.
