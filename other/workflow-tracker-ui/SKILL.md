---
name: workflow-tracker-ui
description: Open the Workflow Foundry tracker UI quickly, start it when needed, or run explicit tracker verification before opening.
---

# Workflow Tracker UI

Use this skill when the user wants to open, run, inspect, or verify the
Workflow Foundry tracker UI.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: `$workflow-tracker-ui` is the operator surface. The
Astro/npm commands below are internal support for opening or verifying the
tracker UI, not the primary way to call this skill.

## Internal Support

1. Work from the repo root.
2. Check whether the tracker is already reachable at `http://127.0.0.1:4321`.
3. If it is reachable, open that URL for the user and report that the existing
   server was reused.
4. If it is not reachable, start the tracker from
   `projects/workflow-foundry/tracker` with:

   ```sh
   npm run dev -- --port 4321
   ```

5. Wait until `http://127.0.0.1:4321` responds, then open it for the user.
6. Report the URL and whether the server was reused or started.

## Developer Verification Mode

Use this branch only when the user asks to verify, test, build, or check the
tracker before opening it.

1. From `projects/workflow-foundry/tracker`, run:

   ```sh
   npm run verify
   ```

2. From the repo root, run:

   ```sh
   node scripts/validate-workflow-state.mjs
   ```

3. If verification passes, open the tracker using the default fast-open path.
4. If verification fails, report the failing command and stop before opening
   unless the user explicitly asks to inspect the broken UI.

## Boundaries

- The tracker UI is read-only against project and task JSON.
- Do not create slash-command shims for this skill.
- Do not edit tracker state as part of opening the UI.
- Browser selection state may live in `localStorage`; canonical workflow state
  remains in project and task JSON.
