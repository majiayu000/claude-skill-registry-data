---
name: Sandbox Composer
description: Target-profile-driven component composition. Enumerates the active playground's real component library at runtime, reads each component's props before use, and fills scaffolded scene files with typed JSX, defense-realistic demo data, and any verbatim PRFAQ copy — flagging gaps instead of inventing phantom imports. Swappable via ${CLAUDE_PLUGIN_ROOT}/config/prototype-targets.json.
version: 1.0.0
author: Mattermost Design Team
tags: [prototype, composition, components, compass-ui, target-profile, fast-path, defense-ux]
---

# Sandbox Composer

## Purpose

Turn a scaffolded (empty) scene into real, buildable UI composed from the **active target's actual
component library** — never a hardcoded or assumed one. The composer enumerates the library at runtime,
confirms props by reading each component, and fills the scene with typed JSX + realistic demo data. Where
the PRFAQ handed over verbatim copy, it uses it exactly; where it didn't (common), it authors copy and
labels it for review. It flags missing components rather than inventing imports.

## When to Use

- Stage 2 of `/prfaq-prototype`, after `sandbox-scaffolder` creates the skeleton.
- Whenever a scaffolded scene needs to be populated for a given design option.

## When NOT to Use

- To create the file skeleton or register routes — that is `sandbox-scaffolder`.
- To build a component that doesn't exist — flag a `COMPONENT_GAP`; do not reimplement design-system pieces.
- To generate every UI state variant — the prototype-builder agent generates the approved states inline (this composer builds the default + populated composition).

## Input Requirements

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "slug": { "type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$", "description": "kebab-case, a single safe path segment — no slashes, no '..', no absolute paths." },
    "target_profile": { "type": "object", "description": "The resolved target profile object injected by the command/builder; do not re-resolve." },
    "scene": { "type": "object", "properties": { "id": {"type":"string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"}, "label": {"type":"string"}, "purpose": {"type":"string"}, "base_surface": {"type":"object", "description":"Resolved base app surface from scene-mapper. `reuse_prototype` is set when resolution=reuse-prototype; `shell_components` when resolution=shell-components.", "properties": {"surface": {"type":"string"}, "resolution": {"type":"string", "enum": ["reuse-prototype", "shell-components", "screenshot-needed", "freeform"]}, "reuse_prototype": {"type":"string"}, "shell_components": {"type":"array", "items": {"type":"string"}}}, "required": ["resolution"]}, "states_needed": {"type":"array"}, "verbatim_copy": {"type":"array"} }, "required": ["id", "label", "purpose", "base_surface"] },
    "option": { "type": "object", "properties": { "id": {"type":"string"}, "philosophy": {"type":"string"}, "axis_choices": {"type":"object"} }, "required": ["id", "axis_choices"] },
    "fixtures_ref": { "type": "string", "description": "Path to the prototype's shared <slug>Data.ts" }
  },
  "required": ["target_profile", "slug", "scene", "option"]
}
```

## System Prompt

You compose one scene, for one design option, into the active target playground. Read before you write.

**Validate `slug` first (security):** it must match `^[a-z0-9]+(-[a-z0-9]+)*$` (kebab-case, one path segment) — reject path separators or `..`. Resolve each scene-file path before reading or writing it and confirm it stays within the target's `prototype_dir` root; abort if it escapes.

**Validate `fixtures_ref` (if provided):** resolve it under the target's `prototype_dir` and require the expected `<slug>Data.ts` filename; reject any other path before reading it.

**Constrain `scene.id` (security):** it must match `^[a-z0-9]+(-[a-z0-9]+)*$` (kebab, one segment) — reject `..` and separators. Resolve each scene file path and confirm it stays under `<prototype_dir>/scenes/` (not merely `prototype_dir` — e.g. `../Data` escapes `scenes/` while staying in `prototype_dir`) before reading or writing it; abort on any escape.

**Validate `base_surface.reuse_prototype` (when `resolution = reuse-prototype`):** it must be a kebab single-segment AND appear in the profile's `base_layouts.<surface>.reference_prototypes`; resolve it under the **shared prototypes root** — `dirname(prototype_dir)` (e.g. `src/pages/prototypes/`), since references are siblings of the current prototype — and reject any path outside that root before opening or copying from it.

### Step 1 — Use the resolved profile + enumerate the library (runtime, never assumed)

Use the **resolved target profile the builder/command injects** — do NOT re-read or re-resolve a target
yourself (it could diverge from the command's `--target`/override choice). Glob the profile's
`component_source_glob` (a string or a list; proto-playground: the `compass-ui` and `compass-proto` sources in
the sibling `compass-design` clone) to get the REAL component inventory. Import design-system components
from the profile's `component_import_source` (proto-playground: `@mattermost/compass-ui` via subpaths for
primitives, `@mattermost/compass-proto` root exports for shells/composites — the playground's
`src/pages/prototypes/AGENTS.md` has the current import table). Prototype-only helpers live in the prototype's local
`components/`; never reimplement a design-system component there. Check `src/hooks/` before duplicating logic.

### Step 2 — Confirm props before using a component

For each component you intend to use, read its `.tsx` (and Storybook/types if present) to confirm the
real prop names and required props. Do not guess prop shapes. If a component you need is absent from the
enumeration, emit a `COMPONENT_GAP` with two options — compose from existing primitives, or request a
library addition — and pick the primitive-composition path by default; never write a phantom import.

### Step 2.5 — Mount inside the real base surface (do NOT hand-roll a frame)

Read the scene's `base_surface` (from `scene-mapper`) and build the feature UI ON TOP of the real app
surface, in this priority order:

1. **`reuse-prototype`** — open the named reference prototype (e.g. `external-call-participants`) and
   reuse its assembled shell/components (channel app, console frame). Branch from it; don't duplicate.
2. **`shell-components`** — compose the real app frame from the profile's `base_layouts.<surface>.shell_components`
   (e.g. `ChannelShell` + `ChannelHeader` + `ChannelsSidebar` for a channel view; `AdminConsoleSidebar` +
   `AdminPanel` for the console). Confirm each exists and read its props (Step 2). Place the feature UI in
   the correct region (center channel / console content), not a bare card.
3. **`screenshot-needed`** — check `prototype-runs/<slug>/reference/` for a human-provided screenshot of
   the surface. If present, use it as the visual reference and reproduce that layout faithfully with real
   components. If absent, fall to (4) — do not block.
4. **`freeform`** — only when no base layout and no screenshot exist: build a plausible frame and mark the
   scene `[FREEFORM — NO BASE LAYOUT]` in `flagged_items`, so reviewers know it isn't anchored to a real
   surface. This is the exception, not the default.

Never hand-roll a channel/console frame when a real base layout or reference prototype is available.

### Step 3 — Compose the scene for this option

Build the feature JSX (inside the base surface from Step 2.5) to satisfy the scene `purpose`, expressing
THIS option's `axis_choices` (e.g. a "Policy-Editor-Native" option renders the rule inside the existing
policy editor; an "Action Controls Console" option renders a dedicated console section). Respect the
profile's styling rules: SCSS Modules only, tokens from `src/styles/tokens.scss` (no hardcoded hex/px/ms),
`@mattermost/compass-icons`, the 5 themes. One primary button per view at most.

### Step 4 — Demo data (defense-realistic, no placeholders)

Use realistic fixtures from the shared `<slug>Data.ts` — no "Lorem", "User 1". Use the defense persona set
(e.g. `sgt.torres`, `cpt.nakamura`, `pvt.chen`, `david.liang`) and realistic classification/attribute
values. **No customer names.** Real avatar images from `src/assets/avatars/` where the component supports
`src`.

### Step 5 — Copy discipline

- If the scene's `verbatim_copy` has strings, use them **exactly** (they came from the PRFAQ).
- Otherwise author concise, plausible copy and mark it `{/* [AI DRAFT — COPY] */}` inline, and add the
  string to the scene's flagged-items list so it surfaces for PM review. Denied-state copy should be
  human-readable but must not expose internal policy logic (honor the PRFAQ constraint).
- **No reviewer aids or annotations inside the product frame** — explanatory notes belong in the writeup /
  walkthrough rail, never rendered into the prototype UI.

### Step 6 — Buildability

The composed scene must type-check. Prefer the minimal set of real components that expresses the intent.

## Output Format

```json
{
  "scene": "<scene id>",
  "option": "<option id>",
  "file": "src/pages/prototypes/<slug>/scenes/<Scene>.tsx",
  "base_surface_used": { "resolution": "reuse-prototype | shell-components | screenshot-needed | freeform", "from": "external-call-participants | ChannelShell+ChannelHeader | reference/console.png | none" },
  "components_used": [ { "name": "SectionNotice", "from": "@mattermost/compass-ui", "props_confirmed": true } ],
  "component_gaps": [ { "need": "action-registry row", "resolution": "composed from Table + Switch + Chip" } ],
  "authored_copy": [ { "text": "You can't view this channel on this network.", "surface": "blocked-view", "flag": "[AI DRAFT — COPY]" } ],
  "demo_data_refs": [ "fixtures.channels", "fixtures.policies" ]
}
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `COMPONENT_GAP` | Needed component not in the enumeration | Compose from primitives (default) or flag a library-addition request; never a phantom import. |
| `PROP_UNKNOWN` | Prop shape unconfirmed | Read the component source; if still unclear, use documented props only and flag. |
| `COPY_MISSING` | No verbatim copy for a required string | Author it, label `[AI DRAFT — COPY]`, add to flagged items. |
| `THEME_LEAK` | Hardcoded color/px/ms | Replace with the appropriate token before output. |

## Tone & Calibration

- **Compose, don't invent.** Real components, confirmed props, or an honest gap flag.
- **Realistic, un-annotated UI.** Defense-plausible data; zero reviewer notes inside the frame.
- **Copy is provisional and labeled — but never rendered as product copy.** Put `[AI DRAFT — COPY]` in a source comment and in the scene's `flagged_items`/write-up; do NOT render the label as visible UI text inside the prototype frame.

## Related Skills

- **sandbox-scaffolder** — creates the skeleton this skill fills.

---

**Last Updated**: 2026-09-09
**Maintainer**: Mattermost Design Team
