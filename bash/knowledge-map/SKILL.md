---
name: knowledge-map
description: Configure, build, and run the local 3D knowledge map for Markdown and text sources.
argument-hint: "[map title or source categories]"
---

# Knowledge Map

This skill builds an independent local 3D explorer with drag-to-orbit, zoom, auto-rotation, and a cinema view. It does not require external services or API keys.

Read:
- `SYSTEM.md`
- `apps/knowledge-map/README.md`
- `apps/knowledge-map/map.config.json`
- `apps/knowledge-map/map.config.local.json`, if present (takes precedence over shared defaults)

## Configure

Reuse the existing title and verified source paths when available. A bare invocation rebuilds and opens the current map; it does not reset configuration.

Ask only for information not already supplied:

1. What should the map be called?
2. Which local categories should it include?

For each category, record:
- an ID,
- display label,
- one or more verified local paths.

Use 1–10 categories. Do not guess paths.

Update `apps/knowledge-map/map.config.local.json` so user-specific paths remain untracked.

## Build and run

From repository root:

```bash
node scripts/build-map.mjs
node scripts/serve-map.mjs
```

The server binds only to `127.0.0.1`. Use the configured port (default `4747`). If that address already serves this map, reuse it instead of launching a duplicate server.

Open the local URL when browser access is available; otherwise provide the link. Explain that dragging orbits the globe, scrolling zooms, and clicking a sphere reads a note. The app README documents keyboard and touch controls.

## Verify

Confirm:
- the generated node count is nonzero when selected sources contain notes,
- configured categories appear,
- dragging changes the viewing angle, zoom works, and auto-rotation can be started and paused,
- cinema mode can be entered and exited,
- search finds a known note,
- category filtering works,
- selecting a node opens its note content; Browse notes also provides keyboard-accessible selection,
- explicit Markdown links are rendered when their target can be resolved,
- no source files were modified.

Only indexed files and resolved explicit links count as knowledge. Curved globe/orbit guides are decorative.

If a category is empty, report it honestly. Do not invent knowledge to populate the map.
