---
name: project-context
description: "Load the full Struq Voice picture before starting any task: what the project is, the architecture map, the file inventory, current state, and the invariants that must never be broken. Invoke at the start of every session or when asked 'what is this project', 'load context', 'get up to speed', 'onboard me', 'where is X', or before making any change. Read AGENTS.md and docs/FEATURES.md first, then use this skill's map to locate files and respect boundaries without re-walking the whole tree. NOT for gating/verification (use verification-gates) or IPC wiring (use ipc-architecture)."
---

# Project context: Struq Voice

A tray-resident Windows dictation app. Hold a key anywhere in Windows,
speak, release, and the transcript appears in the focused field. Windows 10
and 11, 64-bit. Electron 39 pinned, React 19, Tailwind v4, TypeScript strict.

## Read in this order

1. `AGENTS.md` (repo root) - the source of truth.
2. `docs/FEATURES.md` - what is built, current state, known gaps.
3. `docs/ARCHITECTURE.md` - process/window model and boundaries.
4. For UI work: `docs/DESIGN_SYSTEM.md` (Evergreen and Ember, binding).

## Process model

```
MAIN PROCESS            RECORDER (hidden)      OVERLAY (never focused)
lifecycle · tray        warm getUserMedia       capture pill, live waveform
hotkeys · session       AudioWorklet -> PCM
engines · paste · db    -> main
                                                       MAIN WINDOW (on demand)
                                                       Dictate · History · Models · Settings
```

## File map (locate without grepping)

- Boot, wiring, single instance: `src/main/index.ts`
- Capture state machine: `src/main/session/capture-session.ts`
- Hotkeys: `src/main/hotkeys/{index,ptt-hook,toggle-shortcut}.ts`
- Audio pipeline (recorder renderer): `src/renderer/recorder/`
- Engines: `src/main/engines/`
- Models + catalog: `src/main/models/` + `src/shared/models.ts`
- Paste: `src/main/platform/win32/paste.ts`
- History: `src/main/db/`
- Settings + secrets: `src/main/store/` + `src/shared/settings.ts`
- Text cleanup: `src/main/post/text-cleanup.ts`
- IPC single source: `src/shared/ipc.ts` + `src/preload/*.ts`
- Tray: `src/main/tray.ts`
- Windows: `src/main/windows/`
- Main window UI: `src/renderer/main/`

## Invariants (never break)

- Renderer never imports from `src/main/`.
- `src/shared/` has no side effects and no Electron imports.
- Every IPC channel is declared in `src/shared/ipc.ts` and nowhere else.
- Every window: `contextIsolation: true`, `nodeIntegration: false`,
  `sandbox: true`.
- No em dashes / en dashes / horizontal bars anywhere, ever.

## Current state (verified)

All 7 plan phases are built and committed. The unit suite, typecheck, lint,
and the headless dev e2e suite are green. See
`docs/FEATURES.md` for the details and the short known-gaps list (settings +
a11y e2e specs not written, manual checklist not run, shadcn not adopted).
