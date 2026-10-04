---
name: skill-deployer
description: "Deploy a validated user or workspace skill to user_skills/ or .libragent/skills/. Use after skill-creator validation. NOT for system_skills or app-bundled skills. Triggers: deploy skill, install skill, global skill, workspace skill, user_skills."
---

# Skill Deployer

Install a **validated custom skill** into `user_skills/` (global) or `.libragent/skills/` (workspace) so agents load it on the next turn.

> **Prerequisite**: Run `skill-creator` validation first:
> `python <skill-creator-base-dir>/scripts/validate_skill.py <skill-folder> --strict`

This skill covers **where** and **how** to install user/workspace skills. It does **not** cover authoring — use **skill-creator**. It does **not** ship skills with the app — that is a developer/repo workflow (see Bundled scope below).

## What This Skill Is NOT

| User intent | Correct skill | Target path |
| --- | --- | --- |
| Install my custom skill globally | **skill-deployer** (this skill) | `{dataDir}/user_skills/{name}/` |
| Install for this session/project | **skill-deployer** (this skill) | `{workspace}/.libragent/skills/{name}/` |
| Ship skill inside the LibrAgent app | **Developer workflow** (not this skill) | `src-tauri/bundled_skills/{name}/` → synced to `system_skills/` on build |

**Never deploy custom skills to `{dataDir}/system_skills/`.** That folder is a **managed mirror** of packaged bundled skills. Manual additions are **deleted on app startup**. Do not create or edit `.bundled_manifest.json` outside bundled sync — it does not register custom skills.

If the user says "system skill" or points at `system_skills`, they usually mean **global availability**. Deploy to **`user_skills/`**, not `system_skills/`.

## Scope Decision

| Scope | When to use | Override priority |
| --- | --- | --- |
| **workspace** | Skill is specific to the current project or session | Highest |
| **assistant** | Skill is for one assistant only | Middle |
| **global** | Skill should be available in every session | Lowest |

Default to **workspace** when unsure — safest and easiest to remove.

## Target Paths

### Workspace scope (most common)

```text
{workspace-root}/.libragent/skills/{skill-name}/SKILL.md
```

Read `Workspace Root` from the system prompt (`## Workspace` section).

Example: `C:/Users/alice/AppData/Roaming/com.fritzprix.libragent/workspaces/<session-id>/.libragent/skills/my-skill/SKILL.md`

> **NOT** `{workspace-root}/{skill-name}/` — skills at the session root are never scanned.

### Global scope (user skills)

```text
{dataDir}/user_skills/{skill-name}/SKILL.md
```

Resolve `{dataDir}` from `<available_skills>`:

1. Find a skill with `source="global"` whose `<location>` contains **`user_skills`** (not `system_skills`).
2. Take the parent of `user_skills/` as `{dataDir}`.
3. If none exist, use OS defaults:

| OS | `{dataDir}` |
| --- | --- |
| Windows | `%APPDATA%\com.fritzprix.libragent\` |
| macOS | `~/Library/Application Support/com.fritzprix.libragent/` |
| Linux | `~/.local/share/com.fritzprix.libragent/` |

Example: `C:\Users\alice\AppData\Roaming\com.fritzprix.libragent\user_skills\my-skill\SKILL.md`

> **NOT** `{dataDir}/system_skills/` (bundled mirror), `{dataDir}/skills/` (legacy), or `%APPDATA%\LibrAgent\skills\` (old app ID path).

### Assistant scope

```text
{dataDir}/assistants/{assistant-id}/skills/{skill-name}/SKILL.md
```

The user must provide the assistant ID from the Assistants settings panel.

### Agent import scope (IDE / local dev)

Auto-discovered under the workspace root:

- `.agents/skills/`, `.cursor/skills/`, `.gemini/skills/`, `.copilot/skills/`
- `.windsurf/skills/`, `.claude/skills/`, `.cline/skills/`, `.continue/skills/`

```text
{workspace-root}/.cursor/skills/{skill-name}/SKILL.md
```

### Bundled scope — do NOT use this skill

Repo path only; managed by app build mirror and startup sync (not user-deployable):

```text
src-tauri/bundled_skills/{skill-name}/
```

Runtime mirror (read-only for agents; never write custom skills here):

```text
{dataDir}/system_skills/{skill-name}/
```

## Forbidden Locations

| Path | Why |
| --- | --- |
| `{dataDir}/system_skills/` | Managed bundled mirror — extras deleted on startup |
| `{dataDir}/system_skills/.bundled_manifest.json` | Bundled sync only — does not register custom skills |
| `{workspace-root}/{skill-name}/` | Scanner only reads `.libragent/skills/` |
| `{workspace-root}/.bundled_manifest.json` | Manifest ignored here — does not register skills |
| Legacy `{dataDir}/skills/` | Use `user_skills/` instead |
| Legacy `%APPDATA%\LibrAgent\skills\` | Wrong app data dir — use `com.fritzprix.libragent\user_skills\` |

## Deployment Procedure

Prefer **`deploy_skill.py`** over manual file writes. It always runs **strict validation** before and after copy, blocks forbidden targets, rolls back on post-deploy failure, and prints **error codes with fix instructions**.

```bash
python <skill-deployer-base-dir>/scripts/deploy_skill.py <skill-source-dir> --scope global
python <skill-deployer-base-dir>/scripts/deploy_skill.py <skill-source-dir> --scope workspace --workspace "<workspace-root>"
python <skill-deployer-base-dir>/scripts/deploy_skill.py <skill-source-dir> --scope assistant --assistant-id "<id>"
```

| Flag | Purpose |
| --- | --- |
| `--overwrite` | Replace existing target directory |
| `--dry-run` | Strict validate source + print target without copying |
| `--data-dir` | Override default `com.fritzprix.libragent` data directory |

**Validation phases (all strict):**

1. Pre-deploy (source) — frontmatter, folder name match, forbidden files, bad source path
2. Post-deploy (target) — same checks on the copied skill; **rollback** if this fails

Inspect failures manually:

```bash
python <skill-creator-base-dir>/scripts/validate_skill.py <skill-folder> --strict --detailed
```

Each issue prints `[CODE]`, message, and `Fix:` line (e.g. `SKILL-YAML-APOSTROPHE`, `SKILL-PATH-WORKSPACE-ROOT`).

### Manual fallback (only if the script cannot run)

### Step 1 — Validate (skill-creator)

```bash
python <skill-creator-base-dir>/scripts/validate_skill.py <skill-folder> --strict
```

Do not deploy if validation fails. Fix path/YAML issues before writing files.

### Step 2 — Pick scope and target path

Use the scope table above. Construct the full directory:

```text
{target-dir}/{skill-name}/SKILL.md
{target-dir}/{skill-name}/scripts/...
{target-dir}/{skill-name}/references/...
```

**Checklist before writing:**

- [ ] Target is `user_skills/` or `.libragent/skills/` (or assistant/agent import path)
- [ ] Target is **not** `system_skills/`
- [ ] Folder name matches frontmatter `name:`

### Step 3 — Write files

Use workspace tools (`createFile`, etc.) with forward slashes even on Windows.

Copy the entire skill directory tree — not just SKILL.md — when scripts or references exist.

### Step 4 — Verify discovery

On the **next agent turn**, check `<available_skills>` in the system prompt:

```xml
<skill source="global">
  <name>my-new-skill</name>
  <description>...</description>
  <location>.../user_skills/my-new-skill/SKILL.md</location>
</skill>
```

Confirm:

1. Skill name appears
2. `source` matches intended scope (`workspace`, `assistant`, or `global`)
3. `<location>` matches the path you wrote (`user_skills` for global, not `system_skills`)

Re-run `validate_skill.py --strict` on the deployed copy if discovery fails.

### Step 5 — Report

Tell the user:

- Full path written
- Scope chosen
- Skill name as it appears in `<available_skills>`
- That it becomes active on the next agent message

## Coalesce Behavior

Skills merge with **first-wins by lowercase name**. Priority: workspace > assistant > agent import > global > system.

A workspace skill silently overrides a global skill with the same name.

## Common Mistakes

- **Deploying to `system_skills/`** — use `user_skills/` for global custom skills; ship app-bundled skills via `src-tauri/bundled_skills/` in the repo
- **Confusing `system_skills` with global** — global user skills live in `user_skills/`
- **Creating `.bundled_manifest.json`** — only bundled sync uses this; it does not register custom skills elsewhere
- **Hash-checking against bundled manifest** — irrelevant for custom skills; discovery uses directory scan + valid SKILL.md
- **Skipping validation** — invalid YAML is silently ignored by the Rust scanner
- **Workspace root deploy** — must be `.libragent/skills/{name}/`, not `{workspace}/{name}/`
- **Wrong global path** — use `com.fritzprix.libragent\user_skills\`, not legacy `LibrAgent\skills\`
- **Apostrophe in YAML** — fix in skill-creator (`"it's"` not `'it\'s'`)
- **Name ≠ folder name** — breaks `@skill:name` lookup
- **Expecting immediate UI refresh** — skills reload at the start of the next agent turn
