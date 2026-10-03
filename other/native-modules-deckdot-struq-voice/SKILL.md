---
name: native-modules
description: "Handle the native modules in Struq Voice: better-sqlite3, uiohook-napi, sherpa-onnx-node, and the Electron 39 rebuild story. Use whenever a task involves native modules, electron-builder rebuilds, the postinstall script, 'module failed to load', history unavailable, PTT broken, Parakeet not starting, @electron/rebuild, or an Electron version bump. Explains the rebuild script, the degradation paths (every module fails soft), and the rule never to upgrade Electron without explicit approval. NOT for IPC (use ipc-architecture) or gating (use verification-gates)."
argument-hint: "[rebuild | degrade | electron-version | missing-module]"
---

# Native modules in Struq Voice

Three native modules target Electron 39 specifically:

| Module | Purpose | Degradation if it fails |
|---|---|---|
| `better-sqlite3` | History (SQLite + FTS5) | History unavailable; transcription still works |
| `uiohook-napi` | PTT press-and-hold, keyTap paste | PTT falls back to toggle; app still boots |
| `sherpa-onnx-node` | Parakeet inference | Engine reports "runtime not installed" |

## The rebuild script

`scripts/rebuild-native-modules.mjs` runs on `postinstall` via pnpm. It finds
each module in the pnpm store and rebuilds it against the pinned Electron
version (`39.1.2` in the script). It never fails the install: each module is
handled only if present, and every failure logs a warning with a retry hint
instead of aborting.

Manual retries:

```bash
pnpm rebuild better-sqlite3
pnpm rebuild uiohook-napi
```

## The non-negotiable rule

**Do not upgrade Electron without the user's explicit request.** The 39 line
is chosen because native prebuilds for these three modules are a known
quantity there. Bumping Electron means re-verifying every native module, the
`@electron/rebuild` pass, and the e2e suite.

## Known runtime facts

- `better-sqlite3` + FTS5 verified working under Electron 39
  (`better-sqlite3+FTS5 OK: 1`).
- `uiohook-napi` must start only after the recorder stream is live; that is
  the structural fix for the getUserMedia-kills-the-hook issue, and it is
  verified by `hook.spec.ts`.
- `sherpa-onnx-node` loads under Electron via N-API (verified), so it does
  not need a rebuild the way the other two do, but it still follows the
  soft-degradation rule.

## Verifying after an install

```bash
pnpm install          # triggers postinstall rebuild
pnpm typecheck && pnpm lint && pnpm test
```

If the app boots with degraded features (no history, no PTT, no Parakeet),
check the `[native]` warnings from the rebuild script rather than the app
code. The cause is almost always the store path or a stale rebuild, not a
regression in `src/`.
