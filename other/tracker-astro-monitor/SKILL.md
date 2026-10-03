---
name: tracker-astro-monitor
description: Build and maintain the read-only Astro dashboard that monitors this control repo's tracker state, workflow runs, workstreams, upload status, stale surfaces, and next actions from local ops JSON only.
---

# Tracker Astro Monitor

Use this workflow when the user wants a local UI for watching what is happening
inside the control repo tracker.

## Repeated Job

Turn the file-backed tracker state under `ops/` into a read-only Astro
dashboard that an operator can open locally to see current projects,
workstreams, workflow runs, upload status, stale/non-project surfaces, and next
actions.

## Trigger

Use this workflow when the user asks to:

- build or update the tracker monitor UI;
- inspect tracker state visually;
- add a 2D dashboard panel for workflow runs, projects, sessions, upload state,
  or stale surfaces;
- make the control repo easier to monitor without changing tracker authority.

Refuse or reroute when the request wants third-party writes, publishing,
credential changes, live remote mutation, replacing the tracker registry, or a
non-Astro app stack.

## Input Contract

The workflow reads only local tracker surfaces:

- `ops/registry/projects.json`;
- `ops/registry/workstreams.json`;
- `ops/registry/workflow-runs.json`;
- `ops/sync/github-upload-state.json`;
- optional event, session, handoff, and daily-rollup files when future panels
  need them.

The UI must not infer active projects from folder names, stale README tables, or
old lane docs. Tracker registry state remains authoritative.

## Output Artifact

The current output is a static Astro dashboard:

- export adapter: `node scripts/control-repo.mjs export-tracker-ui-data`;
- dashboard snapshot: `tracker-ui/src/data/tracker-dashboard.json`;
- Astro route: `tracker-ui/src/pages/index.astro`;
- styles: `tracker-ui/src/styles/global.css`;
- validation: `tests/control-repo.test.mjs`.

## Agent Lanes

- tracker-data lane: read and normalize local tracker JSON.
- UI lane: render a dense, work-focused, 2D Astro dashboard.
- validation lane: prove the exporter and route consume the expected snapshot.
- review lane: check that no UI panel claims authority beyond tracker data.

## Validation Loop

Before treating monitor changes as complete, run:

```bash
npm test
npm run build
npm run validate
git diff --check
```

## Safety Contract

This workflow is read-only. It must not:

- write to third-party systems;
- publish, push, merge, or post without explicit approval;
- mutate tracker registries from the browser;
- use credentials or auth bypasses;
- present folder scans as project authority;
- use 3D, WebGL, canvas scenes, or decorative app surfaces for the monitor.

The dashboard may show stale or non-project surfaces, but it must label them as
tracker context rather than active project truth.
