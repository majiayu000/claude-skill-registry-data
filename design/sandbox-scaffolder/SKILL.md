---
name: Sandbox Scaffolder
description: Target-profile-driven scaffolding for a multi-scene, multi-option prototype into the active playground defined in ${CLAUDE_PLUGIN_ROOT}/config/prototype-targets.json. Reads the target's real conventions at runtime (folder layout, manifest shape, scene API), checks for collisions/reuse, and creates the orchestrator + scene files + manifest entry. Swappable — point at a newer playground by changing the target profile, not this skill.
version: 1.0.0
author: Mattermost Design Team
tags: [prototype, scaffolding, react, typescript, vite, target-profile, fast-path, defense-ux]
---

# Sandbox Scaffolder

## Purpose

Create the file skeleton for a `/prfaq-prototype` prototype in whatever playground is the **active
target**, without hardcoding that playground. **The command/builder resolves the active target** (project
override → `.claude/prototype-targets.json` → the bundled default, plus any `--target`) and injects the
resolved `target_profile`; this skill consumes **only** that injected profile — it does not read the config
or re-resolve the target. It confirms the profile's real conventions at runtime and scaffolds a
multi-scene, multi-option prototype that matches them. Point the pipeline at a newer playground later by
adding a profile and flipping `active_default` — this skill does not change.

## When to Use

- Stage 2 of `/prfaq-prototype`, after the analyst's scene plan + clarifications are settled, before composition.
- Whenever the prototype-builder needs the file skeleton for the chosen scenes/options.

## When NOT to Use

- To populate screens with real components — that is `sandbox-composer`.
- To decide scenes/options — that is `scene-mapper` + the analyst's clarification round.
- To scaffold into a hardcoded path — always resolve the target profile.

## Input Requirements

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "slug": { "type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$", "example": "attribute-based-action-controls", "description": "kebab-case, a single safe path segment — no slashes, no '..', no absolute paths." },
    "label": { "type": "string", "example": "Attribute-Based Action Controls" },
    "target_profile": { "type": "object", "description": "The resolved target profile object injected by the command/builder (already resolved, incl. --target / project override); do not re-resolve." },
    "options": { "type": "array", "minItems": 1, "items": { "type": "object", "properties": { "id": {"type":"string"}, "label": {"type":"string"}, "philosophy": {"type":"string"} }, "required": ["id", "label"] }, "description": "The design directions (e.g. option-a, option-b)." },
    "scenes": { "type": "array", "minItems": 1, "items": { "type": "object", "properties": { "id": {"type":"string"}, "label": {"type":"string"} }, "required": ["id", "label"] }, "description": "The screens to build (e.g. blocked-view / authoring / registry)." }
  },
  "required": ["target_profile", "slug", "label", "options", "scenes"]
}
```

## System Prompt

You scaffold a prototype into the **active target playground**. Never assume conventions — read them.

**Validate `slug` first (security):** it must match `^[a-z0-9]+(-[a-z0-9]+)*$` (kebab-case, one path segment) — reject any value containing path separators or `..`. After forming the prototype directory, resolve the path and confirm it stays within the target's `prototype_dir` root; abort if it escapes.

**Constrain scene IDs (security):** require every `scenes[].id` (and the active `scene.id`) to match `^[a-z0-9]+(-[a-z0-9]+)*$` (kebab, one segment); resolve each scene file path and confirm it stays under `<prototype_dir>/scenes/` before creating, reading, or writing it — abort on any escape. Apply the same kebab single-segment check to every `options[].id` (it can become a manifest/route path segment in the sibling-entry fallback).

### Step 1 — Use the resolved target profile (passed in — do not re-resolve)

Use the **resolved target profile the builder/command injects** (already resolved via the command's order:
project `prototype-targets.json` → `.claude/prototype-targets.json` → the bundled
`${CLAUDE_PLUGIN_ROOT}/config/prototype-targets.json`, plus any `--target` override). Do NOT re-read or
re-select a target yourself — that could diverge from the command's choice. From the injected profile take:
`workspace_relative_root`, `prototype_dir`, `manifest_file`, `manifest_entry_shape`, `route_pattern`,
`scene_api`, `starter_template`, `example_prototype`, `conventions_docs`. All paths below are relative to
`workspace_relative_root`.

### Step 2 — Confirm conventions at runtime (they drift)

- Read the profile's `conventions_docs` (for proto-playground: `src/pages/prototypes/AGENTS.md`).
- Read the `starter_template` (if the profile has one) and `example_prototype` orchestrators for the
  canonical shape (for proto-playground, `external-call-participants/ExternalCallParticipants.tsx` shows
  the real `usePrototypeChrome` + `SceneSwitcher` pattern).
- Read the `manifest_file` to confirm the current `PrototypeEntry` shape before adding an entry.

### Step 3 — Collision / reuse check (do not overwrite)

- If `prototype_dir` for this `slug` already exists, STOP and report — offer: reuse/extend, pick a new
  slug, or explicit overwrite. Never silently overwrite.
- If an existing prototype clearly overlaps (e.g. a neighboring `external-call-participants` covers a
  scene), surface it so the builder can branch from it rather than duplicate. Reuse beats rebuild.

### Step 4 — Create the skeleton (multi-scene, multi-option)

Follow the profile's `folder_convention`. For proto-playground (kebab-slug), create
`src/pages/prototypes/<slug>/`:

```
<PascalSlug>.tsx        # thin orchestrator: option state + scene state + chrome + switch
<slug>Scenes.ts         # scene ids + labels (feeds SceneSwitcher)
<slug>Data.ts           # shared demo fixtures (composer fills)
<Slug>.module.scss      # shared styles (tokens only)
components/             # prototype-only shared UI (NOT design-system)
scenes/                 # one file per (scene) — options handled via an `option` prop or per-option files
```

**Multi-option mapping (per the profile's `multi_option_convention`):** one slug. The orchestrator holds
BOTH an `option` toggle (the design directions) and a `scene` switch (the screens). Put the option toggle
+ `SceneSwitcher` in the center slot via `setCenterSlot(...)` inside a `useEffect` (cleanup
`setCenterSlot(null)`; re-run on change; never `position:fixed`). If the profile's `scene_api.scene_register_hook` is set (and resolves), call it
with the active scene so reviewer comments scope per screen; if it's `null`, skip it — never phantom-import. Each scene file receives the active `option` (and state) as props
and renders that direction's take. Only split into per-option files when a shared scene file would
mislead. Mirror the exact import paths from the profile's `scene_api` (verify they resolve).

### Step 5 — Register in the manifest

Append a `PrototypeEntry` matching the profile's `manifest_entry_shape` (proto-playground:
`{ id, label, path, component }`), importing the orchestrator; `path = route_pattern` with `<slug>`.
Re-read the interface first; do not hardcode fields if the manifest changed.

### Step 6 — Header labels

Top every generated file with an `// [AI DRAFT]` comment. Leave scene bodies as thin placeholders for
`sandbox-composer` to fill — do not compose components here.

## Output Format

```json
{
  "target": "proto-playground",
  "root": "prototype-playground/proto-playground",
  "files_created": [ { "path": "src/pages/prototypes/<slug>/<PascalSlug>.tsx", "type": "orchestrator" } ],
  "files_modified": [ { "path": "src/manifests/prototypes.ts", "changes": ["import", "PROTOTYPES entry"] } ],
  "route": "/prototypes/<slug>",
  "scenes_scaffolded": [ "..." ],
  "options_scaffolded": [ "..." ],
  "reuse_notes": [ "..." ],
  "collisions": [ ]
}
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `TARGET_UNRESOLVED` | No resolved `target_profile` injected, or it is missing required keys | Stop; report that the command/builder must inject a resolved target profile. |
| `ROOT_MISSING` | `workspace_relative_root` absent on disk | Stop. The command's `playground-bootstrap` pre-flight should have offered the clone; tell the user to re-run so it can, or to point the profile at their playground. |
| `PROTOTYPE_EXISTS` | Slug dir already present | Offer reuse/extend, new slug, or explicit overwrite; never silent overwrite. |
| `MANIFEST_SHAPE_DRIFT` | Manifest entry fields differ from the profile | Trust the live manifest; update the profile note and match the live shape. |

## Tone & Calibration

- **Convention-first, runtime-verified.** Read the real files; never assume the profile is perfectly current.
- **Reuse over rebuild.** Surface overlapping prototypes so the builder branches instead of duplicating.
- **Thin orchestrator.** Chrome + switching only; no composition here.

## Related Skills

- **sandbox-composer** — fills the scaffolded scene files with real components + demo data.
- **scene-mapper** — supplies the scenes/options this skill lays out.

---

**Last Updated**: 2026-09-09
**Maintainer**: Mattermost Design Team
