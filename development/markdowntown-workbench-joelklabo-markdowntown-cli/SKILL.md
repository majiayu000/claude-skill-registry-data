---
name: markdowntown-workbench
description: Use this when working on the Workbench UI, Workbench state/store, export/compile pipeline, or adapter/target behavior (agents-md, claude-code, github-copilot, etc.).
---

# Workbench + export pipeline

## When to use
- Building or refactoring Workbench UI panels, onboarding, or actions.
- Updating Workbench state (UAM v1, scopes, blocks, targets) or scan handoff.
- Changing compile/export behavior, adapters, or target options.

## Quick map
- **Workbench UI + state:** `src/components/workbench/*` + `src/hooks/useWorkbenchStore.ts`
- **Compile endpoint:** `src/app/api/compile/route.ts`
- **Compile + adapters:** `src/lib/compile/compile.ts`, `src/lib/adapters/*`, `src/lib/uam/compile/*`
- **Export UX:** `src/components/workbench/ExportPanel.tsx`

## Workflow
1. **Confirm entry point**
   - Identify whether the change is UI-only, state-only, or export pipeline.
   - Workbench state lives in `useWorkbenchStore`; it normalizes UAM v1 and syncs legacy fields.

2. **State + targets**
   - Targets are stored on the UAM v1 definition; changes should flow through `setUam` + target helpers.
   - When adjusting scan → Workbench handoff, review `applyScanContext` and `SCAN_TOOL_TARGET_MAP`.

3. **Export/compile behavior**
   - Export panel calls `/api/compile` (debounced) and displays the compilation result.
   - Update compile or adapter logic in `src/lib/compile/compile.ts` and `src/lib/adapters/*`.
   - Keep file path collisions and warnings surfaced (compile result is shown in Workbench).

4. **Adapters**
   - Adapters define target-specific output; register new adapters in the registry.
   - If adapter output or options change, update `docs/architecture/skills-export-matrix.md`.

5. **Tests + checks**
   - Run `npm run compile`, `npm run lint`, `npm run test:unit`.
   - If you change export behavior, check any Workbench/E2E references and update tests as needed.

## References
- codex/skills/markdowntown-workbench/references/workbench-ui.md
- codex/skills/markdowntown-workbench/references/compile-adapters.md

## Guardrails
- Prefer UAM v1 helpers (`createUamTargetV1`, `normalizeUamTargetsV1`) to avoid drift.
- Keep Workbench strings aligned with `docs/ux/microcopy-guidelines.md`.
- Always look for refactoring or bugs; create new bd tasks when you spot them.
